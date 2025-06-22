# Egg Interpreter 🥚🐣

Egg is a minimalist, whimsical programming language inspired by eggs and birds — designed to be simple, fun, and easy to extend. It uses playful keywords like `yolk`, `shellmatch`, `carton`, and `hatch` to create a unique coding experience.

---

## Features

- **Variables** with `yolk` (assignment)
- **Pattern matching** with `shellmatch` / `case` / `default`
- **Arrays** called `carton` with methods (`append`, `pop`, `remove`)
- **Control flow**:
  - Conditional blocks with `if`/`else`/`endif`
  - Loops with `loop condition { ... }`
- **Functions** definition and calls with `fun`/`crackup` and `lay`
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
## Run Egg Code

- Install the Egg CLI globally:

```bash
npm install -g egglang-cli
```
Then run any .egg file:

```bash
egg run dino.egg
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
# Traditional fixed-size array
carton nest 3
fill nest at 0 with 10
hatch nest at 0  # outputs: 10

# Dynamic array initialization
carton eggs = [1, 2, 3]
eggs.append(4)      # [1, 2, 3, 4]
yolk first = eggs.pop()  # removes 4
eggs.remove(0)      # removes at index 0 → [2, 3]
```
## Control Flow
### if-else blocks
```bash
yolk x = 10
if x > 5:
    hatch "x is large"
else:
    hatch "x is small"
endif
```
### Loops
```bash
yolk i = 0;
loop i < 5 {
    yolk i = i + 1;
}
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
- The interpreter parses and executes Egg code line-by-line

- Variables are stored in environments (yolk assigns values)

- Arrays (carton) support:

  - Indexed access (at)

  - Dynamic methods (append, pop, remove)

  - Both fixed-size and dynamic initialization

- Control flow:

  - if/else/endif blocks

  - loop condition { ... } constructs

- Pattern matching uses shellmatch blocks

- Functions are defined as named code blocks and called with crackup

- Built-in EggTools functions extend language capabilities

- Simple error handling prints fragile: messages

## Contributing
Contributions, bug reports, and feature requests are welcome!

- Fork the repo

- Create a new branch

- Submit a pull request


## Example: Complete Egg Script
```bash

incubate utils.egg

# Array demo
carton eggs = [1, 2, 3];
eggs.append(4);
hatch len(eggs);  # 4
yolk num1 = eggs.pop();  # removes 4
yolk num2 = eggs.remove(0);  # removes at index 0 → [2, 3]
crackup add
crackup multiply

yolk num = 7
crackup is_even     # prints "Odd"


# Loop demo
yolk i = 0;
loop i < len(eggs) {
    hatch eggs at i
    yolk i = i + 1
}

# Conditional demo
if len(eggs) > 2:
    hatch "Plenty of eggs!"
else:
    hatch "Need more eggs!"
endif

# Function demo
fun greet
    hatch "Hello from an egg function!"
lay

crackup greet
```
---
## Easter Egg - 🥚 Eggspionage: Terminal Cam in ASCII

```bash
eggspionage
```
- Make sure you have opencv-python and numpy installed.
- Make sure you have web cam access enabled for vscode.
- Make sure to resize the terminal for a better experience.
- Use the slider to scroll to the bottom for current camera frames.
- By default, the terminal cam will render in base black text mode.<br>
- Here -c refers to color mode. Use one of r, g, b, m, d. r = red, g = green, b = blue, m = multicolor, d = dino mode 🦖🥚.

### Use VSCode terminal to run eggspionage for best experience.

Example:

```bash
eggspionage -c r
```

### Features:
- 📸 Live webcam feed rendered in ASCII

- 🌈 Optional color mode

- ⌨️ Cross-platform compatibility (macOS, Linux, Windows)

- 🧠 Automatically scales to your terminal size

- ✂️ Gracefully exits on Ctrl+C

---

## Inspiration
Egglang was originally hatched during a late-night coding session when I came across a devpost hackathon in San Antonio.The idea? To build a fun, minimalist programming language where every concept is inspired by eggs, birds, or both. What started as a joke in my mind, writing a program that begins with yolk and ends with a hatch, quickly made into a fully functional interpreter.

- The sheer absurdity of using phrases like crackup for defining functions
- To basically make it unique and funny, if it is.

## What it does
- Make simple programs currently with .egg extensions.

## How I built it
- Interpreter: Walked the AST and evaluated each node using Python classes.
- Features: Added variables (yolk), arrays (carton), pattern matching (shellmatch), functions (crackup, lay), and built-in utilities like eggtime().
- Extras: Added fun side commands like eggspionage — a secret easter egg animation when you run eggspionage in the CLI.

## Challenges I ran into
- Balancing silliness with actual usability, making sure Egglang wasn't just a joke, but something you could write real (simple) programs in.
- Designing syntax that feels "egg-themed" yet readable and intuitive
- Debugging parser edge cases when nesting blocks or working with user-defined functions

## Accomplishments that I am proud of
- The eggspionage easter egg, which is a terminal cam.
- Made a VS Code extension, which is not live on the vs code extensions store yet, but it supports .egg files language highlighting.

## What I learned
- Designing a readable syntax that balances fun with function
- Handling scope, pattern matching, arrays (aka cartons)
- Deploying it as a language installable using 
```bash
npm install -g egglang-cli
```

## What's next for EggLang
- Having more keywords and support like real languages maybe.
- Along with more easter eggs.

---

Thanks for cracking open Egg! 🥚🐣
