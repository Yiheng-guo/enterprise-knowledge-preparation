from pathlib import Path
import unittest,json,importlib.util,subprocess,sys,tempfile
R=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('skill_runner',R/'scripts/run.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class SkillTests(unittest.TestCase):
    def test_normal(self):
        result=m.process(json.loads((R/'examples/input.json').read_text()))
        self.assertNotIn(result['status'],('blocked','failed'))
    def test_failure_boundary(self):
        data=json.loads((R/'examples/failure-input.json').read_text())
        result=m.process(data)
        self.assertEqual(result['public_export'],[]); self.assertEqual(len(result['conflicts']),1)
    def test_refuse_overwrite(self):
        with tempfile.TemporaryDirectory() as temp:
            out=Path(temp)/'result.json';out.write_text('preserve')
            p=subprocess.run([sys.executable,str(R/'scripts/run.py'),str(R/'examples/input.json'),'--output',str(out)],capture_output=True)
            self.assertNotEqual(p.returncode,0);self.assertEqual(out.read_text(),'preserve')
if __name__=='__main__':unittest.main()
