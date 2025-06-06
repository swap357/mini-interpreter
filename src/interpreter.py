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

    def run(self):
        consts = self.code.co_consts
        names = self.code.co_names
        instructions = list(dis.Bytecode(self.code))
        while self.pc < len(instructions):
            instr = instructions[self.pc]
            self.pc += 1
            op_name = instr.opname
            arg = instr.arg
            handler = getattr(self, f'op_{op_name}', self.op_default)
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

    def op_CALL(self, arg, consts, names):
        args = [self.stack.pop() for _ in range(arg)]
        func = self.stack.pop()
        if self.stack and self.stack[-1] is None:
            self.stack.pop()
        result = func(*reversed(args))
        self.stack.append(result)

    def op_RESUME(self, arg, consts, names):
        pass

    def op_POP_TOP(self, arg, consts, names):
        self.stack.pop()

    def op_CACHE(self, arg, consts, names):
        pass

    def op_RETURN_VALUE(self, arg, consts, names):
        value = self.stack.pop()
        print(value)
        self.pc = len(self.code.co_code)  # exit loop

    def op_RETURN_CONST(self, arg, consts, names):
        self.pc = len(self.code.co_code)

    # Stubs for potential 3.14-only opcodes so interpreter doesn't crash
    def op_PUSH_NULL(self, arg, consts, names):
        self.stack.append(None)

    def op_RESUME_QUICK(self, arg, consts, names):
        pass

    def op_default(self, arg, consts, names):
        raise NotImplementedError(f"Opcode not implemented: {opcode.opname[self.code.co_code[self.pc-1]]}")


def main(path: str):
    with open(path) as f:
        source = f.read()
    code = compile(source, path, 'exec')
    MiniInterpreter(code).run()


if __name__ == '__main__':
    main(sys.argv[1])
