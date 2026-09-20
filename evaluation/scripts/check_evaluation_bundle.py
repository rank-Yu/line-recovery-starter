"""Verify evaluation inputs, references and fixtures; no model calls."""
import hashlib
import json
from pathlib import Path
from datasets import check_case

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
GRADING = ROOT / 'grading'
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    split = read(DATA / 'split-manifest.json')['cases']
    package = read(GRADING / 'manifest.json')
    assert sha(DATA / 'split-manifest.json') == package['split_manifest_sha256']
    assert len(split) == len(package['cases']) == 17
    assert {e['case_id'] for e in split if e['split'] == 'optimization'} == {f'lr_{n}' for n in range(101,111)}
    assert {e['case_id'] for e in split if e['split'] == 'test'} == {'lr_201','lr_203','lr_204','lr_205','lr_206','lr_302','lr_306'}
    refs = {e['case_id']: e for e in package['cases']}
    expected_inputs = set(); expected_refs = set()
    for e in split:
        directory = DATA / e['input']; ref = refs[e['case_id']]
        assert e['input'] == e['split'] + '/' + e['case_id'] == ref['input']
        assert sha(directory/'manifest.json') == e['input_manifest_sha256'] == ref['input_manifest_sha256']
        check_case(directory)
        expected_inputs.add(directory)
        assert set(ref['files']) == {'reference.json','backend-fixture.json'}
        for name, info in ref['files'].items():
            f = GRADING / e['input'] / name
            assert f.stat().st_size == info['bytes'] and sha(f) == info['sha256']
            obj = read(f); assert obj['case_id'] == e['case_id']
            if name == 'reference.json': assert obj['split'] == e['split']
            else: assert obj['execution_mode'] == 'dry_run'
            expected_refs.add(f)
    actual_inputs = {p for split_name in ('optimization','test') for p in (DATA/split_name).iterdir()}
    actual_refs = {p for split_name in ('optimization','test') for p in (GRADING/split_name).rglob('*') if p.is_file()}
    assert actual_inputs == expected_inputs and actual_refs == expected_refs
    print(json.dumps({'optimization':10,'test':7,'input_files':187,'evaluation_files':34,'passed':True,'model_calls':0}))
if __name__ == '__main__': main()
