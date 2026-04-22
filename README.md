```
# 🚀 STEP — Smart Typing Enhancement Platform

> **Type less. Think more. Code faster.**

---

## 🧠 What is STEP?

**STEP (Smart Typing Enhancement Platform)** is a **system-wide typing engine** that enhances how you write code and text.

It acts as a **real-time layer between your keyboard and operating system**, enabling:

- ⚡ Instant code expansion  
- 🧠 Intelligent autocorrection  
- 🌍 Multi-language support  
- 🎯 Cursor-aware snippets  

Unlike IDE plugins, STEP works **everywhere**:

- VS Code  
- Notepad  
- Browser  
- Word / Google Docs  
- Terminal  

---

## ✨ Features

### ⚡ Smart Snippets

Type short triggers → get full syntax instantly:

```

> pr  →  printf("");
> if  →  if () {
> ...
> }

````

---

### 🎯 Cursor-Aware Editing

STEP intelligently places your cursor using the `|` marker:

```c
printf("|");
````

After expansion:

```c
printf();
        ^
```

---

### 🧠 Intelligent Autocorrect

Corrects common typing mistakes in real-time:

```
teh      → the
recieve  → receive
welcoma  → welcome
hhell    → hello
```

✔ Fast
✔ Context-aware
✔ Non-intrusive

---

### 🌍 Multi-Language Support

Switch languages instantly:

| Shortcut       | Language |
| -------------- | -------- |
| Ctrl + Alt + 1 | C        |
| Ctrl + Alt + 2 | Python   |
| Ctrl + Alt + 3 | C++      |

Each language has its own:

* syntax rules
* snippet system
* formatting

---

### 🔁 Mode System

STEP works in 3 modes:

| Mode    | Behavior            |
| ------- | ------------------- |
| Coding  | Snippets enabled    |
| Writing | Autocorrect enabled |
| Off     | STEP disabled       |

Switch mode using:

```
Ctrl + Alt + F10
```

---

### ⚙️ System-Wide Engine

Built using:

* `pynput` → global keyboard listener
* `Controller()` → input injection

STEP:

* captures keystrokes globally
* processes them in real-time
* injects corrected or expanded text

---

## 🏗️ How It Works

### 🔹 1. Input Capture

```python
kb.Listener(on_press=onPress, on_release=onRelease)
```

Captures all keyboard input system-wide.

---

### 🔹 2. Buffer System

```python
bufferKey
```

Stores the current typed word.

---

### 🔹 3. Pattern Detection

STEP checks:

* Is it a snippet? → `>pr`
* Is it a word? → `teh`
* Is it a delimiter? → space / enter

---

### 🔹 4. Action Engine

#### Coding Mode

```python
expandInstantly()
expandShortcut()
```

#### Writing Mode

```python
autoCorrectCurrentWord()
```

---

### 🔹 5. Smart Replacement

STEP:

1. Deletes original text
2. Injects new text
3. Positions cursor

---

## 🧩 Snippet Architecture

Each language uses a dictionary:

```python
c_keyPair = {
    ">pr": "printf(\"|\");",
    ">if": "if (|) {\n    \n}",
}
```

---

## 🧠 Autocorrect Engine

Uses:

```python
SpellChecker()
```

Enhanced with:

* similarity scoring
* typo filtering
* safe replacement logic

---

## 🧪 Example Workflow

### Coding Mode

```
>main
```

↓

```c
#include <stdio.h>

int main() {
    
    return 0;
}
```

---

### Writing Mode

```
recieve + space
```

↓

```
receive
```

---

## 🛠️ Installation

```bash
pip install pynput pyspellchecker
```

Run:

```bash
python main.py
```

---

## 🧪 Requirements

* Python 3.x
* Windows / Linux (X11 recommended for Linux)

---

## ⚠️ Notes

* Linux Wayland may block global input
* Some apps handle synthetic key input differently
* Run with proper permissions if needed

---

## 🚀 Future Enhancements

* 🔥 Tab navigation (`<1> <2>`)
* 🧠 Learning-based autocorrect
* ⚙️ Config file (user-defined snippets)
* 🖥️ GUI control panel
* 📦 EXE standalone app
* 🧩 Plugin system

---

## 💡 Vision

STEP is more than a tool.

It is a step toward:

> **A programmable typing layer over your OS**

A system that:

* understands your typing
* improves your speed
* adapts to your workflow

---

## 👨‍💻 Author

Built with ⚡ by Samar

---

## ⭐ Support

If you like STEP:

* Star ⭐ the repo
* Share 🚀
* Improve 🔧


---

If you want next upgrade:

👉 I can make this **insane GitHub profile style (badges + animations + neon theme)** 🚀
```
