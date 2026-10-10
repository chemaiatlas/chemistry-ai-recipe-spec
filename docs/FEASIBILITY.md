# CARS 0.1 — Feasibility Study

## 1. Executive Summary

CARS proposes an open, vendor-neutral, machine-readable way to describe chemistry AI recipes. It allows chemistry practitioners to interact with services through a **task → input → result** experience, while researchers and developers can implement the same declared capability using different execution backends.

**Recommendation: proceed with a limited 0.1 prototype, not a claim of standardization.** The initial scope covers recipe metadata, input/output contracts, chemical semantics, capability declarations, scientific limitations and evidence, provenance, security requirements, and optional execution bindings. It does not introduce a new scheduling language or promise that computational predictions reproduce experimental findings.

Success criteria for the pilot are: **at least three distinct recipes, two independent execution implementations, one externally importable example, a functioning schema validator, and traceable execution reports.**

## 2. Problem, Stakeholders, and Scope

### 2.1 Intended users

- **Chemistry practitioners:** Submit structures, data, or files using familiar scientific forms without understanding LLMs, MCP, containers, or APIs.
- **Recipe authors:** Researchers, scientific software developers, and model providers who declare task boundaries, inputs, outputs, applicability, and supporting evidence.
- **Execution platforms:** ChemAI Atlas or third parties that handle authorization, scheduling, billing, isolation, logging, and presentation of results.
- **Reviewers:** Independent parties assessing security, evidence, and reproducibility. Scientific review must remain separate from syntactic conformance.

### 2.2 Non-goals for 0.1

- Replacing CWL, WDL, Arazzo, MCP, Agent Skills, or RO-Crate.
- Inventing new chemical structure representations, nomenclature, unit systems, or ontologies.
- Requiring every recipe to be executable; `documentation_only` recipes remain valid.
- Defining a universal billing, federated identity, or cross-platform payment protocol.
- Treating LLM-generated explanations as experimentally established facts.

## 3. Existing Standards and the Gap

| Standard or ecosystem | Existing contribution | What CARS should reuse | What CARS must not duplicate |
|---|---|---|---|
| **CWL v1.2** | Portable scientific tool and workflow descriptions | Tool/workflow references, I/O contracts, containers | A scheduling language |
| **WDL** | Data-analysis task orchestration | Resource requirements and task boundaries | Workflow execution syntax |
| **Arazzo 1.1** | API and event-driven workflow descriptions | API-oriented execution adapters | API workflow language |
| **BioCompute Object / IEEE 2791** | Computational methods, parameters, provenance, error domains | Scientific purpose, parameters, uncertainty, review | The entire BCO object model |
| **RO-Crate / Workflow Run RO-Crate** | Structured research objects and execution provenance | Artifacts, versions, evidence, run records | General-purpose provenance format |
| **Agent Skills** | Packaging instructions, scripts, and resources for agents | Instruction-based adapter | Agent instruction conventions |
| **MCP** | Connecting AI applications to tools | Tool invocation bridges | Tool transport/protocol |
| **InChI, SMILES, SDF, IUPAC terminology** | Chemistry representations and naming | Explicit representation and normalization policies | New molecular representations |
| **OPTIMADE** | Materials database API interoperability | Domain-specific interface governance | Materials database API |

**Gap hypothesis:** We have not identified a widely adopted unified specification covering, together, **chemistry task semantics + AI applicability + recipe discovery + execution bindings + scientific evidence**. This is a research and product hypothesis, **not proof that no similar specification exists**. A public call for prior art and systematic literature review should precede any stronger claim.

### 3.1 Architectural position

```text
End user: choose a chemistry task -> supply data -> inspect results
                              |
                     CARS recipe manifest
     [task / chemical I-O / capabilities / evidence / policy]
                              |
                   optional execution adapter
             CWL | Arazzo | Agent Skill | MCP | native
                              |
                 tools / models / data / services
                              |
             results + provenance + validation record
```

CARS is **not an execution engine**. It describes **what a recipe is, who it serves, what it requires, how it can be evaluated, and which execution mechanism may run it**.

## 10. Interoperability and Open Governance

### 10.1 Suggested public repository

```text
chemistry-ai-recipe-spec/
  README.md
  SPECIFICATION.md
  schema/cars-0.1.schema.json
  examples/molecular-descriptors/recipe.yaml
  examples/chemical-data-validation/recipe.yaml
  examples/literature-extraction/recipe.yaml
  tests/valid/
  tests/invalid/
  rfcs/
  governance/CONTRIBUTING.md
  governance/CODE_OF_CONDUCT.md
  LICENSE
```

A possible licensing approach is **CC BY 4.0 for prose specification text** and **Apache-2.0 or MIT for code, schemas, and validators**, subject to contributor agreement and legal review. Publish stable, versioned specification URLs with mirrors and downloadable releases.

### 10.2 Governance principles

- Use public RFCs, issues, change logs, and recorded design decisions.
- ChemAI Atlas may initiate the project, but third parties must be able to validate and implement it independently.
- Establish compatibility rules: allow rapid changes during 0.1; define a formal deprecation process after 1.0.
- Separate **schema maintenance**, **recipe catalog moderation**, and **scientific review** responsibilities.
- Publish conflicts of interest and prevent paid placement from influencing scientific-quality labels.

## 11. Integration with ChemAI Atlas

ChemAI Atlas can retain its existing **PostgreSQL** resource and recipe content model. It does not need an immediate migration to CARS. Consider adding:

- `recipe_spec_version`, `recipe_manifest_jsonb`, `manifest_sha256`, `conformance_profile`.
- **`recipe_versions`:** Immutable version snapshots and publication history.
- **`recipe_executors`:** Backend type, entry point, availability, and permissions.
- **`recipe_validation_runs`:** Layered results, log summaries, tool versions, and run timestamps.
- **`recipe_evidence`:** Publications, benchmarks, review statements, and provenance.

Store manifests as PostgreSQL `jsonb`, while indexing frequently searched attributes in conventional columns. Compute SHA-256 over a specified canonical published representation; otherwise, harmless serialization differences can change hashes. Avoid reducing the validation model to a single `validated` Boolean.

### 11.1 User experience

**For practitioners:** Browse by tasks such as molecular analysis, data cleaning, spectroscopy, and literature extraction. Show only task forms, result explanations, costs, and clearly differentiated evidence labels.

**For developers:** Expose the manifest, dependencies, execution adapters, versions, and test reports.

## 12. Recommended Pilot Recipes

| Pilot | Why it is useful | Difficulty | Critical checks |
|---|---|---|---|
| **Molecular descriptor calculation** | Deterministic, standard structure input | Low | Reference structures/values; salt and stereochemistry edge cases |
| **CAS/name/structure consistency checking** | Closely aligned with real chemical-data cleaning | Medium | Distinguish CAS format checks from identity matching; trace sources |
| **Extraction of experimental conditions from literature** | Tests LLMs alongside evidence chains | Medium–high | Citation anchoring, human sampling, hallucination rates |

Avoid starting with definitive toxicity judgments, clinical recommendations, hazardous reaction operations, or fully automated synthesis execution. These demand more extensive validation and safety controls.

## 14. Risk Register

| Risk | Severity | Mitigation |
|---|---|---|
| Duplication of existing standards | High | Define only chemistry semantics and bindings; reuse established specifications |
| Insufficient chemistry expertise | High | Invite at least two domain experts from different specialties into RFCs and scientific review |
| Unreliable scientific outputs | High | Independent evidence states, applicability, benchmark datasets, human review |
| Malicious third-party recipes | High | Isolation, hashes/signatures, permission review, no automatic execution |
| Overly complex specification | Medium–high | Small core schema with optional profiles/extensions |
| Ecosystem cold start | High | Export existing recipes first; then recruit independent implementers |
| Conflict between openness and monetization | Medium | Keep specification and validator open; monetize hosting and services |
| Licensing and data rights | High | Per-dependency licensing, privacy classification, audit trails |

## 15. Business Model and Open Boundaries

**Recommended open assets:** Specification text, schema, validator, test fixtures, public recipe manifests, and basic import/export interfaces.

**Potential commercial services:** Hosted execution, GPU compute, private workspaces, enterprise SSO, organizational review, batch processing, audit capabilities, and SLAs. Payment must never be a prerequisite for a positive scientific-validation label.

The ecosystem value of an open specification depends on whether third parties can implement, validate, and exchange recipes **without seeking permission from ChemAI Atlas**. Otherwise, the more accurate term is a platform-specific file format, not an open standard.

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

## 17. Primary References (as of 2026-10-10)

- Common Workflow Language: https://www.commonwl.org/ ; https://www.commonwl.org/v1.2/
- BioCompute Object: https://docs.biocomputeobject.org/ ; https://docs.biocomputeobject.org/bco-domains/
- Arazzo: https://spec.openapis.org/arazzo/latest.html
- RO-Crate: https://www.researchobject.org/ro-crate/ ; https://www.researchobject.org/workflow-run-crate/
- Agent Skills: https://agentskills.io/specification ; https://github.com/agentskills/agentskills
- Model Context Protocol: https://modelcontextprotocol.io/specification/
- Workflow Description Language: https://openwdl.org/
- OPTIMADE: https://www.optimade.org/specification/latest/
- InChI Trust: https://www.inchi-trust.org/
- IUPAC: https://iupac.org/
- JSON Schema: https://json-schema.org/specification
- RFC 2119 and RFC 8174: https://www.rfc-editor.org/rfc/rfc2119 ; https://www.rfc-editor.org/rfc/rfc8174

---

## Recommendation

Initiate CARS as an **independent, open-source project supported by ChemAI Atlas**. Begin with a **verifiable chemistry recipe manifest and reference adapters**, demonstrate genuine cross-platform value through working examples, and defer claims of industry-standard status or plans for a full marketplace and generalized execution engine.

**Suggested short project description:**

> An open, vendor-neutral specification for describing, validating, and exchanging AI-powered chemistry recipes and workflows. Initiated by ChemAI Atlas.
