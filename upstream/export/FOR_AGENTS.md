# For Agents: keep intent attached to your workflow

You plan, act, inspect the result, and revise. When the plan lives only in a
transcript, an interruption or an unexpected result makes you reconstruct both
what you meant and what happened. Subsea Cable gives the plan an explicit Goal
structure and records the deductions that realize it.

This language is general-purpose. For an Agent, its immediate value is a
workflow you can inspect and revise without rewriting its committed past.

## The value for your own work

- **Keep the plan explicit.** A `.vyg` Voyage Plan names dependencies, routes
  Values, and exposes conditional choices instead of hiding orchestration in a
  tool implementation.
- **Keep future decisions open.** A Goal reference is observed when its exact
  occurrence is demanded. An authorized author can publish a revised definition
  for later-demanded occurrences while preserving committed selections.
- **Keep the reason for each leaf.** Deduction records join selected artifacts
  and lineages to realized structure. A Runtime supporting voyage results can
  provide the provenance needed to examine a drained voyage.
- **Keep existing tools.** Genuine computation stays in Host leaves. You author
  dependencies and routing; you do not need to turn your tools into one language.

These are contract capabilities, not a claim that every implementation supports
crash recovery, live provenance queries, or effect reuse. Check
[Runtime availability](RUNTIME_STATUS.md) before depending on them.

## Start with one bounded task

Here is a plan for fixing one failing test:

```subsea
root FixFailingTest/1

FixFailingTest = [issue] -1> [
    [] -> {code: ReadCode[issue], logs: ReadLogs[issue]},
    [{code, logs}] -> Diagnose[code, logs],
    Patch,
    Verify,
]

ReadCode = [issue] -1> $readCode(issue)
ReadLogs = [issue] -1> $readLogs(issue)
Diagnose = [code, logs] -1> $diagnoseWithLLM(code, logs)
Patch = [diagnosis] -1> $patch(diagnosis)
Verify = [patch] -1> $verify(patch)
```

Reading code and logs has no dependency between the two branches. Diagnosis
needs both named results; patching needs the diagnosis; verification needs the
patch. The Host resolves those genuine leaf implementations. Define each leaf's
input, output, completion, and effect contract before connecting real tools.

The plan itself does not guarantee that a patch is safe or a test is sufficient.
Those judgments belong to the author and the leaf contracts. Source validation
finds structural mistakes; it cannot inspect an opaque Anchor implementation.

## Revise a plan without erasing evidence

Only the selected branch contributes work. An authorized author may revise
future Goal definitions; already committed selections remain fixed. If the work
to change is already committed, author a new voyage. Supported structural reuse
does not imply an effect can safely be skipped or repeated.

[Why Subsea Cable](WHY_SUBSEA.md#2-what-this-makes-possible-replanning-after-an-unexpected-failure)
explains bounded replanning from completed result evidence. Live ancestry
queries and durable recovery require explicit implementation support.

## Keep your integration focused

| Your responsibility | Verify in the selected implementation |
|---|---|
| Author Goals, branches, and explicit routing | Source validation and the pinned language semantics |
| Connect existing tools as genuine leaves | Host signatures, Values, failures, and cancellation |
| Author authorized Goal revisions | Consistent alias observation and immutable history |
| Observe inputs and results | Segment admission, output multiplicity, and explicit terminals |
| Request evidence for decisions | Declared trace and provenance capabilities |

A small parser or a happy-path runner does not establish these guarantees when
alias changes, streaming, cancellation, and failure interact. The
[Runtime Contract](implementation/RUNTIME_CONTRACT.md) lets you evaluate support;
its maintainers own the execution and conformance work. Start with the
[adoption guide](ADOPTION.md) and [Runtime availability](RUNTIME_STATUS.md).

<span id="6-what-is-not-done-yet"></span>

## What is available and what is still open

The structural semantics, guarded recursion, policy addressee rules, and
Runtime responsibilities are specified. Availability is narrower than the
specification: an implementation prototype is being tested. You can run the
primes reference example through your Agent ([Get Started](GET_STARTED.md));
the separate Agent-authored revision scenario remains in progress as of the
date in [Runtime availability](RUNTIME_STATUS.md).

Concrete retry, timeout, delivery, and regression-policy meanings require a
declared profile; do not infer support from an annotation name. Portable live
provenance queries are an open item listed in
[Why Subsea Cable](WHY_SUBSEA.md#7-open-problems); lineage segments identify
Goals by `Name/Arity`, not by hash, as described in
[Joined records](WHY_SUBSEA.md#13-joined-one-record-answers-several-questions).
Exact identity, hash-encoding interoperability, and recovery support also depend
on explicitly identified implementation capabilities. If you lose a Cable handle
while the Cable is still retained, an authorized operator session can list and
describe your Cables to recover the same handle without changing the run.

## Choose the next step

| Your goal | Read |
|---|---|
| Understand the problem and value | [Overview](README.md), then [Why Subsea Cable](WHY_SUBSEA.md) |
| See a plan run | [Get Started](GET_STARTED.md) |
| Prepare one workflow | [Adoption guide](ADOPTION.md) |
| Decide whether execution support is ready | [Runtime availability](RUNTIME_STATUS.md) |
| Check public authoring and syntax | [Language Reference](LANGUAGE_REFERENCE.md), [ANTLR](SubseaCable.g4), and [EBNF](SubseaCable.ebnf) |
| Review observable obligations | [Runtime Contract](implementation/RUNTIME_CONTRACT.md) and [conformance](conformance/README.md) |
| Report a gap or contribute evidence | [Contributing](CONTRIBUTING.md) and [Governance](GOVERNANCE.md) |

These pages are public usage and observable-behavior guides, not the complete
Runtime conformance baseline. Check declared implementation support and use
the public contribution guide to submit findings and proposals.

You can begin by committing a small, reviewable Voyage Plan and inventorying the
Host leaves it needs. Keep the workflow's intent in Goals and choose execution
support by demonstrated guarantees.
