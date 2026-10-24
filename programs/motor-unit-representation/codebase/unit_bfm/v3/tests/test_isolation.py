"""Protect the old implementation and keep V3 import dependencies explicit."""
import ast
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[3]

class IsolationTests(unittest.TestCase):
    def test_legacy_baseline_unchanged(self):
        baseline = ROOT / '.ssh/relay-agents/v3-development-baseline.json'
        if not baseline.exists():
            self.skipTest('Coordinator baseline is not distributed with this checkout')
        saved=json.loads(baseline.read_text())
        for name,digest in saved['files'].items():
            with self.subTest(file=name):
                p=ROOT/name
                self.assertTrue(p.is_file())
                self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),digest)
        for name,info in saved['artifact_files'].items():
            with self.subTest(artifact=name):
                st=(ROOT/name).stat()
                self.assertEqual(st.st_size,info['size'])
                self.assertEqual(st.st_mtime_ns,info['mtime_ns'])

    def test_no_importing_legacy_training_components(self):
        base=ROOT/'unit_bfm/v3'
        for path in base.rglob('*.py'):
            if any(p in path.parts for p in ('runs','__pycache__')):
                continue
            for node in ast.walk(ast.parse(path.read_text(),filename=str(path))):
                with self.subTest(file=path.name,line=getattr(node,'lineno',0)):
                    if isinstance(node,ast.ImportFrom):
                        self.assertFalse(node.level>=2,'V3 must not import its parent V2 implementation')
                        module=node.module or ''
                        self.assertFalse(module=='unit_bfm' or (module.startswith('unit_bfm.') and not module.startswith('unit_bfm.v3')))
                    elif isinstance(node,ast.Import):
                        for alias in node.names:
                            self.assertFalse(alias.name.startswith('unit_bfm.') and not alias.name.startswith('unit_bfm.v3'))

if __name__=='__main__':unittest.main()
