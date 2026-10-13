# Few-shot authoring demonstrations

Status: optional prompting examples, not model training or measured improvement.
Sources: `pack.json` → `module_sources`. Exact task/answer pairs are recorded in
`evals/few-shot.json`; answers are complete `.vyg` files, not executable traces.

For a new task, read one or two relevant pairs after the mental model and before
drafting. Keep the examples' request, source answer, leaf contract and routing
explanation together. Adapt the structure to the new task; do not copy Anchor
names as if every Host provides them. Then use actual validation feedback.
These demonstrations must not serve as held-out evaluation cases.

## Forward a result with a second argument

Request: read an item, then return its fetched Value with a caller-supplied label.
Answer: [forward-with-label.vyg](../examples/forward-with-label.vyg).

`Fetch/1/1` calls one genuine `$fetch` leaf. The inline `[value] ->` binds its
returned Value and explicitly passes both `value` and `label` to `Label/2/1`.
Writing `[Fetch[item], Label[label]]` does not forward the fetched Value and
also violates this answer's Label arity. A well-formed explicit-argument call
can still discard an upstream result; parse success does not establish intent.

The Host contract is `$fetch(item) -> one Value`, and `Label` is a pure Map
constructor. No actual fetch is demonstrated here.

## Turn worker judgment into visible routing

Request: classify an incident, retry a flaky test or patch a real defect, and
preserve the classification evidence in the selected action's inputs.
Answer: [classify-then-act.vyg](../examples/classify-then-act.vyg).

The classification leaf returns one Map with `cause` (`"flaky"` or `"real"`)
and `evidence`. Destructuring binds both Values before an effect-free selector
chooses an action. Each action Anchor returns one report Value. The Host must
enforce that enum/shape contract; this Plan supplies no fallback for unknown keys.
LLM classification may be non-deterministic. This example does not require every
LLM leaf to make exactly one judgment.

Selecting one already-written action is execution, not a new plan. If evidence
requires an additional diagnostic dependency, the orchestrator must author and
validate a revised Goal and rebind it for undeduced occurrences. An earlier
committed judgment is reassessed by new work, never by rewriting history.

## Make the recursive exit explicit

Request: decrement a nonnegative integer until zero, then return it.
Answer: [guarded-countdown.vyg](../examples/guarded-countdown.vyg).

The selector chooses the `Finish` exit at `n <= 0`; only the other branch
creates a fresh `CountDown` occurrence. A chosen arithmetic/function Host
profile is required. Definition recursion is not an instruction to unroll all
future work in advance.

Compare an Agent draft with these routing and leaf contracts, then report the
real syntax/structural diagnostics and availability limits. A plausible prose
explanation is not a substitute for those checks or for execution evidence.
