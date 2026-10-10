# CARS 0.1 — Proposed Specification

**Status: Community Draft (non-normative until ratified).**

## 4. Design Principles for 0.1

1. **Task-first:** Name recipes after chemistry tasks rather than model brands.
2. **Execution-neutral:** Keep recipe semantics separate from backend-specific adapters.
3. **Chemistry-aware:** Represent molecular structures, reactions, spectra, and experimental tables explicitly.
4. **Evidence-aware:** Distinguish deterministic calculations, model predictions, retrieved evidence, human annotations, and experimental observations.
5. **Secure by default:** Never automatically execute untrusted code; declare permissions, network access, and sensitive-data handling.
6. **Portable:** Publish schemas, conformance tests, and reference implementations that work without ChemAI Atlas services.
7. **Progressive:** Allow descriptive recipes and make execution capabilities opt-in.
8. **Versioned:** Version the specification independently of individual recipes and test compatibility.

## 5. Proposed Object Model

### 5.1 Top-level fields

| Field | Requirement | Meaning |
|---|---|---|
| `cars_version` | MUST | Specification version, e.g. `0.1.0` |
| `id` | MUST | Globally identifiable URI; hosting by ChemAI Atlas is not required |
| `version` | MUST | Recipe version following SemVer |
| `title` | MUST | Human-readable, optionally localized title |
| `summary` | MUST | Brief purpose and intended audience |
| `domain` / `task` | MUST | Domain classification and task identifier |
| `authors` / `license` | MUST | Attribution and recipe-document license |
| `inputs` / `outputs` | MUST | Types, formats, units, and constraints |
| `capabilities` | MUST | Vendor-independent logical capabilities and dependencies |
| `scientific` | MUST | Method, applicability, limitations, and evidence status |
| `execution` | SHOULD | `documentation_only` or execution adapter binding |
| `security` | MUST | Data classification, network, and code-execution policy |
| `provenance` | SHOULD | References and model/data versions |
| `examples` | SHOULD | Small, nonsensitive inputs and expected results |
| `extensions` | MAY | Namespaced extension properties |

The capitalized terms **MUST**, **SHOULD**, and **MAY** follow the conventions of RFC 2119 and RFC 8174. A normative specification must include the corresponding interpretation clause.

### 5.2 Initial chemistry data-type registry

- **`chemical_structure`:** SMILES, MOL, SDF, or InChI. Specify representation, salt/solvate policy, stereochemistry, and normalization strategy.
- **`chemical_reaction`:** RXN or reaction SMILES. Record reactant/product mapping and stoichiometry where relevant.
- **`molecular_properties`:** JSON or CSV. Each property should carry units, method, conditions, and whether it was calculated, predicted, or measured.
- **`spectrum`:** Choose formats appropriate to the spectroscopy modality, such as JCAMP-DX or mzML; record modality, instrument, and acquisition conditions.
- **`chemical_table`:** CSV, TSV, or SDF. Define column mappings, missing-value handling, and identity/key policy.
- **`literature_set`:** DOI/URI lists or structured citations, with retrieval dates and sources.

Do not assume conversions between chemical representations are lossless. Structure normalization must be an explicit, inspectable operation.

### 5.3 Result semantics and trust

Each result should declare a `result_kind`, chosen from:

- `deterministic_calculation`
- `model_prediction`
- `retrieved_evidence`
- `human_annotation`
- `experimental_measurement`
- `generated_explanation`

The proposed `scientific.validation_status` values are `not_assessed`, `benchmarked`, `independently_reviewed`, and `experimentally_supported`. Any status beyond `not_assessed` requires evidence. These labels are **not a single linear certification ladder**; the dimensions of benchmarking, peer review, and experimental support must remain distinguishable.

## 6. Minimal YAML Example

*Illustrative only; this example has not yet been validated against an implemented CARS JSON Schema.*

```yaml
cars_version: "0.1.0"
id: "https://example.org/recipes/molecular-descriptors"
version: "1.0.0"
title:
  en: "Molecular Descriptor Calculation"
  zh: "分子描述符计算"
summary:
  en: "Calculate selected descriptors from a validated molecular structure."
domain: "cheminformatics"
task: "molecular_descriptor_calculation"
authors:
  - name: "Example Research Team"
license: "CC-BY-4.0"
inputs:
  - id: "molecule"
    type: "chemical_structure"
    required: true
    formats: ["smiles"]
    constraints:
      stereochemistry: "preserve_if_present"
      mixture_policy: "reject"
outputs:
  - id: "descriptors"
    type: "molecular_properties"
    formats: ["application/json"]
    properties:
      - name: "molecular_weight"
        unit: "g/mol"
        result_kind: "deterministic_calculation"
capabilities:
  - id: "validate_structure"
    kind: "structure_validation"
  - id: "calculate_descriptors"
    kind: "molecular_descriptor_calculation"
    depends_on: ["validate_structure"]
scientific:
  method: "Structure validation followed by descriptor calculation"
  applicability: "Single-component organic molecules supported by the chosen toolkit"
  limitations:
    - "Input representation and normalization affect computed values"
  validation_status: "not_assessed"
security:
  data_classification: "public_or_non_sensitive"
  network_access: "not_required"
  untrusted_code_execution: false
execution:
  mode: "adapter"
  adapters:
    - type: "cwl"
      definition: "workflow.cwl"
provenance:
  references: []
examples:
  - input: {molecule: "CCO"}
    note: "Illustrative input only; numerical output omitted pending executable test"
```

**Important:** `license` applies to the recipe document, not automatically to model weights, datasets, APIs, or third-party software. Dependencies require separate license declarations. A future normative release should choose a verifiable units vocabulary or UCUM-compatible mapping. An executor must not run arbitrary referenced files solely because a manifest points to them.

## 7. Proposed Conformance Profiles

| Profile | Requirements | What a user may reasonably expect |
|---|---|---|
| `CARS-Describe` | Core metadata, chemical I/O, limitations, security | Searchable, understandable, comparable |
| `CARS-Execute` | Describe + supported adapter + parameter validation | Runnable in a specified environment; **not** a guarantee of scientific correctness |
| `CARS-Reproduce` | Execute + pinned dependencies, test inputs, output checks, run provenance | Repeatable tests under declared conditions |
| `CARS-Reviewed` | Any applicable profile + identified reviewer, scope, date, and evidence | Scoped third-party review, **not** experimental certification |

`CARS-Reviewed` should be treated as an **orthogonal review assertion**, not as a level that automatically outranks `CARS-Reproduce`. Interfaces should display **format conformance**, **execution tests**, and **scientific evidence** separately.

## 8. Validation Framework

1. **L0 — Schema:** Required fields, data types, enumerations, URIs, and versions.
2. **L1 — Semantic:** Acyclic capability dependencies, resolvable references, compatible formats/units, nonempty applicability statements.
3. **L2 — Security:** Dependency licensing, least-privilege permissions, outbound requests, credentials, and supply-chain checks.
4. **L3 — Execution:** Sandbox execution of fixtures, with runtime, failure information, and output checks recorded.
5. **L4 — Scientific:** Comparison against references or benchmarks, with error metrics, coverage, failure cases, and reviewer attribution.

Much of L0–L3 can be automated. L4 must be tailored to each chemistry task and cannot be replaced with a universal score. For predictive models, report possible data leakage, training-set overlap, applicability domain, and uncertainty. For retrosynthesis, generated routes must not be presented as experimentally demonstrated feasibility.

## 9. Execution Bindings and Security Model

- **`documentation_only`:** Human-readable instructions, with no claim of machine execution.
- **`adapter:cwl`:** Reference validated CWL documents and pinned dependencies.
- **`adapter:arazzo`:** Reference Arazzo descriptions for API-oriented sequences.
- **`adapter:agent_skill`:** Reference a Skill package and explicitly declare host environment and permissions; do not assume consistent behavior across clients.
- **`adapter:mcp`:** Reference discoverable tool capabilities and server configuration; MCP does not itself replace workflow orchestration.
- **`adapter:native`:** Allow proprietary platform execution, but do not count it as evidence of cross-platform interoperability.

Do not store API keys inside recipe files. Inject credentials through a platform secret manager. Execute third-party code in isolated environments with network, filesystem, CPU/GPU, duration, and cost limits. Private molecular structures and unpublished experimental data must not be used for model training or placed in public logs by default. Platforms need explicit retention and deletion policies.

## Compatibility note

The accompanying JSON Schema covers a subset of this proposal (L0 only). Additional semantic, security, execution and scientific checks are future work.
