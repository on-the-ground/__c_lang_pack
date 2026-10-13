# The Subsea Cable World

> **Status:** public conceptual guide, not an internal architecture specification.

![The original Subsea Cable concept sketch](assets/subsea-cable-concept.jpg)

This original concept sketch is explanatory; the sections below define the
public terms.

## Voyage Plan

The authored `.vyg` source is a **Voyage Plan**: Goals and dependencies describing
work. It is not a trace. Open choices can remain revisable until work is selected.

## Sea and Goals

The **Sea** is Goal space. Names refer to intent; immutable artifacts identify
particular definitions. A name and a selected definition are different.

## Vessel and deduction

The **Vessel** navigates the voyage. **Reduction** is a Goal's structural rule;
**deduction** applies it to selected work and preserves committed history.
**Carousel** names the mechanism involved in one deduction. Later revisions
do not rewrite earlier committed selections.

## Cable and Touchdown

A **Cable** is realized work with Values and completion. **Touchdown** means
work has reached a concrete Host leaf. Structural records connect it to intent,
but do not prove attempts ran or effects succeeded. A completed **Fully Touchdown
Cable** and provenance describe a drained voyage under supported capabilities.

## Host, Anchors, and Scheduler

The **Host** supplies primitive and leaf computation. An **Anchor**, written
`$name(...)`, identifies an existing tool implementation. The **Scheduler**
controls eligibility and outcomes under a declared profile. Keep dependencies
in the Voyage Plan and genuine tool code in Host leaves.

See [Adoption](ADOPTION.md), [For Agents](FOR_AGENTS.md), and
[Language Reference](LANGUAGE_REFERENCE.md). Check
[Runtime availability](RUNTIME_STATUS.md) before depending on execution,
recovery, or provenance access.
