# Write, validate, execute, observe, revise

Status: informative authoring summary. Sources: `pack.json` → `module_sources`.

1. **Check the environment.** Read `pack.json`; compare its language revision
   with the implementation's declared revision and profiles. Discover actual
   connected tools and their schemas. Do not fabricate MCP operation names.
2. **Define the work.** State the root input tuple, expected Values, completion,
   and genuine Host leaves. Record each leaf's input/output, effects, evidence,
   and failure contract. Put dependencies and choices in Goals.
3. **Author and inspect.** Use the syntax and patterns modules. Explain what
   each stage receives and emits. Check explicit routing, arities, keyed joins,
   multiplicities, recursion exits, and referenced Goals or Host bindings.
4. **Validate.** Use the selected implementation's actual source validator when
   available. Separate syntax diagnostics from structural/semantic diagnostics
   and Host-contract checks. Preserve the input source and structured diagnostics
   the tool actually returns. A parser pass alone establishes only syntax.
5. **Execute only a supported path.** Through the declared implementation surface,
   store/publish the validated source, lay the target, and send the complete input
   tuple. These are conceptual operations, not portable MCP command spellings.
   Read actual Values and `EndOfResult`; decommission when finished and wait for
   `EndOfStream`. Report a draft as a draft when no compatible execution tool exists.
6. **Inspect evidence.** Separate authored intent, selected definitions,
   structural deductions, and Host outcomes. Use only authorized, supported
   observations. A final result does not substitute for live evidence when the
   task requires investigation before completion. Mark unavailable evidence.
7. **Revise from evidence.** Describe what assumption failed. Validate a new
   immutable Goal definition, then use the authorized alias-rebind surface.
   Record old/new identities, the reason, and the evidence used. An alias change
   affects only occurrences not yet committed to a selected definition; concurrent
   demand may already have selected the old definition. Verify observed selections
   instead of assuming every pending-looking occurrence used the new definition.

A useful handoff records source and pack revision, Runtime/Host versions and
profiles, validated source, actual diagnostics, input tuple, retained handle (if
supported), output/terminals, evidence references, and any revision identities.
Do not substitute a reconstructed story for unavailable execution evidence.

## Availability at the target revision

The published MCP demo runs only its bundled primes example with limits 1–100.
It does not execute arbitrary user Voyage Plans or expose a step-by-step trace.
General Plan validation/publication/execution and alias-rebind MCP integration
are not established by this pack. Portable live provenance queries are not an
active public contract at this revision. A separately supported experimental
profile must declare its own scope; a Draft proposal is not activated behavior.

Read the dated [availability report](https://4gentsinc.github.io/subsea_cable_webpages/RUNTIME_STATUS/)
and [demo instructions](https://4gentsinc.github.io/subsea_cable_webpages/GET_STARTED/).
Before using a newer Runtime, recheck its current capabilities and revision.
The pack provides static authoring context; actual Agent execution feedback must
still validate its usefulness with the general Plan surface when that is available.
