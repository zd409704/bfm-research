"""Coordinator runner for selected independent tests; keeps raw evidence and hashes."""
import argparse,datetime,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]

def main():
    p=argparse.ArgumentParser();p.add_argument('--name',required=True);p.add_argument('tests',nargs='+');a=p.parse_args()
    out=ROOT/'unit_bfm/v3/audits'/a.name;out.mkdir(exist_ok=False)
    files=[f for f in (ROOT/'unit_bfm/v3').rglob('*.py') if not any(x in f.parts for x in ('runs','__pycache__'))]
    def hashes():return {str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
    before=hashes();cmd=[sys.executable,'-m','unittest',*a.tests,'-v']
    with (out/'test.log').open('w') as f:r=subprocess.run(cmd,cwd=ROOT,stdout=f,stderr=subprocess.STDOUT)
    after=hashes();d={'command':cmd,'exit_code':r.returncode,'before':before,'after':after,'changed_during_run':[k for k in before if before[k]!=after[k]],'time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    (out/'manifest.json').write_text(json.dumps(d,indent=2));print(json.dumps({'exit_code':r.returncode,'evidence':str(out),'changed_during_run':d['changed_during_run']}));raise SystemExit(r.returncode)
if __name__=='__main__':main()
