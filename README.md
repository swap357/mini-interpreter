# Mini Bytecode Interpreter

This project explores Python bytecode changes between versions 3.13 and 3.14. It
contains a minimal bytecode interpreter written in Python along with utilities
to disassemble sample programs and compare the resulting bytecode across Python
versions.

## Quickstart

1. Install dependencies and run the tests:
   ```bash
   pip install -U pytest
   pytest -q
   ```
2. Run the interpreter on a sample:
   ```bash
   python src/interpreter.py samples/hello.py
   ```
3. Run microbenchmarks:
   ```bash
   python scripts/microbench.py results_dir samples/hello.py --repeat 3 --number 1
   ```
   This will output a JSON file with timing information.
4. Inspect bytecode differences by running the GitHub Actions workflow which
   disassembles the samples on both Python 3.13 and 3.14 and produces a diff
   report.

## License

This project is licensed under the MIT License. See `LICENSE` for details.
