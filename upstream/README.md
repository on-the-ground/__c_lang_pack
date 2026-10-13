# Immutable public-source verification snapshot

Only the public `export/` files named by `pack.json` are copied here at its
target language commit. These are integrity/conformance inputs, not separately
editable language definitions. Use the public URLs in the manifest for reading;
the snapshot does not reproduce the entire documentation site's link closure.

Update through `scripts/sync_sources.py` from an authorized language checkout.
It checks the exact immutable commit, path allowlist and expected hashes. It
does not fetch private sources. CI validates the snapshot locally and requires
no language-repository token or checkout. A changed source is reviewed before
its metadata and summaries are updated.
