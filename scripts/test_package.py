#!/usr/bin/env python3
"""Exercise distribution determinism and leakage/staleness rejection."""
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('agent_pack_package', Path(__file__).with_name('package.py'))
package = importlib.util.module_from_spec(spec)
spec.loader.exec_module(package)


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.output = self.root / 'output'

    def build(self):
        package.package(package.ROOT, self.output, 'build')
        return self.output / package.BUNDLE

    def test_deterministic_archives_and_public_members(self):
        files, version = package.expected_files(package.ROOT)
        self.assertEqual(package.archive_bytes(files), package.archive_bytes(dict(reversed(list(files.items())))))
        bundle = self.build()
        package.package(package.ROOT, self.output, 'validate')
        self.assertFalse(any('confidential' in p for p in files))
        self.assertFalse(any(p.startswith('.github/') for p in files))
        release = json.loads((bundle / 'release.json').read_text())
        for name, fingerprint in release['files'].items():
            self.assertEqual(package.digest((bundle / name).read_bytes()), fingerprint)
        self.assertLessEqual(release['compact_bytes'], 18000)

    def test_rejects_changed_missing_and_extra_generated_files(self):
        bundle = self.build()
        target = bundle / 'knowledge/model.md'
        original = target.read_bytes()
        target.write_bytes(original + b'altered')
        with self.assertRaisesRegex(ValueError, 'modified generated file'):
            package.package(package.ROOT, self.output, 'validate')
        target.unlink()
        with self.assertRaisesRegex(ValueError, 'Missing or unexpected generated file'):
            package.package(package.ROOT, self.output, 'validate')
        target.write_bytes(original)
        (bundle / 'unexpected.md').write_text('unexpected')
        with self.assertRaisesRegex(ValueError, 'Missing or unexpected generated file'):
            package.package(package.ROOT, self.output, 'validate')

    def test_rejects_archive_tampering(self):
        self.build()
        archive = next(self.output.glob('*.tar.gz'))
        archive.write_bytes(archive.read_bytes() + b'changed')
        with self.assertRaisesRegex(ValueError, 'modified archive'):
            package.package(package.ROOT, self.output, 'validate')

    def test_rejects_traversal_and_symlink_sources(self):
        for name in ['../confidential/AGENTS.md', '/tmp/x', 'knowledge/../../secret', 'knowledge\\secret']:
            with self.assertRaisesRegex(ValueError, 'Unsafe manifest path'):
                package.safe_path(name)
        (self.root / 'secret').write_text('private')
        (self.root / 'linked').symlink_to(self.root / 'secret')
        with self.assertRaisesRegex(ValueError, 'Symlink'):
            package.read_regular(self.root, 'linked')

    def test_rejects_distribution_symlinks_and_source_overwrite(self):
        bundle = self.build()
        target = bundle / 'knowledge/model.md'
        target.unlink()
        target.symlink_to(package.ROOT / package.PACK / 'knowledge/model.md')
        with self.assertRaisesRegex(ValueError, 'symlinks'):
            package.package(package.ROOT, self.output, 'validate')
        with self.assertRaisesRegex(ValueError, 'outside the source checkout'):
            package.package(package.ROOT, package.ROOT / 'dist', 'build')

    def test_rejects_source_fingerprint_drift(self):
        # A standalone clone needs no private language checkout or git objects.
        source = self.root / 'checkout'
        source.mkdir()
        shutil.copyfile(package.ROOT / 'pack.json', source / 'pack.json')
        shutil.copytree(package.ROOT / 'upstream', source / 'upstream')
        (source / 'upstream/export/LANGUAGE_REFERENCE.md').write_text('changed language source')
        with self.assertRaisesRegex(ValueError, 'Source drift'):
            package.expected_files(source)

    def test_rejects_missing_few_shot_answer(self):
        source = self.root / 'checkout'
        shutil.copytree(package.ROOT, source, ignore=shutil.ignore_patterns('.git', '__pycache__', 'dist'))
        target = source / 'evals/few-shot.json'
        pairs = json.loads(target.read_text())
        pairs['cases'][0]['answer'] = 'examples/not-present.vyg'
        target.write_text(json.dumps(pairs))
        with self.assertRaisesRegex(ValueError, 'missing few-shot answer'):
            package.expected_files(source)

    def test_rejects_unlisted_source_payload_and_private_reference(self):
        source = self.root / 'checkout'
        shutil.copytree(package.ROOT, source, ignore=shutil.ignore_patterns('.git', '__pycache__', 'dist'))
        extra = source / 'knowledge/unlisted.md'
        extra.write_text('unreviewed extra payload')
        with self.assertRaisesRegex(ValueError, 'explicit payload allowlist'):
            package.expected_files(source)
        extra.unlink()
        target = source / 'knowledge/model.md'
        target.write_text(target.read_text() + '\nconfidential/hidden.md\n')
        with self.assertRaisesRegex(ValueError, 'Nonpublic source reference'):
            package.expected_files(source)


if __name__ == '__main__':
    unittest.main()
