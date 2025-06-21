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
    # print(f"get_carton_value({array_name}, {index})")  # <== DEBUG
    if array_name not in arrays:
        print(f"fragile: carton '{array_name}' not found")
        return 0
    if not (0 <= index < len(arrays[array_name])):
        print(f"fragile: carton index {index} out of range")
        return 0
    return arrays[array_name][index]

def split_args(args_str):
    args = []
    current = ''
    depth = 0
    in_quotes = False
    quote_char = ''

    for ch in args_str:
        if ch in ('"', "'"):
            if in_quotes:
                if ch == quote_char:
                    in_quotes = False
            else:
                in_quotes = True
                quote_char = ch
            current += ch
        elif ch == ',' and depth == 0 and not in_quotes:
            args.append(current.strip())
            current = ''
        else:
            if ch == '(' and not in_quotes:
                depth += 1
            elif ch == ')' and not in_quotes and depth > 0:
                depth -= 1
            current += ch
    if current.strip():
        args.append(current.strip())
    return args


def eval_expr(expr):
    expr = expr.strip()

    # Handle string literals
    if (expr.startswith('"') and expr.endswith('"')) or (expr.startswith("'") and expr.endswith("'")):
        return expr[1:-1]

    # Strip outermost parentheses if they wrap the entire expression
    while expr.startswith('(') and expr.endswith(')'):
        # Check that the parentheses are actually wrapping the whole expression
        depth = 0
        matched = True
        for i, ch in enumerate(expr):
            if ch == '(':
                depth += 1
            elif ch == ')':
                depth -= 1
                if depth == 0 and i != len(expr) - 1:
                    matched = False
                    break
        if matched:
            expr = expr[1:-1].strip()
        else:
            break

    # array access
    array_access_match = re.match(r'(\w+)\s+at\s+(.+)', expr)
    if array_access_match:
        arr_name = array_access_match.group(1)
        idx_expr = array_access_match.group(2).strip()
        idx = eval_expr(idx_expr)
        return get_carton_value(arr_name, idx)

    # function calls like len(x), random(1,5)
    func_call_match = re.match(r'(\w+)\((.*?)\)', expr)
    if func_call_match:
        func_name = func_call_match.group(1)
        args_str = func_call_match.group(2)
        # print(f"DEBUG: func call {func_name} with args {args_str!r}")
        args = [eval_expr(arg) for arg in split_args(args_str)] if args_str else []
        # print(f"DEBUG: evaluated args = {args}")
        return eggtools_call(func_name, args)

    # Tokenize and evaluate
    tokens = expr.split()
    if len(tokens) == 1:
        try:
            return int(tokens[0])
        except ValueError:
            if tokens[0] in arrays:
                return arrays[tokens[0]]

            env = current_env()
            val = env.get(tokens[0], global_env.get(tokens[0], None))
            if val is None:
                print(f"fragile: variable '{tokens[0]}' is undefined")
                return 0
            return val

    try:
        result = eval_expr(tokens[0])
        i = 1
        while i < len(tokens) - 1:
            op = tokens[i]
            right = eval_expr(tokens[i + 1])
            # print(f"eval: {result} {op} {right}")
            if op == '+':
                result += right
            elif op == 'scramble':
                result -= right
            elif op == 'roll':
                result *= right
            elif op == 'split':
                result /= right
            elif op == 'mod':
                result %= right
            elif op == 'pow':
                result **= right
            elif op == '<':
                result = int(result < right)
            elif op == '>':
                result = int(result > right)
            elif op == '==':
                result = int(result == right)
            elif op == '!=':
                result = int(result != right)
            elif op == '<=':
                result = int(result <= right)
            elif op == '>=':
                result = int(result >= right)
            else:
                print(f"fragile: unknown operator '{op}'")
                return 0
            i += 2
        return result
    except Exception as e:
        print(f"fragile: error in eval_expr('{expr}'): {e}")
        return 0



def boil(var1, comp, var2, dest):
    env = current_env()
    a = eval_expr(var1)
    b = eval_expr(var2)
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
    message = message.strip()
    if (message.startswith('"') and message.endswith('"')) or (message.startswith("'") and message.endswith("'")):
        print(message.strip('"\''))
    else:
        val = eval_expr(message)
        print(val)

def handle_if_block(lines, index):
    # Example: if x > 5:
    condition_expr = lines[index][3:-1].strip()  # remove 'if ' and trailing ':'
    cond = eval_expr(condition_expr)
    i = index + 1
    if cond:
        # Execute lines until else: or endif
        while i < len(lines) and lines[i] not in ('else:', 'endif'):
            interpret_line(lines[i], lines, i)
            i += 1
        # Skip else block if exists
        if i < len(lines) and lines[i] == 'else:':
            while i < len(lines) and lines[i] != 'endif':
                i += 1
        if i < len(lines) and lines[i] == 'endif':
            return i + 1
        else:
            return i
    else:
        # Skip if block until else: or endif
        while i < len(lines) and lines[i] not in ('else:', 'endif'):
            i += 1
        # Execute else block if exists
        if i < len(lines) and lines[i] == 'else:':
            i += 1
            while i < len(lines) and lines[i] != 'endif':
                interpret_line(lines[i], lines, i)
                i += 1
        if i < len(lines) and lines[i] == 'endif':
            return i + 1
        else:
            return i
        
        
def handle_loop(lines, index):
    line = lines[index].strip()
    if not line.endswith('{'):
        print("fragile: syntax error in loop, missing '{'")
        return index + 1

    condition_expr = line[len('loop'):].strip()
    condition_expr = condition_expr[:-1].strip()

    loop_body = []
    i = index + 1
    brace_count = 1

    while i < len(lines) and brace_count > 0:
        current_line = lines[i].strip()
        if current_line.endswith('{'):
            brace_count += 1
        if current_line == '}':
            brace_count -= 1
            i += 1
            if brace_count == 0:
                break
            else:
                continue
        if brace_count > 0:
            loop_body.append(lines[i])
        i += 1

    env = current_env()
    while eval_expr(condition_expr):
        j = 0
        while j < len(loop_body):
            ret = interpret_line(loop_body[j], loop_body, j)
            j = ret if ret is not None else j + 1

    return i



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
    func_body = functions[func_name]
    i = 0
    while i < len(func_body):
        ret = interpret_line(func_body[i], func_body, i)
        i = ret if ret is not None else i + 1
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
    j = 0
    while j < len(block_to_run):
        ret = interpret_line(block_to_run[j], block_to_run, j)
        j = ret if ret is not None else j + 1
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


def interpret_line(line, lines=None, current_index=None):
    line = line.strip()
    if not line or line.startswith('#'):  # <-- ADD THIS LINE
        return
    
    # Now each line is a single statement ending with ';' removed in run_egglang
    tokens = line.split()
    if not tokens:
        return

    cmd = tokens[0]

    try:
        if cmd == 'yolk':
            # syntax: yolk var = expr;
            var_name = tokens[1]
            if tokens[2] == '=':
                expr = ' '.join(tokens[3:])
                value = eval_expr(expr)
                yolk(var_name, value)

        elif cmd == 'boil':
            # syntax: boil var1 comp var2 dest;
            if len(tokens) != 5:
                print("fragile: invalid boil syntax")
                return
            var1, comp, var2, dest = tokens[1:]
            boil(var1, comp, var2, dest)

        elif cmd == 'hatch':
            msg = ' '.join(tokens[1:])
            hatch(msg)

        elif cmd == 'carton':
            # two syntaxes possible:
            # 1) carton arr 5;
            # 2) carton a = [12, 13, "Jay"];
            rest = line[len('carton'):].strip()
            # check if '=' is in rest
            if '=' in rest:
                # parse "a = [12, 13, "Jay"]"
                parts = rest.split('=', 1)
                arr_name = parts[0].strip()
                array_str = parts[1].strip()
                # array_str should start with '[' and end with ']'
                if array_str.startswith('[') and array_str.endswith(']'):
                    # parse the contents inside []
                    content = array_str[1:-1].strip()
                    # split by commas outside quotes
                    elems = split_args(content)
                    parsed_elems = []
                    for e in elems:
                        e = e.strip()
                        # if string literal
                        if (e.startswith('"') and e.endswith('"')) or (e.startswith("'") and e.endswith("'")):
                            parsed_elems.append(e[1:-1])
                        else:
                            # try int
                            try:
                                parsed_elems.append(int(e))
                            except ValueError:
                                # fallback: evaluate expression (variable or function call)
                                parsed_elems.append(eval_expr(e))
                    arrays[arr_name] = parsed_elems
                else:
                    print("fragile: invalid carton initialization syntax")
                    return
            else:
                # old syntax: carton arr 5;
                parts = rest.split()
                if len(parts) != 2:
                    print("fragile: invalid carton syntax")
                    return
                arr_name = parts[0]
                size = int(parts[1])
                arrays[arr_name] = [0] * size

        elif cmd == 'fill':
            arr_name = tokens[1]
            if tokens[2] != 'at' or tokens[4] != 'with':
                print("fragile: syntax error in fill")
                return
            idx = eval_expr(tokens[3])
            val_expr = ' '.join(tokens[5:])
            val = eval_expr(val_expr)
            fill_carton(arr_name, idx, val)

        elif cmd == 'crackup':
            func_name = tokens[1]
            handle_function_call(func_name)

        elif cmd == 'fun':
            return handle_function_def(lines, current_index)

        elif cmd == 'loop':
            return handle_loop(lines, current_index)
        
        elif cmd == 'incubate':
            handle_incubate(line)
            

        else:
            print(f"fragile: unknown command '{cmd}'")

    except Exception as e:
        print(f"fragile: error processing line '{line}': {e}")

def run_egglang(code):
    # Split physical lines by ';' so each statement ends with ;
    raw_lines = code.strip().split('\n')
    # Flatten all statements split by ';' into single list of logical lines
    lines = []
    for raw_line in raw_lines:
        parts = [p.strip() for p in raw_line.split(';') if p.strip()]
        lines.extend(parts)

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line or line.startswith('#'):
            i += 1
            continue

        if line.startswith('shellmatch'):
            i = handle_shellmatch(lines, i)
        elif line.startswith('if ') and line.endswith(':'):
            i = handle_if_block(lines, i)
        elif line == 'else:':
            # else is handled inside handle_if_block, skip here
            i += 1
        else:
            ret = interpret_line(line, lines, i)
            i = ret if ret is not None else i + 1



if __name__ == '__main__':
    # 1. Simple variable assignment and hatch
    sample1 = '''
    yolk x = 42;
    hatch x;
    '''
    run_egglang(sample1)
    print("\n----------------\n")

    # 2. Simple loop printing 0 to 4
    sample2 = '''
    yolk i = 0;
    loop i < 5 {
    hatch i;
    yolk i = i + 1;
    }
    '''
    run_egglang(sample2)
    print("\n----------------\n")

    # 3. Loop inside function
    sample3 = '''
    fun countUp
    yolk i = 0;
    loop i < 5 {
        hatch i;
        yolk i = i + 1;
    }
    lay;

    crackup countUp;
    '''
    run_egglang(sample3)
    print("\n----------------\n")

    # 4. Function with parameters simulated by globals (no real params yet)
    sample4 = '''
    yolk limit = 3;

    fun countLimit
    yolk i = 0;
    loop i < limit {
        hatch i;
        yolk i = i + 1;
    }
    lay;

    crackup countLimit;
    '''
    run_egglang(sample4)
    print("\n----------------\n")

    # 5. Using carton (array) and fill, then print elements
    sample5 = '''
    carton arr 3;
    fill arr at 0 with 10;
    fill arr at 1 with 20;
    fill arr at 2 with 30;

    yolk i = 0;
    loop i < 3 {
    hatch arr at i;
    yolk i = i + 1;
    }
    '''
    run_egglang(sample5)
    print("\n----------------\n")

    # 6. Conditional if-else block
    sample6 = '''
    yolk x = 5;
    if x > 3:
    hatch "x is greater than 3";
    else:
    hatch "x is 3 or less";
    endif;
    '''
    run_egglang(sample6)
    print("\n----------------\n")

    # 7. Boil comparison and hatch result
    sample7 = '''
    yolk a = 7;
    yolk b = 5;
    boil a > b res;
    hatch res;
    '''
    run_egglang(sample7)
    print("\n----------------\n")

    # 8. Shellmatch with cases and default
    sample8 = '''
    yolk animal = "cat";

    shellmatch animal
    case "dog":
        hatch "It's a dog";
    case "cat":
        hatch "It's a cat";
    default:
        hatch "Unknown animal";
    endshell;
    '''
    run_egglang(sample8)
    print("\n----------------\n")

    # 9. Function calling another function
    sample9 = '''
    fun inner
    hatch "Inner function";
    lay;

    fun outer
    hatch "Outer function start";
    crackup inner;
    hatch "Outer function end";
    lay;

    crackup outer;
    '''
    run_egglang(sample9)
    print("\n----------------\n")

    # 10. Loop modifying array elements
    sample10 = '''
    carton nums 5;
    yolk i = 0;
    loop i < 5 {
    fill nums at i with i roll 2;  # multiply by 2
    yolk i = i + 1;
    }

    yolk j = 0;
    loop j < 5 {
    hatch nums at j;
    yolk j = j + 1;
    }
    '''
    run_egglang(sample10)
    print("\n----------------\n")

    sample_new_carton = '''
    carton a = [12, 13, "Jay"];

    yolk i = 0;
    loop i < len(a) {
    hatch a at i;
    yolk i = i + 1;
    }
    '''

    run_egglang(sample_new_carton)
    print("\n----------------\n")