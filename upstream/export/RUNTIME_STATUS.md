# Runtime availability

> **Last checked:** 2026-10-11 (Asia/Seoul).
> This is a dated availability report, not language authority or a release promise.

Subsea Cable is an evolving pre-1.0 specification. There is no designated
official Runtime or publicly available production release. An implementation
prototype is being tested; its progress does not establish a supported package
that an adopter can install today.

You can run one reference example through an Agent today. A public demo image
contains the prototype and a WebAssembly Host. [Get Started](GET_STARTED.md)
connects it in a few steps.

## Capabilities and availability

| Capability | Status | What an adopter can rely on now |
|---|---|---|
| Voyage Plan authoring, syntax, and reference examples | Available | Read the language reference and prepare a workflow |
| Parsing, structural deduction, routed results, and segment completion | In progress | Exercised in controlled prototype tests; no supported public release |
| A reproducible end-to-end execution demo | Available as a demo | The [primes example](conformance/PRIMES_UP_TO.md) runs through an Agent with the public image; see [Get Started](GET_STARTED.md). Only that example, with limits 1–100 |
| Agent-authored revision and replanning demonstration | In progress | A distinct acceptance scenario; the execution demo alone will not establish it |
| Installable Runtime and supported Host integrations | Not available | The demo image runs only its bundled example and Host; it is not a Runtime package |
| Durable recovery, exact replay, and complete incremental reuse | Not established | No deployment support claim is made |
| Portable live provenance queries | Not supported by the current contract | Do not depend on live leaf-ancestry queries without an explicitly supported extension |

No release date is promised. Further public commands, traces, supported
versions, and reproducible evidence will be linked when those artifacts are
available.

## Next user capabilities

The [Roadmap](ROADMAP.md) describes the runnable execution, tool integration,
Agent investigation and future-plan revision milestones. Runtime foundations
have completed work records and controlled prototype evidence. The execution
demo now runs with a real WebAssembly Host through an Agent. Live inspection
and the actual Agent revision demonstration are not yet established. No
supported public Runtime package is available.

## Finite reference execution scenario

[Primes Up To by Trial Division](conformance/PRIMES_UP_TO.md) supplies the revised
Voyage Plan and expected finite aggregate. Candidate progression and divisor
recursion remain Goal structure. Ordinary leaves return values; a
[keyed result map](LANGUAGE_REFERENCE.md#independent-work-and-named-results) joins
one Value per branch, retaining each candidate's head and the recursive remainder.

| Input | Runtime result | Displayed prime numbers | Completion |
|---|---|---|---|
| `1` | one Value: `{}` | none | one successful `EndOfResult` |
| `2` | one Value: `{head: {prime: 2}, rest: {}}` | `2` | one successful `EndOfResult` |
| `30` | one complete map with 29 candidate nodes | `2, 3, 5, 7, 11, 13, 17, 19, 23, 29` | one successful `EndOfResult` |

The displayed numbers come from walking the completed map, not separate Runtime
Values. These keyed result maps wait for their children; the remainder is not a lazy tail
or live generator. After decommission and complete drainage, the scenario
requires one `EndOfStream` and the completed Cable result.

The public demo image produces these results through an Agent; see
[Get Started](GET_STARTED.md). It runs this example only and does not
establish general Host integration or a supported Runtime.

## Prepare for adoption

Use the [adoption guide](ADOPTION.md) to describe one workflow and its genuine
Host leaves. Record expected Values, effect boundaries, and failure cases. Check
the [ecosystem](ECOSYSTEM.md) for a supported implementation before depending on
execution, recovery, or provenance features.
