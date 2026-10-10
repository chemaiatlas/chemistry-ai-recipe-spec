# RFC 0001: Scope, Interoperability and Governance

**Status:** Open for discussion

## Motivation

Establish a vendor-neutral chemistry-aware recipe manifest without duplicating general workflow languages.

## Proposed decisions

1. Separate task semantics from execution adapters.
2. Require scientific limitations and security declarations even for descriptive recipes.
3. Keep the specification and validation tools usable without ChemAI Atlas.
4. Distinguish schema conformance from execution and scientific review.

## 16. Open RFC Questions

1. Does **CARS** conflict with existing names or acronyms? Would `ChemRecipe` be clearer?
2. Should `id` be a URI, DOI, or URN, and how should persistent resolution work?
3. Which JSON Schema draft should be normative, and what are the YAML/JSON and canonicalization rules?
4. Which existing chemistry data-type and units vocabularies should be reused?
5. What minimum fields describe model applicability, confidence, and scientific evidence?
6. Should a recipe, a run instance, and an execution result be distinct objects?
7. Can multiple adapters and fallback execution paths be declared?
8. How are third-party review assertions signed, revoked, and expired?
9. What version-compatibility and deprecation policies should apply?
10. How can governance, contributions, and branding remain neutral?

## How to comment

Open an issue with a concrete example, trade-off, and proposed text change.
