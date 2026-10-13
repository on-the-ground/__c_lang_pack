# Frequent wrong assumptions

Status: informative authoring summary. Sources: `pack.json` → `module_sources`.

| Tempting interpretation | Actual authoring rule |
|---|---|
| `[A[x], B[y]]` forwards A's result | B receives only `y`; use `[A[x], [r] -> B[r, y]]` to forward it |
| `{A[x], B[x]}` returns two values | Unkeyed parallel work has no outward Value; a keyed join returns one Map |
| A keyed join collects a stream | Each branch must provide exactly one Value; `/0` or `/N` is not silently collected |
| A bare downstream Goal runs once | It runs once per upstream Value; `/0` or an empty `/N` invokes it zero times |
| `Goal(args)` returns a scalar inside another argument | It is eager structural work; expose the dependency as a stage instead |
| `root Task/1` includes input 1 | The `1` is arity; send the actual input tuple separately |
| A parent selects all child definitions | Each unqualified Goal reference is selected at that occurrence's demand |
| Updating an alias repairs executed work | Committed selections stay fixed; author new work for reassessment |
| A stored plan proves a tool ran | Structural provenance and execution evidence answer different questions |
| A reused structure means effects can be skipped | Effect reuse needs separate explicit support and evidence |
| An effect-free selector makes the LLM deterministic | It constrains structural selection; Host/LLM computations retain their own semantics |
| `@retry` establishes retry support | Annotation names are insufficient; use a declared supported policy profile |
| Parser success proves a valid, runnable plan | Arity, multiplicity, signatures, profiles, and execution require further checks |

Do not guess a missing output multiplicity as `/1`, silently take the first
stream Value, or wrap the entire orchestration in an opaque Anchor to work around
a structural validation failure. Read the source rule and actual diagnostic.
Do not promise live queries, crash recovery, hash portability, or exact replay
unless the selected implementation explicitly supports and verifies them.
