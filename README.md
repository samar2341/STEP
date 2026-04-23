# 🚀 STEP — Smart Typing Enhancement Platform

> Type less. Think more. Code faster.

---

## 🧠 Overview

STEP (Smart Typing Enhancement Platform) is a **system-wide typing engine** that enhances both coding and writing workflows.

It works as a **real-time layer between your keyboard and the operating system**, allowing you to:

- Expand code instantly using shortcuts  
- Automatically correct typing mistakes  
- Switch between programming languages  
- Use smart cursor placement inside snippets  

Unlike editor plugins, STEP works **everywhere on your system**.

---

## ⚡ Key Features

### 1. Smart Code Snippets

Type short triggers to generate full syntax:


```

> pr  →  printf("");
> if  →  if () {
> ...
> }

````

No IDE dependency. Works globally.

---

### 2. Cursor-Aware Snippets

STEP uses a `|` marker to place the cursor exactly where you need it:

```c
printf("|");
````

After expansion:

```c
printf();
        ^
```

---

### 3. Intelligent Autocorrect

Automatically fixes common typing mistakes:

```
teh      → the
recieve  → receive
welcoma  → welcome
```

* Works in writing mode
* Avoids interfering with code
* Designed to be fast and minimal

---

### 4. Multi-Language Support

Switch between languages instantly:

| Shortcut       | Language |
| -------------- | -------- |
| Ctrl + Alt + 1 | C        |
| Ctrl + Alt + 2 | Python   |
| Ctrl + Alt + 3 | C++      |

Each language has its own:

* syntax rules
* snippet mappings
* formatting style

---

### 5. Mode System

STEP operates in three modes:

| Mode    | Behavior            |
| ------- | ------------------- |
| Coding  | Snippets enabled    |
| Writing | Autocorrect enabled |
| Off     | Disabled            |

Switch modes using:

```
Ctrl + Alt + .
```

---

## 🏗️ How It Works

STEP follows a simple pipeline:

1. Capture global keystrokes
2. Store characters in a buffer
3. Detect patterns (snippet or word)
4. Replace text intelligently

---

### Core Components

* **Keyboard Listener** → captures input globally
* **Buffer System** → tracks typed words
* **Snippet Engine** → expands shortcuts
* **Autocorrect Engine** → fixes words
* **Injector** → simulates typing

---

## 🧩 Example Snippet Mapping

```python
c_keyPair = {
    ">pr": "printf(\"|\");",
    ">if": "if (|) {\n    \n}",
}
```

---

## 🧪 Example Usage

### Coding Mode

Input:

```
>main
```

Output:

```c
#include <stdio.h>

int main() {
    
    return 0;
}
```

---

### Writing Mode

Input:

```
recieve + space
```

Output:

```
receive
```

---

## 🛠️ Installation

Install dependencies:

```bash
pip install pynput pyspellchecker
```

Run STEP:

```bash
python main.py
```

---

## 🧪 Requirements

* Python 3.x
* Windows or Linux (X11 recommended for Linux)

---

## ⚠️ Notes

* Wayland may block global input (use X11 on Linux)
* Some apps handle synthetic input differently
* Run with proper permissions if needed

---

## 🚀 Future Improvements

* Tab navigation between placeholders
* Learning-based autocorrect
* Config file for custom snippets
* GUI control panel
* Standalone executable

---

## 💡 Vision

STEP aims to become:

> A programmable typing layer over your operating system.

A tool that:

* understands your input
* improves your speed
* adapts to your workflow

---

## 👨‍💻 Author

**Built by Samar**

---

## ⭐ Support

If you like STEP:

* Star the repository
* Share it with others
* Contribute improvements

---
