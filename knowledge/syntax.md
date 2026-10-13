# Source forms

Status: informative authoring summary. Sources: `pack.json` → `module_sources`.

Use **Subsea Cable**, `.vyg`, and portable language ID `subsea-cable`. `__C` is a
visual mark, not a code identifier. Names are case-sensitive. Ignoring leading
underscores, the first ASCII letter distinguishes uppercase Goals from lowercase
Values/Maps. Strings may contain Unicode. Statements use meaningful newlines;
`//` and `/* ... */` are comments. The grammar requires the lexical preprocessing
documented in the public conformance guide; a raw ANTLR lexer is insufficient.

Exactly one default root appears in each source unit:

```subsea
root CountDown/1
CountDown = [n] -1> [n <= 0, {true: Finish[n], false: CountDown[n - 1]}]
Finish = (n) -> n
```

Square brackets define structural parameters. Parentheses define a function
leaf, always producing one Value. Structural named definitions may declare
`-0>`, `-1>`, or `-N>` for zero, one, or zero-or-more outward Values. Plain `->`
requires a uniquely inferable multiplicity; it is not a default `/1`. Explicit
multiplicity is a checked contract, not permission to contradict known outputs.
Only named structural definitions have multiplicity arrows; inline stages and
function definitions use `->`.

`Goal[args]` is deferred structural work; `Goal(args)` requests eager demand.
Both are structural occurrences, not ordinary scalar calls. `$anchor(args)`
invokes a Host operation. Keep Goal and Anchor work directly in structural
bodies, stages, or branches. Primitive expressions such as `Next[x + 1]` create
no additional occurrence and remain valid. Exact arithmetic follows the Host
profile.

Serial `[A[x], B]` routes each Value to bare `B` as its one argument. Written
arguments are not extended by routing. Use `[r] -> B[r, y]` to forward a result
alongside another argument. Unkeyed `{A[x], B[x]}` is independent work with no
outward Value. Keyed `{left: A[x], right: B[x]}` joins exactly one Value from each
branch into one Map. Destructure that Map explicitly before further work.

An effect-free selector followed by a keyed branch map selects one structure:
`[flag, {true: Yes[x], false: No[x]}]`. Perform tool calls or LLM judgments in
preceding leaves and route their Values into the selector. Recursion needs a
guarded exit; valid source recursion still may not terminate for some inputs.

Lowercase `map[key]` is lookup; uppercase `Goal[args]` is work. A named Map can
contain structures whose Goal references remain symbolic until needed.
`@policy(args)` annotates a structural occurrence, but its spelling does not
establish portable retry or timeout semantics. Use supported profiles.
