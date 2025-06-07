import argparse
import json
import subprocess
import sys
import timeit
from pathlib import Path
import tempfile


def bench_sample(sample: Path, repeat: int = 5, number: int = 1):
    cmd = [sys.executable, 'src/interpreter.py', str(sample)]
    timer = timeit.Timer(lambda: subprocess.check_output(cmd))
    times = timer.repeat(repeat, number)
    return {
        'sample': str(sample),
        'repeat': repeat,
        'number': number,
        'times': times,
        'avg_time': sum(times) / len(times),
    }


def run_benchmarks(samples, output_dir: Path):
    results = [bench_sample(s) for s in samples]
    output_dir.mkdir(parents=True, exist_ok=True)
    result_file = output_dir / 'microbench_results.json'
    result_file.write_text(json.dumps(results, indent=2))
    print(result_file)
    return result_file


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run microbenchmarks with the mini interpreter.')
    parser.add_argument('output_dir', nargs='?', default=None, help='directory to store results')
    parser.add_argument('samples', nargs='*', help='sample files to benchmark')
    args = parser.parse_args()

    samples = [Path(s) for s in args.samples] if args.samples else list(Path('samples').glob('*.py'))
    out_dir = Path(args.output_dir) if args.output_dir else Path(tempfile.mkdtemp())

    run_benchmarks(samples, out_dir)
