#!/usr/bin/env python3
"""Build/validate the allowlisted public Agent pack without internal sources."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import tarfile
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PACK = Path('.')
BUNDLE = 'subsea-cable-lang-pack'


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + '\n').encode()


def safe_path(name: str) -> PurePosixPath:
    path = PurePosixPath(name)
    if not name or '\\' in name or path.is_absolute() or any(p in {'.', '..'} for p in name.split('/')):
        raise ValueError(f'Unsafe manifest path: {name}')
    return path


def read_regular(root: Path, relative: str) -> bytes:
    safe_path(relative)
    path = root / relative
    if any(part.is_symlink() for part in [path, *path.parents] if part != root.parent):
        raise ValueError(f'Symlink is not a source file: {relative}')
    if not path.is_file() or not path.resolve().is_relative_to(root.resolve()):
        raise ValueError(f'Missing or escaping source file: {relative}')
    return path.read_bytes()


def expected_files(root: Path) -> tuple[dict[str, bytes], str]:
    metadata_bytes = read_regular(root, (PACK / 'pack.json').as_posix())
    metadata = json.loads(metadata_bytes)
    if metadata['name'] != BUNDLE or metadata['status'] != 'informative-authoring-pack':
        raise ValueError('Unexpected pack identity/status')
    if not re.fullmatch(r'\d+\.\d+\.\d+', metadata['version']):
        raise ValueError('Pack version must be explicit semver')
    revision = metadata['language_revision']
    if not re.fullmatch(r'[0-9a-f]{40}', revision):
        raise ValueError('Language revision must be a full commit identity')
    if metadata['license'] != 'Apache-2.0':
        raise ValueError('Expected repository license')

    sources = metadata['sources']
    if not sources:
        raise ValueError('No source provenance')
    for key, source in sources.items():
        safe_path(key)
        relative = safe_path(source['path'])
        if len(relative.parts) < 3 or relative.parts[:2] != ('upstream', 'export') or relative.parts[2] == 'agent-pack':
            raise ValueError(f'Source is not an approved public original: {relative}')
        if source['path'] != 'upstream/export/' + key or source['language_path'] != 'export/' + key:
            raise ValueError(f'Source key/path mismatch: {key}')
        if not source['public_url'].startswith('https://4gentsinc.github.io/subsea_cable_webpages/'):
            raise ValueError(f'Unexpected public source URL: {key}')
        current = read_regular(root, source['path'])
        if digest(current) != source['sha256']:
            raise ValueError(f'Source drift requires review and metadata refresh: {key}')

    payload = metadata['payload']
    if not payload or len(payload) != len(set(payload)):
        raise ValueError('Empty or duplicate payload')
    if set(metadata['module_sources']) != set(payload):
        raise ValueError('Each payload module needs source coverage')
    actual = {'SKILL.md'} | {p.relative_to(root).as_posix()
              for directory in ('knowledge', 'examples', 'adapters', 'evals')
              for p in (root / directory).rglob('*') if p.is_file()}
    if actual != set(payload):
        raise ValueError('Public pack source files differ from the explicit payload allowlist')
    files = {'pack.json': metadata_bytes, 'LICENSE': read_regular(root, 'LICENSE')}
    for name in payload:
        path = safe_path(name)
        if path.suffix not in {'.md', '.vyg', '.json'} or path.parts[0] not in {'SKILL.md', 'knowledge', 'examples', 'adapters', 'evals'}:
            raise ValueError(f'Unexpected public payload classification: {name}')
        if not metadata['module_sources'][name] or not set(metadata['module_sources'][name]) <= set(sources):
            raise ValueError(f'Missing or unknown sources for {name}')
        files[name] = read_regular(root, (PACK / name).as_posix())
        text = files[name].decode('utf-8', errors='strict')
        if re.search(r'confidential/|https://github\.com/on-the-ground/(?:subsea_cable_language|subsea_cable_vessel)(?:/|\b)', text):
            raise ValueError('Nonpublic source reference in payload: ' + name)
        for href in re.findall(r'!?\[[^\]\n]*\]\(([^\s)]+)\)', text):
            url = urlsplit(href)
            if url.scheme or url.netloc or not url.path:
                continue
            target = (root / PACK / path.parent / unquote(url.path)).resolve()
            if not target.is_relative_to((root / PACK).resolve()) or not target.is_file():
                raise ValueError(f'Broken or escaping pack link in {name}: {href}')
    modules = metadata['compact_modules']
    demonstrations = json.loads(files['evals/few-shot.json'])
    if demonstrations['status'] != 'prompt-demonstrations-not-held-out-evaluation':
        raise ValueError('Few-shot examples must be identified as demonstrations')
    cases = demonstrations['cases']
    if not cases or len({case['id'] for case in cases}) != len(cases):
        raise ValueError('Missing or duplicate few-shot cases')
    for case in cases:
        answer = safe_path(case['answer'])
        if answer.suffix != '.vyg' or str(answer) not in files or not case['request'] or not case['review']:
            raise ValueError('Incomplete or missing few-shot answer')
    if not modules or len(modules) != len(set(modules)) or not set(modules) <= set(payload):
        raise ValueError('Invalid compact module selection')
    compact = (f'# Subsea Cable compact context\n\nPack {metadata["version"]}; '
               f'language revision `{revision}`.\nInformative authoring knowledge, not Runtime execution evidence.\n'
               'For syntax and examples, read SKILL.md and the on-demand modules.\n\n').encode()
    compact += b'\n\n'.join(files[name] for name in modules)
    if len(compact) > metadata['compact_byte_budget']:
        raise ValueError(f'Compact context exceeds byte budget: {len(compact)}')
    files['subsea-cable-context.md'] = compact
    files['release.json'] = json_bytes({
        'name': BUNDLE, 'version': metadata['version'], 'language_revision': revision,
        'compact_bytes': len(compact), 'files': {name: digest(content) for name, content in sorted(files.items())},
    })
    return files, metadata['version']


def archive_bytes(files: dict[str, bytes]) -> bytes:
    tar = io.BytesIO()
    with tarfile.open(fileobj=tar, mode='w', format=tarfile.PAX_FORMAT) as archive:
        for name, data in sorted(files.items()):
            item = tarfile.TarInfo(BUNDLE + '/' + name)
            item.size, item.mode, item.mtime = len(data), 0o644, 0
            item.uid = item.gid = 0
            item.uname = item.gname = ''
            archive.addfile(item, io.BytesIO(data))
    output = io.BytesIO()
    with gzip.GzipFile(fileobj=output, mode='wb', filename='', mtime=0, compresslevel=9) as stream:
        stream.write(tar.getvalue())
    return output.getvalue()


def package(root: Path, output: Path, mode: str) -> None:
    files, version = expected_files(root)
    output = output.absolute()
    if output.resolve().is_relative_to(root.resolve()) or root.resolve().is_relative_to(output.resolve()):
        raise ValueError('Output must be outside the source checkout and must not contain it')
    if any(p.is_symlink() for p in [output, *output.parents]):
        raise ValueError('Output path must not contain symlinks')
    bundle = output / BUNDLE
    archive = output / f'{BUNDLE}-{version}.tar.gz'
    expected_archive = archive_bytes(files)
    if mode == 'build':
        if output.exists() and any(output.iterdir()):
            raise ValueError('Build output must be empty; choose a new directory')
        bundle.mkdir(parents=True)
        for name, content in files.items():
            destination = bundle / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(content)
        archive.write_bytes(expected_archive)
    else:
        if not output.is_dir() or {p.name for p in output.iterdir()} != {BUNDLE, archive.name}:
            raise ValueError('Missing or unexpected distribution artifact')
        actual = {p.relative_to(bundle).as_posix() for p in bundle.rglob('*') if p.is_file()}
        if any(p.is_symlink() for p in [bundle, archive, *bundle.rglob('*')]):
            raise ValueError('Distribution must not contain symlinks')
        if actual != set(files):
            raise ValueError('Missing or unexpected generated file')
        for name, content in files.items():
            if read_regular(bundle, name) != content:
                raise ValueError(f'Stale or modified generated file: {name}')
        if archive.read_bytes() != expected_archive:
            raise ValueError('Stale or modified archive')
    print(f'{mode}: {len(files)} public files; archive sha256 {digest(expected_archive)}; {archive}')


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['build', 'validate'])
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    try:
        package(ROOT, args.output, args.mode)
    except (ValueError, KeyError, subprocess.CalledProcessError) as error:
        parser.exit(1, str(error) + '\n')


if __name__ == '__main__':
    main()
