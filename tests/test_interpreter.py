import subprocess
import sys


def test_run_hello(tmp_path):
    out = subprocess.check_output([
        sys.executable,
        'src/interpreter.py',
        'samples/hello.py'
    ], text=True)
    assert out.strip() == 'hello world'


def test_run_loops(tmp_path):
    out = subprocess.check_output([
        sys.executable,
        'src/interpreter.py',
        'samples/loops.py'
    ], text=True)
    assert out.strip() == str(sum(range(5)))


def test_run_conditional(tmp_path):
    out = subprocess.check_output([
        sys.executable,
        'src/interpreter.py',
        'samples/conditional.py'
    ], text=True)
    assert out.strip() == 'true'


def test_run_function_call(tmp_path):
    out = subprocess.check_output([
        sys.executable,
        'src/interpreter.py',
        'samples/function_call.py'
    ], text=True)
    assert out.strip() == '3'
