"""Import only declared public sources from an authorized immutable checkout."""
import argparse
import hashlib
import json
import re
from pathlib import Path, PurePosixPath
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def sync(repo):
    metadata = json.loads((ROOT / 'pack.json').read_text())
    revision = metadata['language_revision']
    if not re.fullmatch(r'[0-9a-f]{40}', revision):
        raise ValueError('Source revision must be a full immutable commit identity')
    # Validate every byte before changing this repository.
    pending = []
    for source in metadata['sources'].values():
        path = PurePosixPath(source['language_path'])
        if (path.is_absolute() or '..' in path.parts or '\\' in str(path)
                or len(path.parts) < 2 or path.parts[0] != 'export'
                or path.parts[1] == 'agent-pack'
                or source['path'] != 'upstream/' + str(path)):
            raise ValueError('Only declared public export sources may be imported')
        data = subprocess.check_output(['git', 'show', revision + ':' + str(path)], cwd=repo)
        if hashlib.sha256(data).hexdigest() != source['sha256']:
            raise ValueError('Pinned source fingerprint differs: ' + str(path))
        destination = ROOT / source['path']
        if any(p.is_symlink() for p in [destination, *destination.parents]):
            raise ValueError('Refusing a symlink destination')
        pending.append((destination, data))
    for destination, data in pending:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
    print('Verified and imported', len(pending), 'public sources at', revision)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--language-repo', required=True, type=Path)
    args = parser.parse_args()
    sync(args.language_repo)
