# Schema and specification alignment

The `schema/cars-0.1.schema.json` file is an **experimental L0 subset** of the CARS 0.1 prose draft. It validates structural shape, mandatory declarations, URI syntax and a limited set of enumerations. It does **not** verify semantic dependency graphs, adapter resolvability, chemical representations, units, dependency licenses, sandbox security, execution success or scientific evidence. The sample `workflow.cwl` reference is intentionally non-executable and must be replaced before claiming CARS-Execute support.

Before a normative release: resolve extensibility policy, semantic identifiers, registry governance, unit vocabulary, adapter contract, signed provenance and compatibility guarantees.

## 2026-10-20 validation-status erratum and migration

The initial release ZIP already contained the mismatch: Specification §5.3 named
four evidence assertions, while Schema used `not_assessed`, `under_review` and
`reviewed`. The CLI delegated to that Schema. Its two original tests covered only
the `not_assessed` example and a missing top-level field, so they could not detect
this drift. No earlier design rationale for the three-value enum is present in
this source bundle; review workflow and scientific evidence had been conflated.

The corrected enum is `not_assessed`, `benchmarked`, `independently_reviewed`,
`experimentally_supported`. Meanings and evidence requirements live in §5.3.
The conformance suite directly parses that section's table and compares its
values to Schema; it also checks the top-level MUST fields and all official
example files, including the inline specification example.

Compatibility impact: manifests with `under_review` or `reviewed` that passed the
initial Schema now fail L0. `under_review` says only that a process is underway;
`reviewed` identifies neither reviewer independence nor scientific scope. Neither
has a lossless mapping, including to `not_assessed`. The CLI reports an error and
migration guidance, without rewriting the input or selecting a replacement.
Recipe owners must inspect the underlying evidence, explicitly select the
appropriate assertion, cite the assessment, and retain their original declaration
in revision history. If evidence cannot be established, do not auto-upgrade or
silently reset the claim; resolve it with the owner before revalidation. Version
any published recipe content change under the recipe's own `version` policy.

The sole bundled official recipe and its inline copy use `not_assessed` and are
unchanged. The ChemAIAtlas public-page copy also uses `not_assessed`. The separate
Desktop M0 archives have no `scientific.validation_status` declaration; they are
not additional conforming specification examples. No surveyed local recipe uses
the two legacy values. Third-party usage cannot be inferred from this local scan.

Keep `cars_version: "0.1.0"`, the Schema path and `$id` for this community-draft
erratum: it restores the original prose contract without changing the manifest
shape or evidence model. This is still a change to the accepted input set, not
full backward compatibility with the faulty Schema. Before publication, announce
this erratum, identify the corrected validator/Schema artifact by revision or
hash, and notify consumers pinning the initial Schema. Do not overwrite an
immutable published release artifact. A future field/model change needs a new
specification version; no ratified versioning/deprecation policy exists yet.

## Other alignment findings (reported, not changed)

- §5.3 lists six `result_kind` values, but input/output property definitions in
  Schema accept any nonempty string. The L0 subset does not enforce that list.
- §5.1 calls recipe `version` SemVer, but the Schema regex accepts invalid numeric
  prerelease identifiers such as `1.0.0-01` and empty identifiers such as
  `1.0.0-alpha..1`. Tightening this is a separate compatibility change.
- §5.1 describes `title` as human-readable and optionally localized; Schema
  requires a nonempty localization object. A plain string is rejected. The prose
  leaves the representation ambiguous and should be made explicit separately.
- The initial data-type registry in §5.2 is descriptive; Schema allows arbitrary
  nonempty I/O type strings. This is an open registry boundary, not an implemented
  closed enum. No defaults are declared in Schema. Top-level MUST/SHOULD/MAY
  requiredness agrees with Schema. Adapter types and modes agree with §9; nested
  field requirements are mostly specified only by Schema, leaving prose gaps.
- Evidence sufficiency, reviewer independence, references, units and semantic
  checks remain outside L0. Accepting a declared evidence status without proving
  it is an explicitly documented limitation, not scientific certification.

The stale §6 claim that the inline example had never been Schema-validated was
updated now that the conformance suite validates it. No other constraints were
changed as part of this erratum.
