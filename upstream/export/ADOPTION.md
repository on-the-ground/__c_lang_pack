# Adopt Subsea Cable for one workflow

Subsea Cable lets you put dependency structure and revisable intent in a Voyage
Plan while keeping existing computation in your tools. Start with one task whose
plan you currently reconstruct from a transcript, function calls, or a run log.

> **Availability:** this is an integration guide, not an installable Runtime
> release. Check [Runtime availability](RUNTIME_STATUS.md) for the dated evidence.
> To see a reference plan run first, follow [Get Started](GET_STARTED.md).

## Express the work you already understand

Choose a bounded workflow: fetch an input, transform it, publish a result.

```subsea
root PublishReport/1

PublishReport = [request] -> [Fetch[request], Transform, Publish]
Fetch = [request] -1> $fetch(request)
Transform = (source) -> $normalize(source)
Publish = [report] -0> $publish(report)
```

The source declares dependencies and output counts. Your existing fetch,
normalization, and publishing implementations remain Host leaves. `Publish` has
no outward Value; a successful segment still has an explicit completion terminal.
Do not hide the whole pipeline behind one `$runWorkflow` Anchor.

Before integration, write down each leaf's accepted inputs, produced Values,
completion conditions, and possible external effects. Decide which steps depend
on one another and which are independent. Keep retry and timeout behavior in an
explicitly supported profile; annotation names alone do not define a policy.

## Divide the integration responsibility

| You author or connect | The chosen implementation must support and verify |
|---|---|
| Goal dependencies, branches, and routing | Validation and the structural semantics of the pinned revision |
| Genuine Host computations and effect boundaries | Host invocation, emission, failure, and cancellation contracts |
| Authorized revisions of future Goal definitions | Alias selection and immutable deduction records |
| Inputs and observation of results | Admission, multiplicity, backpressure, and segment/stream terminals |
| The evidence you need for review | The declared trace, voyage-result, and provenance capabilities |

The [Runtime Contract](implementation/RUNTIME_CONTRACT.md) states the obligations.
It is a reference for checking an implementation, not a requirement to build one
before you can author a Voyage Plan.

## Check an implementation before depending on it

Ask for its exact specification revision, named Host and Scheduler profiles,
supported capabilities, and a reproducible conformance result at a pinned commit.
Check that the command or adapter you will actually use exercises the validated
Runtime surface. Tests of a new library do not make a legacy CLI equivalent.

For a laid Cable, the caller lays a target, sends complete input tuples, observes
Values and one `EndOfResult` per input, and decommissions the Cable before
`EndOfStream`. Concrete API spelling belongs to the implementation.

Recovery and effects need their own checks. A structural checkpoint is not
automatically durable crash recovery. A reused structural segment does not grant
permission to repeat or skip an external effect. A published `$` leaf says where
an effect could occur; attempt and outcome evidence says what actually ran.

## Prepare now; integrate at the supported boundary

You can author and review the `.vyg` plan, inventory existing Host leaves, and
provide a small workload with expected outputs now. Choose a Runtime when its
supported surface covers that workload. If it does not yet, follow its dated
progress and provide the missing acceptance case rather than treating a
prototype as an established integration.

The [Primes Up To](conformance/PRIMES_UP_TO.md) reference uses Goal recursion and
one finite map result. Its source and expected aggregate are specified; the
clean-checkout execution gate remains open. Displaying several prime numbers
means traversing that one completed Value, not receiving a live generator.
[Runtime availability](RUNTIME_STATUS.md) records what has been completed and
what remains. The [Roadmap](ROADMAP.md) connects the next milestones to workflows
you might want to try. No release date is promised here.

For language feedback, see [Contributing](CONTRIBUTING.md). For public authoring
guidance, see the [Language Reference](LANGUAGE_REFERENCE.md).
