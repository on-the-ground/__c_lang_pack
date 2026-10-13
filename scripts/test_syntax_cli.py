"""Exercise exit codes, diagnostic scope, encoding and original-source positions."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from package import ROOT


class SyntaxCliTests(unittest.TestCase):
    jar = None

    def check(self, path):
        process = subprocess.run([sys.executable, str(ROOT / 'scripts/check_examples.py'),
                                  '--antlr-jar', str(self.jar), '--source', str(path)],
                                 capture_output=True, text=True, cwd=ROOT)
        report = json.loads(process.stdout)
        self.assertEqual(report['source_sha256'], hashlib.sha256(path.read_bytes()).hexdigest())
        self.assertFalse(report['checked']['semantics'])
        self.assertFalse(report['checked']['host'])
        self.assertFalse(report['checked']['execution'])
        return process.returncode, report

    def test_semantically_invalid_source_is_only_syntax_checked(self):
        code, report = self.check(ROOT / 'upstream/export/conformance/invalid-semantic/ArityMismatch.vyg')
        self.assertEqual(code, 0)
        self.assertTrue(report['syntax_ok'])
        self.assertEqual(report['diagnostics'], [])

    def test_invalid_utf8_fails_before_lexing(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'invalid.vyg'
            source.write_bytes(b'root Main/0\nMain = () -> "\xff"\n')
            code, report = self.check(source)
            self.assertEqual(code, 1)
            self.assertFalse(report['syntax_ok'])
            self.assertEqual(report['diagnostics'][0]['code'], 'InvalidSourceEncoding')

    def test_syntax_error_keeps_original_unicode_location(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'invalid.vyg'
            line = 'Main = () -> "🙂" ?'
            source.write_text('root Main/0\n' + line + '\n')
            code, report = self.check(source)
            self.assertEqual(code, 1)
            self.assertTrue(any(item['line'] == 2 and item['column'] == line.index('?')
                                for item in report['diagnostics']))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--antlr-jar', required=True, type=Path)
    args, remaining = parser.parse_known_args()
    SyntaxCliTests.jar = args.antlr_jar
    unittest.main(argv=[sys.argv[0], *remaining])
