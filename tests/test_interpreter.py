import subprocess
import sys


def test_run_hello(tmp_path):
    out = subprocess.check_output([
        sys.executable,
        'src/interpreter.py',
        'samples/hello.py'
    ], text=True)
    assert out.strip() == 'hello world'
