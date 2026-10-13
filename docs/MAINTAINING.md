# Maintain the independent pack

This repository owns authoring knowledge, examples, packaging and prompting
guidance. The language repository owns the language; the Runtime repository
owns semantic validation and MCP execution integration. Do not add the pack
back to the language repository or fork its semantic validator here.

`pack.json` records an independent pack version, target language commit,
per-module sources and source hashes. The immutable public snapshot under
`upstream/` lets CI run without access to a private language checkout. It is a
verification input, not a second editable specification. No confidential files,
repository operational instructions or experiment oracle enter distribution.

After a reviewed source/content update:

```sh
python scripts/sync_sources.py --language-repo /path/to/authorized/language
python scripts/package.py build --output /tmp/new-empty-pack-output
python scripts/package.py validate --output /tmp/new-empty-pack-output
python scripts/test_package.py
python scripts/check_examples.py --antlr-jar /path/to/antlr-4.13.2-complete.jar
python scripts/test_syntax_cli.py --antlr-jar /path/to/antlr-4.13.2-complete.jar
```

Refresh fingerprints only after checking new summaries against their sources;
increment the content version when a shipped version changes. The initial
0.1.0 proposal has not been released. Pack, language and Runtime versions remain
distinct. Verify payload bytes, source snapshots, examples and compact budget
before distributing the generated archive. `release.json` detects changed bytes,
not publisher authenticity; use a trusted channel and record the archive digest.

For real Agent testing, keep few-shot demonstrations separate from held-out
tasks and record pack/model/tool revisions, context actually loaded, actual
validator feedback and output. No pass rate or improvement is inferred from
static checks. U1 execution feedback and production default installation remain
follow-up integration work.
