# Egg Interpreter 🥚🐣

Egg is a minimalist, whimsical programming language inspired by eggs and birds — designed to be simple, fun, and easy to extend. It uses playful keywords like `yolk`, `shellmatch`, `carton`, and `hatch` to create a unique coding experience.

---

## Features

- **Variables** with `yolk` (assignment)
- **Pattern matching** with `shellmatch` / `case` / `default`
- **Arrays** called `carton`
- **Control flow** with simple conditional blocks
- **Functions** definition and calls with `crackup` and `lay`
- **Built-in utilities** (`random()`, `eggtime()`, `len()`, `type()`)
- **File inclusion** with `incubate filename.egg`
- Simple **output** via `hatch`

---

## Getting Started

### Requirements

- Python 3.x
- Node.js (for the CLI and VSCode extension)
- VS Code (to use the extension)

---
### Run Egg Code

### 🔹 Option 1: Directly via Python

```bash
python core/egg_interpreter.py path/to/script.egg
```

### 🔹 Option 2: Using the CLI (recommended)

- Clone the repo:

```bash
git clone git@github.com:jayanth920/egglang.git
```

or 

```bash
git clone https://github.com/jayanth920/egglang.git
```

- Install locally (In the repo directory):

```bash
cd runner
npm link
```

- Then run any .egg file:

```bash
egg run hello.egg
```
---

## Egg Language Syntax Examples
### Variable Assignment

```bash
yolk x = 5
yolk greeting = "hello"
```

### Pattern Matching
```bash
yolk action = "crack"

shellmatch action
  case "crack":
    hatch "Breaking stuff"
  case "hatch":
    hatch "Output detected"
  default:
    hatch "Unknown behavior"
endshell
```

### Arrays (carton)
```bash
carton nest 3
fill nest at 0 with 10
hatch nest at 0  # outputs: 10
```

## Functions

### Define a function:

```bash
crackup say_hello
  hatch "Hello from Egg!"
lay
```

### Call a function:

```bash
crackup say_hello
```

### Built-in Functions
- random(a, b) — random int between a and b

- eggtime() — current timestamp string

- len(x) — length of string or list

- type(x) — type name of value

## File Inclusion
- Use incubate filename.egg to include and run another Egg file.

### How It Works (Under the Hood)
- The interpreter parses and executes Egg code line-by-line.

- Variables are stored in environments (yolk assigns values).

- Arrays (carton) support indexed access and mutation.

- Pattern matching uses shellmatch blocks.

- Functions are defined as named code blocks and called with crackup.

- Built-in EggTools functions extend language capabilities.

- Simple error handling prints fragile: messages.

## Contributing
Contributions, bug reports, and feature requests are welcome!

- Fork the repo

- Create a new branch

- Submit a pull request


## Example: Complete Egg Script
```bash

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
```

Thanks for cracking open Egg! 🥚🐣

