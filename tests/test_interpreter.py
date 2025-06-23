import subprocess
import sys


def run_sample(filename: str) -> str:
    """Execute the mini interpreter on *filename* and return stdout."""
    return subprocess.check_output(
        [sys.executable, 'src/interpreter.py', f'samples/{filename}'],
        text=True,
    ).strip()


def test_run_hello(tmp_path):
    assert run_sample('hello.py') == 'hello world'


def test_run_loops(tmp_path):
    assert run_sample('loops.py') == '0\n1\n2'


def test_run_conditionals(tmp_path):
    assert run_sample('conditionals.py') == 'positive'


def test_run_calls(tmp_path):
    assert run_sample('calls.py') == '6'
