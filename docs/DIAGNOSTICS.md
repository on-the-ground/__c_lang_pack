# Voyage diagnosis: scope and recommendation

Status: design recommendation, not an implemented MCP API, LSP server or new
language contract. Based on [Unison research](UNISON_RESEARCH.md), the pinned
public grammar/corpus, and the static checks used for this pack.

**Grammar is necessary but insufficient for an Agent's full feedback loop.**
g4 is an executable syntax input and EBNF explains the same syntax; both need
the maintained lexical preprocessing. Neither provides Codebase context, Goal
arity/multiplicity reasoning, Host binding verification or live revision impact.
A source can parse and still discard a Value the author intended to forward.

| Layer | What checks it | Scope now |
| --- | --- | --- |
| UTF-8, preprocessing, parsing | pinned g4 + preprocessing | local syntax-only JSON checker in this repository |
| root, arity, missing Goals, multiplicity, guarded recursion | existing Vessel source validator | external static checker; general MCP integration is follow-up |
| likely intent traps such as discarded routing | AST/dataflow analysis | future warnings; never redefine valid syntax as an error |
| actual Anchor presence/signature | declared Host registry/profile | report unavailable unless a supported binding check exists |
| interpreted stages, input/output counts and routing | the same semantic analysis result | proposed static explanation, not execution evidence |
| effect-free dry-run | explicit mocks and execution profile | future separate capability; grammar validation must never invoke Anchors |
| live revision impact | authorized live frontier and committed evidence | Runtime integration, not inferable from a file alone |

## First useful integration

Recommend an MCP validation tool over the **existing** Vessel validator and
Codebase-facing interface, coordinated with its M0/U1 work. The knowledge pack
should tell an Agent to discover that server's real schema and iterate on actual
diagnostics. It should not fabricate portable tool names or silently publish/
rebind source while checking it. Full LSP completion/hover/editor transport is
optional later; Agent usefulness does not depend on building all of LSP first.

Propose, for review, one diagnostic model shared by CLI/MCP and any future LSP:
phase, severity, stable code, message, original-source range, related locations,
and optional fix edits. Include source digest, language/validator revisions,
resolution context, and explicitly checked/unavailable capabilities. Never claim
semantic/Host checks passed because they were skipped. Positions should declare
units; the local prototype uses one-based lines and zero-based Unicode code-point
columns, while a future LSP adapter must convert to its negotiated encoding.

Fix edits must be based on the analyzed source digest. Warnings about intention
need an explanation and alternative, not an automatic semantic rewrite. A Host
registry snapshot or mutable Codebase context must be identified explicitly;
unqualified references remain symbolic until actual occurrence demand. Static
checking stores no deduction record and selects no future live artifact.

## What is provided here

`scripts/check_examples.py` generates the parser from a hash-verified public
snapshot and checks 48 syntax corpus cases plus four pack examples. It emits
JSON syntax diagnostics with locations and flags semantic/Host/execution checks
as unavailable. `--source path.vyg` checks an individual file. Syntax-only success
does not mean a valid or runnable Voyage Plan. This is packaging/conformance
tooling, not a new MCP service or a second Runtime implementation.

Few-shot pairs demonstrate explicit routing, visible worker classification and
guarded recursion. They can improve the prompt's concrete guidance, but no
improvement is asserted without held-out Agent experiments. Structured feedback
is complementary. Prioritize it over a complete editor stack when real U1 work
exposes repeated authoring failures; richer interpretation/dry-run/impact tools
should follow supported capabilities and observed demand.
