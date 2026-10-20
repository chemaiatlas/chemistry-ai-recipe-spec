import copy
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from validate import validate_file


class ManifestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spec = (ROOT / 'SPECIFICATION.md').read_text(encoding='utf-8')
        cls.schema = json.loads((ROOT / 'schema/cars-0.1.schema.json').read_text())
        Draft202012Validator.check_schema(cls.schema)
        cls.validator = Draft202012Validator(cls.schema, format_checker=FormatChecker())
        cls.statuses = cls.schema['properties']['scientific']['properties']['validation_status']['enum']
        cls.example_paths = sorted(p for p in (ROOT / 'examples').rglob('*')
                                   if p.suffix in ('.yaml', '.yml', '.json'))
        cls.example = yaml.safe_load(cls.example_paths[0].read_text())

    def test_specification_status_enum_matches_schema(self):
        section = self.spec.split('### 5.3 ', 1)[1].split('\n## ', 1)[0]
        values = re.findall(r'^\| `([^`]+)` \|', section, re.MULTILINE)
        self.assertTrue(values, 'Missing machine-readable status table in section 5.3')
        self.assertEqual(len(values), len(set(values)))
        self.assertCountEqual(values, self.statuses)

    def test_specification_required_top_level_fields_match_schema(self):
        section = self.spec.split('### 5.1 ', 1)[1].split('### 5.2 ', 1)[0]
        fields = []
        for line in section.splitlines():
            if '| MUST |' in line:
                fields.extend(re.findall(r'`([^`]+)`', line.split('| MUST |')[0]))
        self.assertCountEqual(fields, self.schema['required'])

    def test_all_official_examples_pass_schema_and_cli(self):
        self.assertTrue(self.example_paths)
        for path in self.example_paths:
            with self.subTest(path=path):
                self.assertEqual([], validate_file(path))
                result = self.run_cli(path)
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)
                self.assertIn('NOT scientific or execution validation', result.stdout)

    def test_specification_yaml_examples_pass_schema(self):
        blocks = re.findall(r'```yaml\n(.*?)\n```', self.spec, re.DOTALL)
        self.assertTrue(blocks)
        for block in blocks:
            self.assertEqual([], list(self.validator.iter_errors(yaml.safe_load(block))))

    def run_cli(self, path):
        return subprocess.run([sys.executable, str(ROOT / 'tools/validate.py'), str(path)],
                              capture_output=True, text=True, timeout=15, cwd=ROOT)

    def test_status_schema_and_cli_agree_without_mutation(self):
        # Legal values come from Schema; forbidden and wrong-type values are probes.
        cases = [(value, True) for value in self.statuses]
        cases += [(value, False) for value in (
            'under_review', 'reviewed', 'invalid', '', 'BENCHMARKED', None, 1, True, [], {})]
        with tempfile.TemporaryDirectory() as directory:
            for index, (value, expected) in enumerate(cases):
                with self.subTest(value=value):
                    obj = copy.deepcopy(self.example)
                    obj['scientific']['validation_status'] = value
                    self.assertEqual(expected, self.validator.is_valid(obj))
                    # Exercise both YAML and JSON inputs through the real command.
                    for extension in ('yaml', 'json'):
                        path = Path(directory) / f'case-{index}.{extension}'
                        data = yaml.safe_dump(obj) if extension == 'yaml' else json.dumps(obj)
                        path.write_text(data, encoding='utf-8')
                        self.assertEqual(expected, not validate_file(path))
                        result = self.run_cli(path)
                        self.assertEqual(0 if expected else 1, result.returncode,
                                         result.stdout + result.stderr)
                        if isinstance(value, str) and value in ('under_review', 'reviewed'):
                            self.assertIn('no lossless mapping', result.stderr)
                            self.assertIn('no automatic conversion', result.stderr)
                        self.assertEqual(data, path.read_text(encoding='utf-8'))

    def test_missing_required_field_fails_schema_and_cli(self):
        with tempfile.TemporaryDirectory() as directory:
            for field in self.schema['required']:
                with self.subTest(field=field):
                    obj = copy.deepcopy(self.example)
                    obj.pop(field)
                    self.assertFalse(self.validator.is_valid(obj))
                    path = Path(directory) / 'missing.json'
                    path.write_text(json.dumps(obj))
                    self.assertEqual(1, self.run_cli(path).returncode)
            obj = copy.deepcopy(self.example)
            obj['scientific'].pop('validation_status')
            self.assertFalse(self.validator.is_valid(obj))
            path.write_text(json.dumps(obj))
            self.assertEqual(1, self.run_cli(path).returncode)


if __name__ == '__main__':
    unittest.main()
