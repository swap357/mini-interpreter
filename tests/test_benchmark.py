import json
import subprocess
import sys
from pathlib import Path


def test_microbench_runs(tmp_path):
    outdir = tmp_path / 'bench'
    subprocess.check_call([
        sys.executable,
        'scripts/microbench.py',
        str(outdir),
        'samples/hello.py'
    ])
    result_file = outdir / 'microbench_results.json'
    assert result_file.exists()
    data = json.loads(result_file.read_text())
    assert isinstance(data, list)
    assert data and data[0]['sample'].endswith('hello.py')
