# Overview

Python code is compiled into bytecode which is executed by the CPython virtual
machine. Each code object contains a sequence of opcodes (`co_code`), constants,
variable names and more. The VM operates as a stack machine where most opcodes
push or pop values from an evaluation stack.

This project provides a toy interpreter and tools for examining bytecode to
better understand changes introduced in Python 3.14.
