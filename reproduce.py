"""Reconstruct the submitted documents from frozen saved outputs, without fitting.

Run with the documented dependencies available: python -B reproduce.py
No download, installation, strategy call, notebook execution or portfolio engine.
"""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys

ROOT=Path(__file__).resolve().parent


def main():
    manifest=json.loads((ROOT/'RESEARCH-INPUTS.sha256.json').read_text())
    for name,expected in manifest['files'].items():
        actual=hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
        if actual!=expected:raise RuntimeError('Frozen input hash mismatch: '+name)
    print('Frozen inputs verified; no market values interpreted.',flush=True)
    env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1'
    commands=['capstone/extract_costs.py','capstone/render_saved_figures.py','capstone/build_capstone.py','capstone/build_presentation.py','capstone/build_defence.py','preview_defence.py','verify_submission.py']
    for command in commands:
        print('DOCUMENT BUILD:',command,flush=True)
        subprocess.run([sys.executable,'-B',str(ROOT/command)],cwd=ROOT,env=env,check=True)
    print('Saved-output reconstruction complete. No experiment or diagnostic estimator was rerun.',flush=True)


if __name__=='__main__':main()
