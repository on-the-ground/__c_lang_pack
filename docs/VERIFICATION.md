# Initial independent-pack verification

Date: 2026-10-13 (Asia/Seoul). These are preparation checks, not live Agent or
Runtime execution evidence.

- Language source pin: `83a897276b0d50a240530b363101dc64cdc42c30`.
- Content version: 0.1.0, unreleased initial proposal.
- The 61 declared public-source files were imported from that immutable revision
  through an authorized checkout, with every SHA-256 verified. CI uses only the
  local public snapshot; it requires no private language-repository credentials.
- The pack contains 18 allowlisted public files. Knowledge modules, two original
  examples, two new few-shot answers and three demonstration pairs are included.
  Build/validate pass; eight package regression tests cover deterministic bytes,
  tampering, missing/extra files, paths/symlinks, source fingerprint drift,
  missing demonstration answers, and nonpublic payload references.
- Compact context: 8,304 bytes under the 18,000-byte budget.
- Archive SHA-256:
  `d5a0ff6d7da3149fb1794b0132858093da47f4dbdcfa291645004893dc417809`.
- ANTLR 4.13.2/Python runtime 4.13.2 with Java 21 accepts four complete pack
  examples. All 48 public corpus syntax expectations match. The grammar's
  required preprocessing is applied; validation-phase corpus cases may parse
  successfully and remain semantically invalid.
- Individual-file CLI checks distinguish a parsed `ArityMismatch` source from
  semantic verification, reject invalid UTF-8 before lexing, and return syntax
  errors at original-source Unicode code-point locations with nonzero exit codes.
- External Vessel static checker at
  `ead5436aa3908102e126c5045cd700b625325812` accepts all four source units:
  ReviewRequest (4 Goals), CountDown (2), FetchAndLabel (3), ResolveIncident (4).
  These checks do not invoke Host Anchors or verify binding registries.

Reproduction commands are in [maintenance](MAINTAINING.md). The repository's CI
repeats packaging, grammar/corpus and diagnostic CLI checks and attaches the
generated distribution for review. Static correctness does not measure the
few-shot prompting effect. Actual model/tool context, held-out task outcomes,
general Plan validation/execution/rebind feedback and production default-loading
remain later integration evidence.
