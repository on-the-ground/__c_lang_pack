# What Unison does for Agent programming

Reviewed 2026-10-13 (Asia/Seoul). This is a source-based investigation, not a
live UCM experiment or a claim of measured Agent productivity. No upstream
implementation bodies are redistributed.

## Knowledge and tool feedback are separate

The owner's [unison-lang-pack](https://github.com/on-the-ground/unison-lang-pack/tree/f7975894e082e8e2dd15de5cd4e13eab9d90ce5a)
provides progressive knowledge modules and an optional compact attachment.
Its [entry](https://github.com/on-the-ground/unison-lang-pack/blob/f7975894e082e8e2dd15de5cd4e13eab9d90ce5a/SKILL.md)
directs the Agent to consult actual dependency APIs and typecheck its work.
The pack supplies context; it does not implement the compiler or MCP server.

The [lookup guidance](https://github.com/on-the-ground/unison-lang-pack/blob/f7975894e082e8e2dd15de5cd4e13eab9d90ce5a/knowledge/example-lookup.md)
starts with the target project's installed dependencies and focused read-only
queries. It distinguishes browsing examples from installing libraries. This
addresses incorrect symbol/API guesses as well as syntax unfamiliarity.

## MCP connects to UCM's actual checker

Inspected Unison revision: `a1652e3ada28924cb9e75ff1d62408ee8df6b78f`.

- [Official MCP setup](https://github.com/unisonweb/unison/blob/a1652e3ada28924cb9e75ff1d62408ee8df6b78f/docs/mcp.md)
  exposes UCM as an Agent server, including an independent `ucm mcp` process.
  Code/library search and language guidance accompany writing and checking.
- [Tool implementation](https://github.com/unisonweb/unison/blob/a1652e3ada28924cb9e75ff1d62408ee8df6b78f/unison-cli/src/Unison/MCP/Tools.hs)
  routes `typecheck-code` through the existing UCM input machinery in an explicit
  project/branch context. It loads scratch source without adding/updating named
  definitions. Watch expressions can be evaluated, so this is not literally
  computation-free. Update, run and test tools have separate roles.
- [Arguments and tool names](https://github.com/unisonweb/unison/blob/a1652e3ada28924cb9e75ff1d62408ee8df6b78f/unison-cli/src/Unison/MCP/Types.hs)
  identify source text or an absolute file path and the project context. The
  interface can resolve names against real installed definitions and libraries;
  a grammar-only checker cannot supply that information.
- [MCP transcript](https://github.com/unisonweb/unison/blob/a1652e3ada28924cb9e75ff1d62408ee8df6b78f/unison-src/transcripts/idempotent/mcp.md)
  shows a JSON-encoded text result with message lists and output fields. This
  does **not** establish a uniform code/range/fix record for every diagnostic.
- [LSP diagnostics](https://github.com/unisonweb/unison/blob/a1652e3ada28924cb9e75ff1d62408ee8df6b78f/unison-cli/src/Unison/LSP/Diagnostics.hs)
  carry ranges, severity, messages and related locations; diagnostic codes are
  absent in this inspected constructor. LSP and MCP are separate frontends,
  rather than MCP being a wrapper around the LSP wire protocol.
- [MCP prompt](https://github.com/unisonweb/unison/blob/a1652e3ada28924cb9e75ff1d62408ee8df6b78f/unison-cli/src/Unison/MCP/Prompts.hs)
  combines language guidance with a direction to typecheck and inspect real
  definitions. The feedback loop complements prompting.

## Implication for Subsea Cable

Keep few-shot authoring demonstrations in the pack and verify their sources.
Use the actual Vessel validator for semantics and name resolution through its
supported Codebase-facing surface; do not build a second semantic implementation
inside this pack. An Agent-first MCP validation operation is useful without a
full editor LSP. Both could later project the same diagnostic service.

Unison's practical pattern supports this separation. It does not prove that
Subsea requires Unison's type system, that grammar alone is enough, or that
effectful dry-run/impact inspection is already implemented. See
[the diagnostic recommendation](DIAGNOSTICS.md) for scope and limits.
