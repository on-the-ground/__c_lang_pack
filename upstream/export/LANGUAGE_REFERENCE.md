# Subsea Cable Language Reference

> **Status:** public authoring guide and explanatory projection. This is not
> the complete semantic or Runtime conformance baseline. Check your selected
> implementation's language revision and profile. See [Governance](GOVERNANCE.md).

A `.vyg` Voyage Plan describes dependencies and routing. Host leaves provide
computation; a Runtime realizes the work. Start with [Adoption](ADOPTION.md)
and check [Runtime availability](RUNTIME_STATUS.md).

## Source and names

Source is UTF-8. Names use ASCII letters, digits, and underscores and are
case-sensitive. Leading underscores are ignored; the first ASCII letter decides
the role, so `Build` and `_Build` name Goals while `cache` and `_cache` name
values or Maps. A name containing no letter cannot be followed by `[...]`.
String values may contain Unicode. Statements use meaningful newlines rather
than semicolons. Composition can span lines inside delimiters. Comments use
`//` and `/* ... */`.

```subsea
threshold = 10
root Report/1
Report = [request] -1> $report(request, threshold)
```

Each source unit has exactly one `root Name/inputArity`, naming its default
target. The declaration carries no input Values; `/inputArity` states only how
many inputs the target accepts. The caller sends inputs to the live Cable.
`Name#hashPrefix` pins an artifact under the implementation's declared identity
profile.

Later examples are fragments unless they show a `root` declaration. A
self-contained example defines every Goal it references; a Voyage Plan may also
reference Goals that another source unit already stored in the Codebase.

## Goal arrows and function arrows

```subsea
Fetch = [request] -1> $fetch(request)
Normalize = (source) -> $normalize(source)
Process = [request] -> [Fetch[request], Normalize]
```

Square-bracket parameters define structural work; parenthesized parameters
implement one function leaf. `$name(...)` identifies a Host operation. A function
leaf produces one Value. Keep dependencies in structural stages, rather than
nesting Goal or tool calls inside arguments. Primitive expressions such as
`Next[x + 1]` remain usable.

## Deferred and eager Goal references

`Goal[arguments]` is deferred: the referenced work is selected when needed.
`Goal(arguments)` is eager: it requests that work immediately when the containing
structure is demanded. The suffix changes demand timing, not the Goal's reduction
rule. Both forms remain direct structural work, not ordinary synchronous scalar
calls. They may be a complete structural body, serial or parallel stage, or
keyed result branch; do not hide either form in another argument or expression.

## Serial routing

`[Read[input], Normalize, Save]` routes Values through stages. A bare
downstream Goal, such as `Normalize` or `Save`, receives each upstream Value as
its sole argument. A bare first stage receives no argument. Written arguments
are never extended with an upstream Value: in `[A[x], B[y]]`, `B` runs after
`A` with only `y`, and `A`'s result is discarded. Forward it explicitly with a
Goal-arrow stage:

```subsea
Forward = [x, y] -> [A[x], [result] -> B[result, y]]
```

A Goal describes structural work, not a synchronous scalar function.

## Independent work and named results

```subsea
Inspect = [issue] -> {ReadCode[issue], ReadLogs[issue]}
Evidence = [issue] -> {code: ReadCode[issue], logs: ReadLogs[issue]}
ReadCode = [issue] -1> $readCode(issue)
ReadLogs = [issue] -1> $readLogs(issue)
```

Unkeyed braces describe independent work with no outward Value. A keyed result
joins one Value per branch into a Map. A zero-output or streaming branch cannot
silently be collected as one Value. A routed Map can be destructured explicitly:

```subsea
Review = [issue] -> [
    [] -> {code: ReadCode[issue], logs: ReadLogs[issue]},
    [{code, logs}] -> Diagnose[code, logs],
]
Diagnose = [code, logs] -1> $diagnose(code, logs)
```

## Conditional structure and recursion

```subsea
CountDown = [n] -1> [n <= 0, {true: Finish[n], false: CountDown[n - 1]}]
Finish = (n) -> n
```

An effect-free selector chooses one structural branch. Unselected work does not
run. A selected recursive step is fresh work; recursive source definitions do
not imply a cyclic realized Cable. Recursion needs a guarded exit.
See [Guarded Conditional Recursion](Recursion.md).

## Values and Maps

Values include Booleans, Numbers, Strings, and Maps. Arithmetic and conversions
follow the Host profile. Unicode String contents are exact; tools must not
silently normalize them. Lowercase `map[key]` is lookup; uppercase
`Goal[arguments]` is structural work.

```subsea
labels = {true: "ready", false: "waiting"}
Pick = (flag) -> labels[flag]
```

Maps can also select structures whose Goal references remain revisable until
needed. Check supported source validation in the chosen implementation.

## Output multiplicity

| Declaration | Outward Values |
|---|---|
| `[params] -0> body` | none |
| `[params] -1> body` | exactly one |
| `[params] -N> body` | zero or more |
| `[params] -> body` | inferred from structure |
| `(params) -> expression` | exactly one |

A named structural definition using plain `->` needs a uniquely inferable
output count. Opaque Anchor output, an underdetermined recursive signature,
or an unknown branch or external Goal signature can prevent inference; validation
then reports `OutputMultiplicityCannotBeInferred`. Declare `-0>`, `-1>`, or
`-N>` on that named structural definition. An explicit declaration is checked,
not an override of a provably different output count.

A downstream Goal receives one invocation per upstream Value. `/0` and an
empty `/N` cause zero downstream invocations and can complete successfully.
Do not assume an implicit first Value or collection of the stream.

## Revisions and identity

Unqualified Goal references select a definition when their work is needed.
Authorized revisions may affect later work; committed selections remain fixed.
Pinned references remain pinned. Names, artifacts, occurrences, and execution
are distinct; a familiar name does not prove the same definition or effect.
Cross-implementation hashes, replay, and reuse need explicitly supported profiles.

## Policies and Host integration

`@policy(arguments)` annotates the following structural occurrence. Names alone
do not create portable retry, timeout, delivery, or cancellation behavior.
Use declared profiles; unsupported behavior must be rejected explicitly.
Scheduling policies and policies for one Host invocation have different
responsibilities. Do not assume implicit policy inheritance.

Host leaves need input, output, completion, failure, and effect contracts.
[For Agents](FOR_AGENTS.md) shows a bounded integration example.

## Inputs, results, and diagnostics

Lay a target and send a complete input tuple. Each accepted input has an
`EndOfResult`; closing admission and draining work leads to `EndOfStream`.
These controls are separate from user Values. Completion does not establish
durable recovery or exactly-once effects.

Syntax errors, invalid structural contexts, arity errors, unsupported policies,
and output-count violations require explicit reporting. Public
[source examples](conformance/README.md) retain their expected categories.
Parsing them does not certify a Runtime.

## Grammar downloads

[ANTLR](SubseaCable.g4), [EBNF](SubseaCable.ebnf), and the
[required lexical preprocessing](conformance/README.md#required-lexical-preprocessing)
describe source recognition, not the complete Runtime execution contract. Compatibility needs
a declared revision, profile, and corresponding verification evidence.
