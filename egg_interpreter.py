import re
import random
import time
import os

global_env = {}
functions = {}
arrays = {}
call_stack = []


def current_env():
    return call_stack[-1] if call_stack else global_env


def yolk(var_name, value):
    env = current_env()
    env[var_name] = value


def fill_carton(array_name, index, value):
    if array_name not in arrays:
        print(f"fragile: carton '{array_name}' not found")
        return
    if not (0 <= index < len(arrays[array_name])):
        print(f"fragile: carton index {index} out of range")
        return
    arrays[array_name][index] = value


def get_carton_value(array_name, index):
    if array_name not in arrays:
        print(f"fragile: carton '{array_name}' not found")
        return 0
    if not (0 <= index < len(arrays[array_name])):
        print(f"fragile: carton index {index} out of range")
        return 0
    return arrays[array_name][index]


def eval_expr(expr):
    expr = expr.strip()
    # Handle string literals
    if (expr.startswith('"') and expr.endswith('"')) or (expr.startswith("'") and expr.endswith("'")):
        return expr[1:-1]
    if expr.startswith('(') and expr.endswith(')'):
        return eval_expr(expr[1:-1])

    # array access
    array_access_match = re.match(r'(\w+)\s+at\s+(\d+)', expr)
    if array_access_match:
        arr_name = array_access_match.group(1)
        idx = int(array_access_match.group(2))
        return get_carton_value(arr_name, idx)

    # function calls for eggtools: e.g. len(x), random(1,5)
    func_call_match = re.match(r'(\w+)\((.*?)\)', expr)
    if func_call_match:
        func_name = func_call_match.group(1)
        args_str = func_call_match.group(2)
        args = [eval_expr(arg.strip()) for arg in args_str.split(',')] if args_str else []
        return eggtools_call(func_name, args)

    tokens = expr.split()
    if len(tokens) == 1:
        # variable or int
        try:
            return int(tokens[0])
        except ValueError:
            env = current_env()
            return env.get(tokens[0], global_env.get(tokens[0], 0))
    elif len(tokens) == 3:
        a = eval_expr(tokens[0])
        op = tokens[1]
        b = eval_expr(tokens[2])
        if op == 'crack':
            return a + b
        elif op == 'scramble':
            return a - b
        elif op == 'roll':
            return a * b
        elif op == 'split':
            return a / b
        elif op == 'mod':
            return a % b
        elif op == 'pow':
            return a ** b
    return 0


def boil(var1, comp, var2, dest):
    env = current_env()
    a = env.get(var1, global_env.get(var1, 0))
    b = env.get(var2, global_env.get(var2, 0))
    if comp == '==':
        env[dest] = a == b
    elif comp == '>':
        env[dest] = a > b
    elif comp == '<':
        env[dest] = a < b
    elif comp == '!=':
        env[dest] = a != b
    elif comp == '>=':
        env[dest] = a >= b
    elif comp == '<=':
        env[dest] = a <= b


def hatch(message):
    env = current_env()
    if message.startswith('"') or message.startswith("'"):
        print(message.strip('"\''))
    else:
        array_access_match = re.match(r'(\w+)\s+at\s+(\d+)', message)
        if array_access_match:
            arr_name = array_access_match.group(1)
            idx = int(array_access_match.group(2))
            val = get_carton_value(arr_name, idx)
            print(val)
        else:
            print(env.get(message, global_env.get(message, f"Undefined: {message}")))


def handle_if_block(lines, index):
    condition_var = lines[index].split()[1]
    env = current_env()
    cond = env.get(condition_var, global_env.get(condition_var, False))
    i = index + 1
    if cond:
        while i < len(lines) and lines[i].strip() not in ['endif', 'else']:
            interpret_line(lines[i])
            i += 1
        while i < len(lines) and lines[i].strip() != 'endif':
            i += 1
        return i + 1
    else:
        while i < len(lines) and lines[i].strip() not in ['else', 'endif']:
            i += 1
        if i < len(lines) and lines[i].strip() == 'else':
            i += 1
            while i < len(lines) and lines[i].strip() != 'endif':
                interpret_line(lines[i])
                i += 1
            return i + 1
        else:
            return i + 1


def handle_loop(lines, index):
    condition_var = lines[index].split()[1]
    loop_body = []
    i = index + 1
    while i < len(lines) and lines[i].strip() != 'hatch':
        loop_body.append(lines[i])
        i += 1
    env = current_env()
    while env.get(condition_var, global_env.get(condition_var, False)):
        for stmt in loop_body:
            interpret_line(stmt)
    return i + 1


def handle_function_def(lines, index):
    func_name = lines[index].split()[1]
    body = []
    i = index + 1
    while i < len(lines) and lines[i].strip() != 'lay':
        body.append(lines[i])
        i += 1
    functions[func_name] = body
    return i + 1


def handle_function_call(func_name):
    if func_name not in functions:
        print(f"crackup: Undefined function {func_name}")
        return
    call_stack.append({})
    for line in functions[func_name]:
        interpret_line(line)
    call_stack.pop()


def handle_shellmatch(lines, index):
    header = lines[index].strip()
    _, var_name = header.split(maxsplit=1)
    cases = {}
    i = index + 1
    current_case = None
    case_block = []

    def save_case():
        nonlocal current_case, case_block
        if current_case is not None:
            cases[current_case] = case_block
        current_case = None
        case_block = []

    while i < len(lines) and lines[i].strip() != 'endshell':
        line = lines[i].strip()
        case_match = re.match(r'case\s+["\'](.+)["\']\s*:', line)
        if case_match:
            save_case()
            current_case = case_match.group(1)
        elif line == 'default:':
            save_case()
            current_case = 'default'
        else:
            case_block.append(lines[i])
        i += 1
    save_case()

    env = current_env()
    val = env.get(var_name, global_env.get(var_name, None))
    if val is None:
        print(f"fragile: shellmatch var '{var_name}' undefined")
        return i + 1

    block_to_run = cases.get(val, cases.get('default', []))
    for stmt in block_to_run:
        interpret_line(stmt)
    return i + 1


# --- NEW: EggTools built-in functions ---

def eggtools_call(func_name, args):
    if func_name == 'len':
        # support string or list
        if isinstance(args[0], str):
            return len(args[0])
        elif isinstance(args[0], list):
            return len(args[0])
        else:
            return 0
    elif func_name == 'type':
        val = args[0]
        if isinstance(val, str):
            return 'string'
        elif isinstance(val, int):
            return 'int'
        elif isinstance(val, list):
            return 'list'
        else:
            return type(val).__name__
    elif func_name == 'random':
        if len(args) == 2:
            return random.randint(args[0], args[1])
        else:
            return random.random()
    elif func_name == 'eggtime':
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    else:
        print(f"fragile: unknown eggtools function '{func_name}'")
        return None


# --- NEW: Modules / Imports ---

def handle_incubate(line):
    # Syntax: incubate filename.egg
    parts = line.split()
    if len(parts) != 2:
        print("fragile: invalid incubate syntax")
        return
    filename = parts[1]
    if not os.path.isfile(filename):
        print(f"fragile: cannot find file '{filename}'")
        return
    with open(filename, 'r') as f:
        code = f.read()
    run_egglang(code)


def interpret_line(line):
    tokens = line.strip().split()
    if not tokens:
        return

    cmd = tokens[0]

    try:
        if cmd == 'incubate':
            handle_incubate(line)

        elif cmd == 'yolk':
            var_name = tokens[1]
            if tokens[2] == '=':
                expr = ' '.join(tokens[3:])
                value = eval_expr(expr)
                yolk(var_name, value)

        elif cmd == 'crackup':
            func_name = tokens[1]
            handle_function_call(func_name)

        elif cmd == 'shellmatch':
            # shellmatch block spans multiple lines
            # will be handled externally
            pass

        elif cmd == 'carton':
            # create array
            arr_name = tokens[1]
            size = int(tokens[2])
            arrays[arr_name] = [0] * size

        elif cmd == 'fill':
            # fill carton at index with value
            arr_name = tokens[1]
            if tokens[2] != 'at':
                print("fragile: syntax error in fill")
                return
            idx = int(tokens[3])
            if tokens[4] != 'with':
                print("fragile: syntax error in fill")
                return
            val_expr = ' '.join(tokens[5:])
            val = eval_expr(val_expr)
            fill_carton(arr_name, idx, val)

        elif cmd == 'hatch':
            msg = ' '.join(tokens[1:])
            hatch(msg)

        else:
            # catch other simple commands
            pass

    except Exception as e:
        print(f"fragile: error processing line '{line}': {e}")


def run_egglang(code):
    lines = code.strip().split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line or line.startswith('#'):
            i += 1
            continue

        if line.startswith('shellmatch'):
            i = handle_shellmatch(lines, i)
        else:
            interpret_line(line)
            i += 1


if __name__ == '__main__':
    sample = '''
incubate utils.egg

yolk action = "crack"
shellmatch action
  case "crack":
    hatch "Breaking stuff"
  case "hatch":
    hatch "Output detected"
  default:
    hatch "Unknown behavior"
endshell

carton nest 3
fill nest at 0 with 10
hatch nest at 0

yolk r = random(1,10)
hatch r

yolk t = eggtime()
hatch t
'''
    run_egglang(sample)
