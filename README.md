# Subsea Cable language pack

Independent workspace knowledge for Agents authoring Subsea Cable Voyage Plans.
The pack lives here, separately from the language and Runtime repositories.
It provides an Agent Skill entry, focused knowledge modules, optional few-shot
task/answer pairs and a compact context attachment. This initial 0.1.0 is
authoring context; it does not supply a Runtime or MCP server.

## Attach it

For a skill-aware host, use its actual installation mechanism for this folder.
For workspace Agents, place the unpacked pack in `.agent-context/subsea-cable/`
and add [the instruction snippet](adapters/AGENTS.snippet.md) to the workspace's
applicable `AGENTS.md` or `CLAUDE.md`, adjusting paths and preserving existing
instructions. Merely cloning a nested folder does not load its knowledge.
When using this repository as the workspace root, `AGENTS.md` supplies that entry.

For a host that accepts one static context attachment, use the generated
`subsea-cable-context.md`; supply deeper modules/examples on demand. See
[connections](adapters/README.md). Production setup should install a pinned
pack and its instruction entry by default; this repository does not change
any Agent host's defaults itself.

Start at [SKILL.md](SKILL.md). Read the model, then only modules relevant to the
task. [Few-shot guidance](knowledge/few-shot.md) links complete answers for
explicit Value forwarding, classification followed by routing, and guarded
recursion. Demonstrations complement actual validation; they are not a measured
Agent benchmark or a substitute for feedback.

## Build and verify

With Python 3.11+:

```sh
python scripts/package.py build --output /tmp/new-empty-pack-output
python scripts/package.py validate --output /tmp/new-empty-pack-output
python scripts/test_package.py
```

The deterministic archive contains only allowlisted authoring modules, examples,
demonstration pairs, license and metadata. Maintainer docs, scripts and upstream
snapshots are not in the Agent payload. Generated release fingerprints detect
changed bytes; distribute through a trusted channel and record the archive hash.
CI attaches the generated distribution as a review artifact. A GitHub release
and production bootstrap are separate follow-up work.

For syntax checks, use Java 21, ANTLR's 4.13.2 complete jar and Python runtime
`antlr4-python3-runtime==4.13.2`:

```sh
python scripts/check_examples.py --antlr-jar /path/to/antlr-4.13.2-complete.jar
python scripts/check_examples.py --antlr-jar /path/to/antlr-4.13.2-complete.jar --source my-plan.vyg
```

The JSON checker applies the maintained lexical preprocessing and verifies 48
corpus cases plus four pack examples. It checks **syntax only** and reports
semantics/Host/execution as unchecked. Actual structural validation belongs to
the chosen Vessel implementation. The pack registers no general programming
MCP tools; discover actual capabilities and read
[Runtime availability](https://4gentsinc.github.io/subsea_cable_webpages/RUNTIME_STATUS/).

## Versions, sources and tool direction

`pack.json` independently versions the pack, pins language revision
`83a897276b0d50a240530b363101dc64cdc42c30`, and fingerprints approved public
sources. The verified snapshot permits CI without private repository access.
Its informative guides are not an independent specification. No confidential
language material or internal experiment answers are distributed.

[Maintenance](docs/MAINTAINING.md) explains reviewed source updates.
[Unison research](docs/UNISON_RESEARCH.md) examines how a knowledge pack works
with UCM's real MCP checker. [Voyage diagnosis](docs/DIAGNOSTICS.md) recommends
connecting the existing Vessel validator through MCP before building a full
editor LSP, while keeping grammar, semantics, Host checks and execution distinct.
Those richer MCP diagnostics are a recommendation, not implemented by this pack.

Licensed under Apache-2.0. Knowledge modules are original authoring summaries;
the public-source snapshot retains its existing license and provenance.
