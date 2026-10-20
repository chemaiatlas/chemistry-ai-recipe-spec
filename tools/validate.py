#!/usr/bin/env python3
"""Validate CARS draft manifests at L0 (JSON Schema only)."""
import json, sys
from pathlib import Path
import yaml
from jsonschema import Draft202012Validator, FormatChecker

SCHEMA = Path(__file__).resolve().parents[1] / 'schema' / 'cars-0.1.schema.json'

def validate_file(path):
    manifest = yaml.safe_load(Path(path).read_text(encoding='utf-8'))
    schema = json.loads(SCHEMA.read_text(encoding='utf-8'))
    Draft202012Validator.check_schema(schema)
    return sorted(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(manifest), key=lambda e: list(map(str,e.path)))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python tools/validate.py PATH.yaml', file=sys.stderr)
        sys.exit(2)
    try:
        errors = validate_file(sys.argv[1])
    except Exception as exc:
        print(f'Validation error: {exc}', file=sys.stderr)
        sys.exit(2)
    for error in errors:
        if (list(error.path) == ['scientific', 'validation_status']
                and error.validator == 'enum'
                and isinstance(error.instance, str)
                and error.instance in ('under_review', 'reviewed')):
            print('Migration required: legacy scientific.validation_status has no lossless '
                  'mapping. Assess the evidence and explicitly choose a value from '
                  'SPECIFICATION.md section 5.3; no automatic conversion was performed.',
                  file=sys.stderr)
        print(f'FAIL {"/".join(map(str,error.path)) or "<root>"}: {error.message}')
    if errors:
        sys.exit(1)
    print('PASS: CARS 0.1 L0 structural validation only (NOT scientific or execution validation)')
