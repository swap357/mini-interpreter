import sys
import json
import dis


def dump_bytecode(path):
    source = open(path).read()
    code = compile(source, path, 'exec')
    bc = list(dis.Bytecode(code))
    fmt = [
        {
            'offset': instr.offset,
            'opname': instr.opname,
            'argrepr': instr.argrepr,
        }
        for instr in bc
    ]
    print(json.dumps(fmt, indent=2))


if __name__ == '__main__':
    dump_bytecode(sys.argv[1])
