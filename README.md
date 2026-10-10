# Chemistry AI Recipe Specification (CARS)

**Community Draft 0.1 — experimental, not an adopted industry standard.**

CARS is a proposed open, vendor-neutral manifest format for describing, discovering, validating and exchanging AI-assisted chemistry tasks. It is **not** a workflow engine and does **not** certify scientific correctness.

## Why CARS?

Chemistry practitioners should be able to select a task, provide chemical data and inspect results without configuring models, agents or orchestration systems. Authors should be able to publish portable task descriptions with chemical input/output contracts, limitations, security declarations and optional execution bindings.

## Start here

- [Draft specification](SPECIFICATION.md) — proposed fields, profiles and validation levels
- [Feasibility study](docs/FEASIBILITY.md) — prior art, risks and architectural choices
- [Roadmap](ROADMAP.md) — eight-week prototype plan
- [Example recipe](examples/molecular-descriptors.yaml)
- [JSON Schema](schema/cars-0.1.schema.json) — provisional L0 validator
- [RFC 0001](rfcs/0001-scope-and-governance.md) — initial design questions
- [Contributing](CONTRIBUTING.md) — how to participate

## Validate an example

```bash
python -m pip install -r tools/requirements.txt
python tools/validate.py examples/molecular-descriptors.yaml
python -m unittest discover -s tests -v
```

The validator performs **L0 structural checks only**. A passing manifest is not executable, secure or scientifically validated by implication.

## Proposed architecture

`Chemistry task → CARS manifest → optional CWL / Arazzo / Agent Skill / MCP / native adapter → tools → provenance and evidence`

## Project status and governance

This is a discussion-oriented proposal initiated by [ChemAI Atlas](https://chemaiatlas.com/). Independent implementations, critical feedback, and prior-art references are welcome. The initial field names and profiles are provisional. No official standards-body endorsement is claimed.

## License

Specification text and documentation: [CC BY 4.0](LICENSE-DOCS.md). Code, schemas and tests: [Apache 2.0](LICENSE). Individual recipe authors must declare their own recipe license; this does not license third-party models or datasets.
