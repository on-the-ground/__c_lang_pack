"""Check syntax only; never report semantic or execution validation as passed."""
import argparse
import csv
import hashlib
import importlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

from package import ROOT, expected_files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--antlr-jar', required=True, type=Path)
    parser.add_argument('--source', type=Path)
    args = parser.parse_args()
    expected_files(ROOT)  # Validate the snapshot/payload before parser generation.
    from antlr4 import CommonTokenStream, InputStream
    from antlr4.error.ErrorListener import ErrorListener
    from syntax import normalize

    class Errors(ErrorListener):
        def __init__(self, source):
            self.source, self.diagnostics = source, []

        def syntaxError(self, recognizer, symbol, line, column, message, error):
            self.diagnostics.append({'phase': 'syntax', 'severity': 'error',
                                     'code': 'SyntaxError', 'source': self.source,
                                     'line': line, 'column': column, 'message': message})

    with tempfile.TemporaryDirectory() as directory:
        grammar = ROOT / 'upstream/export/SubseaCable.g4'
        subprocess.run(['java', '-jar', str(args.antlr_jar), '-Werror', '-Dlanguage=Python3',
                        '-no-listener', '-no-visitor', '-Xexact-output-dir', '-o', directory,
                        str(grammar)], check=True)
        sys.path.insert(0, directory)
        lexer_class = importlib.import_module('SubseaCableLexer').SubseaCableLexer
        parser_class = importlib.import_module('SubseaCableParser').SubseaCableParser

        def check(path):
            errors = Errors(str(path))
            data = path.read_bytes()
            try:
                text = data.decode('utf-8', errors='strict')
            except UnicodeDecodeError:
                return [{'phase': 'encoding', 'severity': 'error', 'source': str(path),
                         'code': 'InvalidSourceEncoding', 'message': 'Source must be strict UTF-8'}]
            lexer = lexer_class(InputStream(text))
            lexer.removeErrorListeners()
            lexer.addErrorListener(errors)
            tokens = normalize(lexer, parser_class)
            instance = parser_class(CommonTokenStream(tokens))
            instance.removeErrorListeners()
            instance.addErrorListener(errors)
            instance.program()
            return errors.diagnostics

        if args.source:
            diagnostics = check(args.source)
            report = {'syntax_ok': not diagnostics, 'diagnostics': diagnostics,
                      'source_sha256': hashlib.sha256(args.source.read_bytes()).hexdigest(),
                      'checked': {'syntax': True, 'semantics': False, 'host': False, 'execution': False}}
            status = bool(diagnostics)
        else:
            corpus = ROOT / 'upstream/export/conformance'
            rows = list(csv.DictReader((corpus / 'cases.tsv').open(), delimiter='\t'))
            mismatches = []
            for row in rows:
                diagnostics = check(corpus / row['file'])
                expected_parse = not (row['phase'] == 'syntax' and row['expected'] != 'accept')
                if (not diagnostics) != expected_parse:
                    mismatches.append({'file': row['file'], 'expected_parse': expected_parse,
                                       'diagnostics': diagnostics})
            examples = sorted((ROOT / 'examples').glob('*.vyg'))
            if not examples:
                raise ValueError('No pack examples found')
            invalid = [{'file': str(p.relative_to(ROOT)), 'diagnostics': check(p)} for p in examples]
            invalid = [item for item in invalid if item['diagnostics']]
            report = {'corpus_cases': len(rows), 'corpus_mismatches': mismatches,
                      'examples_checked': len(examples), 'invalid_examples': invalid,
                      'checked': {'syntax': True, 'semantics': False, 'host': False, 'execution': False}}
            status = bool(mismatches or invalid)
        report['language_revision'] = json.loads((ROOT / 'pack.json').read_text())['language_revision']
        report['antlr_jar_sha256'] = hashlib.sha256(args.antlr_jar.read_bytes()).hexdigest()
        report['position_units'] = 'line:1-based; column:0-based Unicode code points'
        print(json.dumps(report, indent=2))
        return int(status)


if __name__ == '__main__':
    raise SystemExit(main())
