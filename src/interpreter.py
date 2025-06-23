"""A tiny bytecode interpreter supporting a few Python opcodes."""

import opcode
import types
import sys
import dis


class MiniInterpreter:
    def __init__(self, code: types.CodeType):
        self.code = code
        self.stack = []
        self.pc = 0
        self.instructions = []
        self.offset_to_index = {}

    def run(self):
        consts = self.code.co_consts
        names = self.code.co_names
        self.instructions = list(dis.Bytecode(self.code))
        self.offset_to_index = {
            instr.offset: i for i, instr in enumerate(self.instructions)
        }
        while self.pc < len(self.instructions):
            instr = self.instructions[self.pc]
            self.pc += 1
            op_name = instr.opname
            arg = instr.arg
            handler = getattr(self, f'op_{op_name}', None)
            if handler is None:
                self.op_default(op_name, arg, consts, names)
            else:
                handler(arg, consts, names)

    # Opcode handlers -----------------------------------------------------
    def op_LOAD_CONST(self, arg, consts, names):
        self.stack.append(consts[arg])

    def op_LOAD_NAME(self, arg, consts, names):
        name = names[arg]
        value = globals().get(name, __builtins__.__dict__.get(name))
        self.stack.append(value)

    def op_STORE_NAME(self, arg, consts, names):
        name = names[arg]
        value = self.stack.pop()
        globals()[name] = value

    def op_BINARY_ADD(self, arg, consts, names):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(a + b)

    # --- Control flow and comparison opcodes ---

    def op_GET_ITER(self, arg, consts, names):
        iterable = self.stack.pop()
        self.stack.append(iter(iterable))

    def op_FOR_ITER(self, arg, consts, names):
        instr = self.instructions[self.pc - 1]
        target = self.offset_to_index[instr.argval]
        iterator = self.stack[-1]
        try:
            value = next(iterator)
            self.stack.append(value)
        except StopIteration:
            self.pc = target
            self.stack.append(None)

    def op_JUMP_BACKWARD(self, arg, consts, names):
        instr = self.instructions[self.pc - 1]
        target = self.offset_to_index[instr.argval]
        self.pc = target

    def op_END_FOR(self, arg, consts, names):
        # iterator is below the sentinel pushed by FOR_ITER
        if len(self.stack) >= 2:
            self.stack.pop(-2)

    def op_COMPARE_OP(self, arg, consts, names):
        instr = self.instructions[self.pc - 1]
        op = instr.argval
        b = self.stack.pop()
        a = self.stack.pop()
        if op == '<':
            self.stack.append(a < b)
        elif op == '<=':
            self.stack.append(a <= b)
        elif op == '==':
            self.stack.append(a == b)
        elif op == '!=':
            self.stack.append(a != b)
        elif op == '>':
            self.stack.append(a > b)
        elif op == '>=':
            self.stack.append(a >= b)
        else:
            raise NotImplementedError(f"COMPARE_OP {op}")

    def op_POP_JUMP_IF_FALSE(self, arg, consts, names):
        value = self.stack.pop()
        if not value:
            instr = self.instructions[self.pc - 1]
            target = self.offset_to_index[instr.argval]
            self.pc = target

    def op_CALL(self, arg, consts, names):
        args = [self.stack.pop() for _ in range(arg)]
        func = self.stack.pop()
        if func is None:
            func = self.stack.pop()
        elif self.stack and self.stack[-1] is None:
            self.stack.pop()
        result = func(*reversed(args))
        self.stack.append(result)

    def op_RESUME(self, arg, consts, names):
        pass

    def op_POP_TOP(self, arg, consts, names):
        self.stack.pop()

    def op_CACHE(self, arg, consts, names):
        pass

    def op_PRECALL(self, arg, consts, names):
        pass

    def op_RETURN_VALUE(self, arg, consts, names):
        self.stack.pop()
        self.pc = len(self.code.co_code)  # exit loop

    def op_RETURN_CONST(self, arg, consts, names):
        self.pc = len(self.code.co_code)

    # Stubs for potential 3.14-only opcodes so interpreter doesn't crash
    def op_PUSH_NULL(self, arg, consts, names):
        self.stack.append(None)

    def op_RESUME_QUICK(self, arg, consts, names):
        pass

    def op_default(self, op_name, arg, consts, names):
        raise NotImplementedError(f"Opcode not implemented: {op_name}")


def main(path: str):
    with open(path) as f:
        source = f.read()
    code = compile(source, path, 'exec')
    MiniInterpreter(code).run()


if __name__ == '__main__':
    main(sys.argv[1])
