import difflib
from pathlib import Path
import argparse

HEADER = "## Bytecode diffs (3.13.3 → 3.14-dev)"


def diff_json(old, new):
    old_lines = Path(old).read_text().splitlines()
    new_lines = Path(new).read_text().splitlines()
    return list(difflib.unified_diff(old_lines, new_lines, fromfile=str(old), tofile=str(new)))


def generate(samples, old_dir, new_dir, output):
    lines = [HEADER, ""]
    for sample in samples:
        lines.append(f"### {sample}")
        lines.append("")
        lines.append("```python")
        lines.extend(Path(sample).read_text().splitlines())
        lines.append("```")
        lines.append("")
        old_json = Path(old_dir) / f"{Path(sample).name}.json"
        new_json = Path(new_dir) / f"{Path(sample).name}.json"
        diff_lines = diff_json(old_json, new_json)
        lines.append("```diff")
        lines.extend(diff_lines)
        lines.append("```")
        lines.append("")
    Path(output).write_text("\n".join(lines))


def main(argv=None):
    parser = argparse.ArgumentParser(description="Generate bytecode diff report with source code.")
    parser.add_argument("old_dir", help="directory with old version disassembly")
    parser.add_argument("new_dir", help="directory with new version disassembly")
    parser.add_argument("samples", nargs="*", default=None, help="sample files")
    parser.add_argument("-o", "--output", default="BYTECODE_DIFF.md", help="output markdown file")
    args = parser.parse_args(argv)

    sample_files = args.samples or [str(p) for p in Path("samples").glob("*.py")]
    generate(sample_files, args.old_dir, args.new_dir, args.output)


if __name__ == "__main__":
    main()
