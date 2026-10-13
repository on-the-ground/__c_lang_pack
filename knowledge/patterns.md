# Authoring patterns

Status: informative authoring summary. Sources: `pack.json` → `module_sources`.

## Independent evidence, explicit routing

[review-request.vyg](../examples/review-request.vyg) is a complete source unit:

```subsea
root ReviewRequest/1
ReviewRequest = [request] -1> [
    [] -> {source: ReadSource[request], rules: ReadRules[request]},
    [{source, rules}] -> Assess[source, rules],
]
ReadSource = [request] -1> $readSource(request)
ReadRules = [request] -1> $readRules(request)
Assess = [source, rules] -1> $assess(source, rules)
```

The two reads are independent; assessment waits for their keyed result. The
Host might run assessment in a separate worker LLM session. Document its input,
output, sources, uncertainty, and effects before connecting it. For example,
`$assess` could return `{meetsRule: true, evidence: "source and rule excerpts"}`
as its one Value. This shape is a leaf contract chosen by the application,
not a new built-in language type or assurance that the judgment is accurate.

A worker performs the bounded leaf task. The orchestrator keeps the overall
plan and chooses whether the returned evidence requires a new Goal definition.
A transcript from a worker is not automatically a deduction record. Preserve
worker evidence in the returned Value or the declared external evidence store.

## Existing branch versus new plan

[guarded-countdown.vyg](../examples/guarded-countdown.vyg) demonstrates a
conditional recursive choice with a Host function returning the final number.
Following an already-authored branch is ordinary execution. **Replanning** is an
authorized author publishing a different Goal definition and rebinding its
`Name/Arity`, based on observed evidence. These are distinct actions.

If evidence shows assessment must check an additional rule, author a revised
`Assess` definition and validate it before rebinding. State which undeduced
occurrences may observe it. Already committed occurrences keep the selected
version; use new work to reassess an earlier judgment. A change to a future
alias does not undo a Host effect.

The examples are authoring fixtures, not runnable public demo commands. The
Anchor example requires an actual Host binding for all three operations.
The countdown needs a compatible arithmetic/function Host profile. Check the
chosen Runtime's support before reporting a run.
