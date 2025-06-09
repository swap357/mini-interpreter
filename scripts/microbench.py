import argparse
"""Simple microbenchmark harness for the mini interpreter."""

import argparse
import json
import statistics
import subprocess
import sys
import timeit
from pathlib import Path
import tempfile


def bench_sample(sample: Path, repeat: int = 5, number: int = 1) -> dict:
    """Return timing statistics for a single sample."""

    cmd = [sys.executable, "src/interpreter.py", str(sample)]
    timer = timeit.Timer(lambda: subprocess.check_output(cmd))
    times = timer.repeat(repeat, number)
    return {
        "sample": str(sample),
        "repeat": repeat,
        "number": number,
        "times": times,
        "avg_time": statistics.mean(times),
        "stdev": statistics.stdev(times) if len(times) > 1 else 0.0,
    }


def run_benchmarks(samples, output_dir: Path, repeat: int, number: int) -> Path:
    """Benchmark all samples and store results in *output_dir*."""

    output_dir.mkdir(parents=True, exist_ok=True)
    results = [bench_sample(s, repeat=repeat, number=number) for s in samples]
    result_file = output_dir / "microbench_results.json"
    result_file.write_text(json.dumps(results, indent=2))
    return result_file


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Run microbenchmarks with the mini interpreter."
    )
    parser.add_argument(
        "output_dir", nargs="?", default=None, help="directory to store results"
    )
    parser.add_argument("samples", nargs="*", help="sample files to benchmark")
    parser.add_argument("--repeat", type=int, default=5, help="repeat count")
    parser.add_argument("--number", type=int, default=1, help="loops per repeat")
    args = parser.parse_args(argv)

    samples = (
        [Path(s) for s in args.samples]
        if args.samples
        else list(Path("samples").glob("*.py"))
    )
    out_dir = Path(args.output_dir) if args.output_dir else Path(tempfile.mkdtemp())

    result_file = run_benchmarks(samples, out_dir, args.repeat, args.number)
    print(result_file)


if __name__ == "__main__":
    main()
