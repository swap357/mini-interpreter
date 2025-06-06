import json
import subprocess
import sys
from pathlib import Path


SAMPLES = list(Path('samples').glob('*.py'))


def test_disassemble_outputs_json(tmp_path):
    for sample in SAMPLES:
        out = subprocess.check_output([
            sys.executable,
            'scripts/disassemble.py',
            str(sample)
        ], text=True)
        data = json.loads(out)
        assert isinstance(data, list)
        assert all('opname' in instr for instr in data)
