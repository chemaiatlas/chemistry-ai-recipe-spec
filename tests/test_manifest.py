import copy
import sys
import unittest
from pathlib import Path
import yaml
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from validate import validate_file

class ManifestTests(unittest.TestCase):
    def test_example_passes_l0(self):
        self.assertEqual([], validate_file(ROOT / 'examples' / 'molecular-descriptors.yaml'))
    def test_missing_required_field_fails(self):
        from jsonschema import Draft202012Validator
        import json
        obj = yaml.safe_load((ROOT / 'examples' / 'molecular-descriptors.yaml').read_text())
        obj.pop('scientific')
        schema = json.loads((ROOT / 'schema' / 'cars-0.1.schema.json').read_text())
        self.assertTrue(list(Draft202012Validator(schema).iter_errors(obj)))

if __name__ == '__main__': unittest.main()
