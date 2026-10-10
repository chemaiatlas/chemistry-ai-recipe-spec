# Prototype Roadmap

## 13. Eight-Week Prototype Roadmap

| Week | Focus | Deliverable |
|---|---|---|
| **1** | Scope, terminology, review of prior art and scientific standards | RFC-0001 and glossary |
| **2** | 0.1 fields, JSON Schema, sample manifests | Alpha schema and two examples |
| **3** | Validator CLI, error codes, negative tests | `cars validate` prototype |
| **4** | First executable recipe (CWL or native) | Run record and test fixtures |
| **5** | Second, independent execution backend (API/Arazzo) | Interoperability comparison |
| **6** | PostgreSQL and recipe-page integration | Import/export and version snapshots |
| **7** | Invite 3–5 external developers and chemistry users | Feedback, failure cases, RFCs |
| **8** | Revise draft and publish assessment | Draft 0.1 and go/no-go decision |

**Go/no-go gates:** Three distinct task examples; two execution backends; all published examples pass L0/L1; at least one external developer imports a recipe without private APIs; and end users can distinguish calculated, predicted, and measured results. If these are not met, continue treating CARS as an experimental interchange format rather than presenting it as an industry standard.
