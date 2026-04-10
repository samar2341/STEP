# STEP — Smart Typing Enhancement Platform

## 🚀 Overview

STEP (Smart Typing Enhancement Platform) is a cross-platform keyboard mediation system designed to improve programming efficiency. It intercepts keyboard input, expands coding shortcuts, corrects common typing mistakes, and adapts based on user behavior.

Instead of typing full syntax repeatedly, users can type short triggers like `>pr` and STEP expands them into full code like `printf("");`.

---

## 🎯 Objectives

* Reduce repetitive typing in programming
* Increase coding speed and efficiency
* Minimize typing errors
* Provide adaptive suggestions based on usage
* Create a system-level keyboard enhancement tool

---

## 🧠 Core Features

### 1. Shortcut Expansion

Users can define shortcuts prefixed with `>`.

Examples:

* `>pr` → `printf("");`
* `>w` → `while`
* `>if` → `if () { }`

Expansion is triggered on:

* Space
* Enter
* Tab

---

### 2. Global Keyboard Mediation

STEP works across applications (VS Code, Notepad, browser inputs) by:

* Listening to global keyboard input
* Processing input using rules
* Injecting modified output

---

### 3. ON/OFF Toggle

* Toggle using a hotkey (e.g., F8)
* When OFF → normal keyboard behavior
* When ON → smart features active

---

### 4. Typo Detection & Correction

STEP tracks common mistakes and can auto-correct:

* `retrun` → `return`
* `pritnf` → `printf`

---

### 5. Usage Tracking

STEP monitors:

* Frequently used shortcuts
* Repeated patterns
* Backspace-heavy sequences

---

### 6. Adaptive Suggestions

Based on usage:

* Suggest shorter shortcuts
* Recommend corrections
* Highlight inefficient typing patterns

---

## ⚙️ System Architecture

Keyboard → Listener → Buffer → Rule Engine → Injector → Application

### Components:

* **Listener**: Captures keystrokes
* **Buffer**: Stores recent input
* **Rule Engine**: Matches shortcuts and errors
* **Injector**: Outputs modified text
* **Stats Module**: Tracks usage and mistakes

---

## 🛠️ Tech Stack

* Python
* pynput (keyboard listening & control)
* tkinter (optional UI)
* JSON (configuration storage)

---

## 📦 Installation

```bash
pip install pynput
```

Run the program:

```bash
python main.py
```

---

## ▶️ Usage

1. Start STEP
2. Ensure it is ACTIVE
3. Type shortcuts using `>` prefix
4. Press space/enter to expand

Example:

```
>pr ␣ → printf("");
```

---

## 📊 Example Shortcut Config

```json
{
  ">pr": "printf(\"\");",
  ">w": "while",
  ">if": "if () {\n    \n}"
}
```

---

## ⚠️ Limitations / Flaws

### 1. OS-Level Restrictions

* Some applications block synthetic input
* macOS may require accessibility permissions
* Linux may require elevated privileges

### 2. Not Truly Low-Level

* Uses high-level hooks (pynput)
* Not a full kernel-level mediator

### 3. Potential Input Conflicts

* `>` is a valid programming symbol
* Must carefully avoid false triggers

### 4. Performance Overhead

* Continuous key listening may use CPU
* Large rule sets can slow matching

### 5. Limited Context Awareness

* Does not fully understand programming language context
* Cannot differentiate all scenarios automatically

### 6. Error Detection Simplicity

* Basic typo correction
* Not full NLP or AI-based system

---

## ⚠️ Risks & Challenges

* Key injection may behave inconsistently across OS
* Debugging keyboard hooks can be difficult
* Race conditions in fast typing scenarios
* Buffer synchronization issues

---

## 🔮 Future Improvements

* AI-based typo correction
* Language-specific expansion (C, Python, JS)
* GUI dashboard with analytics
* Custom user-defined mappings
* Plugin system
* Integration with IDEs
* Performance optimization with lower-level APIs

---

## 🏁 Conclusion

STEP is a powerful prototype that demonstrates how keyboard input can be enhanced intelligently to improve programming efficiency. While the current implementation focuses on rule-based expansion and basic adaptation, it lays the foundation for a more advanced, intelligent typing system.

---

## 👨‍💻 Author

Samar 

---

## 📜 License

This project is for educational purposes.
