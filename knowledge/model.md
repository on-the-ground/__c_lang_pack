# Mental model

Status: informative authoring summary. Sources: `pack.json` → `module_sources`.

A user states a goal in natural language. An Agent authors a **Voyage Plan**:
explicit dependencies and routing in `.vyg` source. The **Subsea Cable Runtime**
realizes that structure. **Vessel** is its control plane; the live **Cable** is
its data plane. A **Host** performs genuine leaf computation: functions, tools,
APIs, or a worker LLM session. Do not label Vessel alone the complete Runtime.

An orchestrator LLM can design and revise the plan while worker LLMs perform
leaf tasks. Both LLMs may be non-deterministic. The authored structural rules
make dependency, routing, and definition selection explicit; they do not make
LLM judgments correct or deterministic. Keep orchestration in Goals rather than
hiding the entire workflow behind one `$doEverything` operation.

A **Goal** describes structural work. It is not a synchronous scalar function.
A **reduction** is the structural rule in a definition; a **deduction** commits
that rule's application to a particular occurrence. **Touchdown** is grounded
leaf work. A selected named definition and the resulting structure are evidence
of how a leaf became part of the plan, not evidence that its tool result is true.

Unqualified `Name/Arity` references remain revisable until their exact occurrence
is demanded. An Agent or authorized operator authors a new definition and
rebinds the alias. Already committed selections stay fixed. Merely parsing,
storing, or resolving a parent does not select all its child Goal definitions.
A pinned `Name#hashPrefix` stays pinned under the implementation's identity
profile. Keep names, immutable artifacts, occurrences, and attempts distinct.

A source unit declares `root Name/inputArity`; it carries no input. The caller
lays a Cable for a target, sends complete input tuples, and observes Values plus
one `EndOfResult` for each admitted input. Decommission closes admission; drainage
then leads to `EndOfStream`. Terminals are controls, not ordinary user Values.
A completed plan does not by itself establish durable recovery or exactly-once
effects.

Public authoring guides explain observable behavior. Grammar checks recognize
source syntax; they do not certify a Runtime. Select an implementation by its
pinned revision, profiles, supported capabilities, and actual feedback.
