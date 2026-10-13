# Subsea Cable conformance examples

> **Status:** public source examples and diagnostic expectations, not a complete
> Runtime certification suite or execution implementation guide. The required
> lexical preprocessing section is the maintained syntax-level contract.

[cases.tsv](cases.tsv) lists source cases by phase and diagnostic category.
The `.vyg` files help authors and syntax-tool developers. A `validation` case
can parse successfully while remaining an invalid program. Existing fixture
expectations are unchanged.

## Required lexical preprocessing

The ANTLR lexer produces physical `TERMINATOR`, whitespace, and comment tokens.
Before parsing, a token-source wrapper must perform this deterministic pass:

1. Decode the source strictly as UTF-8. Reject malformed input as
   `InvalidSourceEncoding` before lexing.
2. Discard ordinary whitespace and line-comment tokens. The newline following a
   line comment remains a physical `TERMINATOR` token.
3. Replace each block-comment token conceptually with one whitespace boundary.
   Its internal newlines never produce terminators. Because tokenization has
   already occurred, discarding the token must not concatenate its neighbors.
4. Track unmatched opening `(`, `[`, and `{` tokens with a delimiter stack.
5. For each physical `TERMINATOR`, suppress it when the delimiter stack is not
   empty or when the previous significant token is in this exact set:

   ```text
   =  ->  -0>  -1>  -N>  ,  :  @  $
   ||  &&  ==  !=  <=  >=  <  >
   +  -  *  /  %  !
   ```

6. Form named-Goal multiplicity arrows. Track the square-bracket group that
   begins a Binding right-hand side: the `[` immediately following a `=` at
   delimiter depth zero. When that group closes back to depth zero and the next
   three significant tokens are `-`, one of `0`, `1` or `N`, and `>` with no
   intervening character (the end offset of each is immediately followed by the
   start offset of the next), replace them with one `MULTIPLICITY_ARROW` token
   whose text is `-0>`, `-1>` or `-N>` and whose span covers all three. Nowhere
   else are those tokens fused, so `(base)-1>0` and `x-1>0` keep their
   subtraction and comparison, a spaced `[x] - 1 > $a` is not an arrow, a
   function-leaf definition `(params) -> body` has no multiplicity arrow, and an
   inline Goal-arrow stage has none either.
7. Form the contextual Root keyword. When the first significant token of a
   statement (the first of the file, or the first after an emitted logical
   `TERMINATOR`, at delimiter depth zero) is the Identifier `root` and the next
   significant token is an Identifier, retype it as `ROOT`. After `ROOT`, an
   Identifier, an optional `HASH_QUALIFIER`, and `/`, retype a `NUMBER` with no
   fractional part as `ROOT_ARITY`. Every other token is left unchanged, so
   `root = 5` stays a Binding while `root A[5]`, `root A/1.0`, and `start A/1`
   reach the parser as SyntaxErrors.
8. Coalesce consecutive surviving physical newlines into one logical
   `TERMINATOR`, preserving the span of the coalesced source region.
9. Emit all other significant tokens unchanged and finally emit EOF. The parser,
   not this pass, reports unmatched or misordered delimiters.

The “previous significant token” ignores whitespace and comments. A newline
before an operator is not continuation; only a newline after a listed token is.

## What the examples cover

- Core source forms, continuation, Strings, and root declarations.
- Structural call placement, arity, and named results.
- Conditional recursion and output counts.
- Explicit diagnostic categories for invalid authoring.

[ANTLR](../SubseaCable.g4) and [EBNF](../SubseaCable.ebnf) describe syntax;
they do not establish complete processing or Runtime compatibility. These
examples do not certify execution, alias races, recovery, policies, or effects.
Claims need a supported revision, profile, and corresponding verification basis.

## Evaluate your workflow

[Deduction](DEDUCTION.md) explains revision guarantees; [Policy](POLICY.md)
describes profile expectations; [Laid Cable](LAID_CABLE.md) describes inputs and
terminals. [Primes Up To](PRIMES_UP_TO.md) illustrates Goal recursion and one
finite aggregate result; its source and expected results are specified, and
a public demo runs it through an Agent ([Get Started](../GET_STARTED.md)).
See [Governance](../GOVERNANCE.md) and the
[Runtime Contract](../implementation/RUNTIME_CONTRACT.md). Report discrepancies
through [Contributing](../CONTRIBUTING.md).
