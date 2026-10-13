---
name: subsea-cable-lang-pack
description: Author, explain, review, and revise Subsea Cable Voyage Plans using explicit dependencies, routed Values, and implementation feedback.
---

# Subsea Cable language pack

Use this pack when working on a `.vyg` Voyage Plan or explaining its behavior.
It is authoring knowledge, not an independent specification, Runtime, or proof
of execution. Check `pack.json` for the target language revision and source
fingerprints. Runtime support and pack version are separate.

Start with [the mental model](knowledge/model.md). Read only what the task needs:

| Task | Read next |
|---|---|
| Draft or edit source | [Syntax](knowledge/syntax.md), then [patterns](knowledge/patterns.md) |
| Learn from task/answer demonstrations | [Few-shot examples](knowledge/few-shot.md) |
| Review likely misunderstandings | [Pitfalls](knowledge/pitfalls.md) |
| Validate, run, or revise | [Workflow](knowledge/workflow.md) |
| Attach the pack to an Agent workspace | [Connections](adapters/README.md) |

The generated `subsea-cable-context.md` contains the model, pitfalls, and workflow
for hosts that accept one context attachment. Use the modules for deeper syntax
and examples. Neither attachment nor a nested clone forces an Agent to load it.

Keep the plan small and explicit. State the root input, output multiplicities,
leaf contracts, and expected result before executing. Use actual validation and
execution feedback; never infer success from a plausible explanation.

If syntax, documented meaning, and implementation feedback disagree, preserve a
small reproduction and the exact revisions; stop only the affected path and
report the discrepancy. Do not invent a language rule to make the example work.

Public guidance: [Language Reference](https://4gentsinc.github.io/subsea_cable_webpages/LANGUAGE_REFERENCE/)
and [Runtime availability](https://4gentsinc.github.io/subsea_cable_webpages/RUNTIME_STATUS/).
Those links describe the published site; the fingerprints in `pack.json` identify
the sources used for this pack, rather than promising the site is immutable.
