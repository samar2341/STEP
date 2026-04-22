
```
# STEP — Smart Typing Enhancement Platform

A system-wide typing engine for faster coding. Type shortcuts, get full snippets. Works everywhere — VS Code, terminal, browser, text editors.

## What it does

- Type `>pr` → get `printf("");`
- Autocorrect typos as you type
- Works globally (not just in your IDE)
- Support for C, Python, C++, and more

---

## Features

### Smart Snippets

Short triggers expand to full code:

```
>pr   →  printf("");
>if   →  if () {
           }
>main →  int main() {
             return 0;
         }
```

### Autocorrect

Real-time typo fixing:

```
teh      → the
recieve  → receive
hhell    → hello
```

### Multi-Language

Switch between C, Python, C++ with keyboard shortcuts.

### Mode System

- **Coding Mode**: Snippets on
- **Writing Mode**: Autocorrect on  
- **Off**: Disabled

---

## How It Works

1. **Listens** to all keyboard input globally
2. **Buffers** the current word being typed
3. **Detects** if it's a snippet trigger or misspelling
4. **Replaces** the text with the expansion or correction
5. **Positions** cursor in the right place

Uses `pynput` for keyboard listening and text injection.

---

## Snippet Architecture

Each language has a dictionary of triggers:

```python
c_keyPair = {
    ">pr": "printf(\"|\")",
    ">if": "if (|) {\n    \n}",
}
```

The `|` marks where the cursor goes after expansion.

---

## Autocorrect Engine

Uses `SpellChecker()` with similarity scoring to catch typos safely. Only corrects common mistakes.

---

## Example Workflow

Type `>main` in Coding Mode:

```c
#include <stdio.h>

int main() {
    
    return 0;
}
```

Type `recieve` in Writing Mode → autocorrects to `receive`

---

## Installation

```bash
pip install pynput pyspellchecker
python main.py
```

---

## Requirements

- Python 3.x
- Windows / Linux (X11)

---

## Notes

- Wayland may not work on Linux
- Some apps handle synthetic input differently

---

## Future Ideas

- Tab navigation for cursor stops
- Config file for custom snippets
- GUI control panel
- Standalone EXE

---

## Author

Built by Samar
```
