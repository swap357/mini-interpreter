# Testing and Benchmarking Improvement Plan

This document outlines tasks for extending the current test suite into a more robust benchmarking framework. The goal is to provide insights from micro to macro level bytecode analysis and act as a reference for adapting tools like Numba to Python 3.14.

## Modular Task List for Codex

The following tasks are ordered so that they build on each other. Each task is
small enough for the Codex agent to implement in a focused pull request.

1. **Expand sample programs and tests**
   - Create new examples in `samples/` covering loops, conditionals and
     function calls.
   - Add tests in `tests/` to run these samples through the interpreter and
     check their output.

2. **Cross-version validation script**
   - Write a script that executes the interpreter under Python 3.13 and 3.14
     and compares results.
   - Integrate this script into a GitHub Actions workflow.

3. **Microbenchmark harness**
   - Add a benchmarking module that uses `pyperf` (or `timeit` if dependencies
     are limited) to time the execution of short code snippets.
   - Store benchmark results as JSON in a temporary directory.

4. **Macro benchmark runner**
   - Provide a script that can execute larger programs or selected benchmarks
     from the `performance` suite.
   - Summarize total execution time and instruction counts.

5. **Profiling hooks**
   - Extend `MiniInterpreter` with optional instrumentation that records the
     opcode sequence during execution.
   - Output a profile file that can be loaded by other tools for comparison.

6. **Documentation updates**
   - Document how to run the benchmarking scripts and how to interpret the
     output.
   - Summarize key findings in `docs/3.14_changes.md` as tasks progress.

7. **CI integration**
   - Update `.github/workflows/compare-bytecode.yml` so that it runs the new
     scripts and uploads the JSON results as artifacts.
   - Configure the workflow to fail if benchmarks regress beyond a set
     threshold.

## 1. Expand Functional Test Coverage
- Add more sample programs that exercise a variety of Python opcodes (loops, conditionals, function calls, comprehensions). Create corresponding tests in `tests/` to ensure the interpreter handles them correctly.
- Include edge cases such as exception handling, list/dict operations and attribute access.

## 2. Cross‑Version Bytecode Validation
- Run the interpreter and disassembly scripts under both Python 3.13 and 3.14.
- Verify that the interpreter produces identical output across versions for the same source program, or record intentional differences when new opcodes appear.
- Integrate this check into CI to prevent regressions when upgrading Python.

## 3. Microbenchmarks
- Use the `timeit` module or `pyperf` to benchmark single opcodes or small code fragments.
- Collect metrics such as execution time and opcode counts. Store results as JSON for easy comparison.
- Provide fixtures so tests fail if performance changes beyond a threshold.

## 4. Macro Benchmarks
- Run larger programs or existing Python benchmarks (e.g. from the `performance` suite) through the interpreter.
- Capture aggregate statistics (total instructions executed, elapsed time).
- Generate visualizations to highlight differences between Python versions.

## 5. Profiling Hooks
- Add optional instrumentation to the interpreter that records each opcode executed.
- Emit profiles that can be compared between 3.13 and 3.14 to see how bytecode changes impact execution flow.

## 6. Documentation and Reporting
- Document how to reproduce benchmarks and how results inform bytecode changes.
- Summarize findings in the repository (e.g. `docs/3.14_changes.md`). These reports can guide efforts to make Numba compatible with Python 3.14.

## 7. Continuous Integration Enhancements
- Extend `.github/workflows/compare-bytecode.yml` to run benchmarks in addition to tests.
- Upload benchmark results as workflow artifacts and fail the workflow if significant regressions are detected.

By implementing the above tasks, the test suite will evolve from simple correctness checks into a comprehensive benchmarking tool. The collected data can serve educational purposes and help Numba developers track Python 3.14 compatibility issues.
