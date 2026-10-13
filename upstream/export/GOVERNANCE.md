# Language Governance

> **Status:** public process and documentation-status guide, not the complete
> source-repository authority map or Runtime certification baseline.

## Roles and contributions

The project maintains syntax, meaning, naming, and accepted language decisions.
External Runtime and Host projects own code, releases, security, support,
profiles, and verification. Independent implementations remain welcome;
publication scope does not revoke implementation rights.

Report findings or worked-out SCP proposals in the
[public community repository](https://github.com/4gentsInc/subsea_cable_webpages).
Source-repository developers retain their maintainer route.
[Contributing](CONTRIBUTING.md) describes public intake.

## Decision and activation

Draft and Discussion record work in progress. Owner approval authorizes scoped
integration. A decision becomes Accepted and effective only when one activation
PR synchronizes every affected canonical contract, grammar, diagnostic, example,
compatibility note, and conformance projection and is squash-merged. An intake
issue or proposal-only merge does not activate behavior.

Accepted decisions retain their effect. The [decision index](SCP.md) provides
identifiers and topics; it is not a substitute for maintained decisions or
complete semantic contracts. Report conflicts rather than selecting a reading silently.

## Documentation and compatibility

Public pages explain motivation, authoring, observable guarantees, and availability.
Usage and Runtime guides are explanatory projections, not a complete independent
implementation or certification package. Grammar downloads remain syntax
projections; source fixtures retain their expectations. Neither establishes
full Runtime conformance.

Full Runtime conformance verification is available only against the maintained
canonical baseline, which is not publicly distributed on this site. Public
syntax-tool checks can use the grammar, required preprocessing, and source
fixtures; they do not replace that baseline. Without it, describe the public
behaviors and profiles you support rather than claiming full Runtime conformance.
Questions about verification scope can be raised in the public community
repository; this page does not offer baseline access or a certification service.

Claims must name the supported revision, profile, capabilities, unsupported
features, and verification basis. Publication changes do not alter existing
syntax, semantics, component responsibilities, or effective decisions.

## Current availability

Subsea Cable is pre-1.0. [Runtime availability](RUNTIME_STATUS.md) reports dated
status. [Ecosystem](ECOSYSTEM.md) listing is not endorsement or maintenance transfer.
