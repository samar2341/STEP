import sys
import time
import re
import difflib
from spellchecker import SpellChecker
from pynput import keyboard as kb

try:
    import ctypes
except ImportError:
    ctypes = None

spell = SpellChecker(distance=2)
controller = kb.Controller()

language = "c"
mode = "coding"
autocorrect_enabled = True
gui_open = False
pressedKeys = set()
hotkeyLockAuto = False
hotkeyLockMode = False
hotkeyLockCycle = False
bufferKey = ""
activeKey = True
injectingKey = False
writingWords = []

c_keyPair = {
    ">pr": 'printf("|");',
    ">if": "if (|) {\n    \n}",
    ">for": "for (int i = 0; i < |; i++) {\n    \n}",
    ">w": "while (|) {\n    \n}",
    ">sw": "switch (|) {\n    case :\n        break;\n    default:\n        break;\n}",
    ">case": "case |:\n    break;",
    ">do": "do {\n    \n} while (|);",
    ">else": "else {\n    \n}",
    ">elif": "else if (|) {\n    \n}",
    ">main": "#include <stdio.h>\n\nint main() {\n    \n    return 0;\n}",
    ">inc": "#include <|>",
    ">stdio": "#include <stdio.h>",
    ">stdlib": "#include <stdlib.h>",
    ">string": "#include <string.h>",
    ">math": "#include <math.h>",
    ">stru": "struct | {\n    \n};",
    ">typedef": "typedef struct {\n    \n} |;",
    ">union": "union | {\n    \n};",
    ">enum": "enum | {\n    \n};",
    ">fn": "void |() {\n    \n}",
    ">return": "return |;",
    ">break": "break;",
    ">continue": "continue;",
}

py_keyPair = {
    ">pr": "print(|)",
    ">if": "if |:\n    ",
    ">for": "for i in range(|):\n    ",
    ">w": "while |:\n    ",
    ">def": "def |():\n    ",
    ">class": "class |:\n    def __init__(self):\n        ",
    ">try": "try:\n    \nexcept Exception as e:\n    ",
    ">with": "with | as var:\n    ",
    ">import": "import |",
    ">from": "from | import ",
    ">lambda": "lambda |: ",
    ">return": "return |",
    ">pass": "pass",
    ">break": "break",
    ">continue": "continue",
    ">else": "else:\n    ",
    ">elif": "elif |:\n    ",
}

cpp_keyPair = {
    ">pr": 'cout << "|" << endl;',
    ">if": "if (|) {\n    \n}",
    ">for": "for (int i = 0; i < |; i++) {\n    \n}",
    ">w": "while (|) {\n    \n}",
    ">sw": "switch (|) {\n    case :\n        break;\n    default:\n        break;\n}",
    ">case": "case |:\n    break;",
    ">do": "do {\n    \n} while (|);",
    ">else": "else {\n    \n}",
    ">elif": "else if (|) {\n    \n}",
    ">main": "#include <iostream>\nusing namespace std;\n\nint main() {\n    \n    return 0;\n}",
    ">inc": "#include <|>",
    ">iostream": "#include <iostream>",
    ">vector": "#include <vector>",
    ">string": "#include <string>",
    ">algorithm": "#include <algorithm>",
    ">class": "class | {\npublic:\n    \n};",
    ">stru": "struct | {\n    \n};",
    ">try": "try {\n    \n} catch (const exception& e) {\n    \n}",
    ">template": "template <typename T>\nclass | {\npublic:\n    \n};",
    ">namespace": "namespace | {\n    \n}",
    ">using": "using namespace |;",
    ">fn": "void |() {\n    \n}",
    ">return": "return |;",
    ">break": "break;",
    ">continue": "continue;",
}

languageMapping = {
    "c": c_keyPair,
    "python": py_keyPair,
    "cpp": cpp_keyPair,
}

forceCorrections = {
    "teh": "the",
    "hte": "the",
    "adn": "and",
    "nad": "and",
    "recieve": "receive",
    "wierd": "weird",
    "seperate": "separate",
    "definately": "definitely",
    "occured": "occurred",
    "untill": "until",
    "becuase": "because",
    "bcuz": "because",
    "bcz": "because",
    "dont": "don't",
    "doesnt": "doesn't",
    "didnt": "didn't",
    "cant": "can't",
    "wont": "won't",
    "shouldnt": "shouldn't",
    "couldnt": "couldn't",
    "wouldnt": "wouldn't",
    "im": "I'm",
    "i": "I",
    "ive": "I've",
    "ill": "I'll",
    "id": "I'd",
    "u": "you",
    "ur": "your",
    "pls": "please",
    "plz": "please",
    "thx": "thanks",
    "thanx": "thanks",
    "gonna": "going",
    "wanna": "want",
    "lemme": "let",
    "kinda": "kind",
    "cuz": "because",
    "alot": "a lot",
    "aswell": "as well",
}

contextCorrections = {
    ("i", "am"): ("I", "am"),
    ("i", "have"): ("I", "have"),
    ("i", "will"): ("I", "will"),
    ("i", "can"): ("I", "can"),
    ("i", "want"): ("I", "want"),
    ("your", "welcome"): ("you're", "welcome"),
    ("could", "of"): ("could", "have"),
    ("should", "of"): ("should", "have"),
    ("would", "of"): ("would", "have"),
    ("a", "hour"): ("an", "hour"),
    ("an", "user"): ("a", "user"),
    ("an", "university"): ("a", "university"),
    ("a", "apple"): ("an", "apple"),
    ("a", "error"): ("an", "error"),
    ("a", "example"): ("an", "example"),
    ("a", "issue"): ("an", "issue"),
}

skipWords = {
    "api", "apis", "backend", "frontend", "javascript", "python", "react", "node", "express",
    "mongodb", "github", "git", "vscode", "linux", "windows", "html", "css", "json", "http",
    "https", "url", "ui", "ux", "ai", "mern", "oop", "oops", "dsa", "sql", "npm", "pip",
}

def updateMenuBar():
    title = f"STEP | Language: {language.upper()} | Mode: {mode} | Autocorrect: {'ON' if autocorrect_enabled else 'OFF'}"
    if sys.platform.startswith("win") and ctypes:
        ctypes.windll.kernel32.SetConsoleTitleW(title)
    else:
        print(f"[MENU] {title}")

def setLanguage(lang):
    global language
    if lang not in languageMapping:
        print(f"[ERROR] Unknown language: {lang}")
        return
    language = lang
    clearBufferKey()
    print(f"[STEP] Language switched to: {language}")
    updateMenuBar()

def setMode(new_mode):
    global mode
    valid_modes = {"writing", "coding", "off"}
    if new_mode not in valid_modes:
        print(f"[ERROR] Invalid mode: {new_mode}")
        return
    mode = new_mode
    clearBufferKey()
    print(f"[STEP] Mode switched to: {mode}")
    updateMenuBar()

def getCurrentKeyPair():
    return languageMapping[language]

def isDelimeter(key):
    try:
        char = key.char
    except AttributeError:
        char = None
    delimiters = ['(', ')', '{', '}', '[', ']', '.', ',', ';', ':', '!', '?']
    return key in (kb.Key.space, kb.Key.enter, kb.Key.tab) or (char in delimiters if char else False)

def clearBufferKey():
    global bufferKey
    bufferKey = ""

def removeLastCharacter():
    global bufferKey
    bufferKey = bufferKey[:-1]

def updateBufferKey(char):
    global bufferKey
    if mode == "coding":
        if not bufferKey:
            if char == ">":
                bufferKey = ">"
            return
        if char.isalnum() or char in ["_", ">", "."]:
            bufferKey += char
        else:
            clearBufferKey()
    elif mode == "writing":
        if char.isalpha() or char in ["'"]:
            bufferKey += char
        else:
            clearBufferKey()

def pressBackspace(times):
    try:
        for _ in range(times):
            controller.press(kb.Key.backspace)
            controller.release(kb.Key.backspace)
            time.sleep(0.004)
    except Exception as e:
        print(f"Error pressing backspace: {e}")

def typeText(text):
    global injectingKey
    injectingKey = True
    try:
        controller.type(text)
        time.sleep(0.004)
    except Exception as e:
        print(f"Error typing text: {e}")
    finally:
        injectingKey = False

def typeWithCursor(template):
    marker = "|"
    if marker not in template:
        controller.type(template)
        return
    marker_index = template.index(marker)
    final_text = template.replace(marker, "")
    controller.type(final_text)
    chars_to_move_left = len(final_text) - marker_index
    for _ in range(chars_to_move_left):
        controller.press(kb.Key.left)
        controller.release(kb.Key.left)

def findExactShortcut():
    return getCurrentKeyPair().get(bufferKey)

def expandShortcut(delimiter_key):
    global injectingKey
    expansion = findExactShortcut()
    if not expansion:
        clearBufferKey()
        return
    typed = bufferKey
    clearBufferKey()
    injectingKey = True
    try:
        pressBackspace(len(typed))
        typeWithCursor(expansion)
        if delimiter_key == kb.Key.space:
            controller.press(kb.Key.space)
            controller.release(kb.Key.space)
        elif delimiter_key == kb.Key.enter:
            controller.press(kb.Key.enter)
            controller.release(kb.Key.enter)
        elif delimiter_key == kb.Key.tab:
            controller.press(kb.Key.tab)
            controller.release(kb.Key.tab)
        print(f"Expanded: {typed} -> {expansion}")
    finally:
        injectingKey = False

def toggleStep():
    global activeKey
    activeKey = not activeKey
    clearBufferKey()
    print("STEP active:", activeKey)

def _cycleMode():
    global mode, autocorrect_enabled
    if mode == "coding":
        autocorrect_enabled = True
        setMode("writing")
        print("[STEP] ▶ writing mode | Autocorrect ON")
    elif mode == "writing":
        mode = "off"
        autocorrect_enabled = False
        clearBufferKey()
        print("[STEP] ▶ OFF")
    else:
        autocorrect_enabled = False
        setMode("coding")
        print("[STEP] ▶ coding mode | Autocorrect OFF")
    updateMenuBar()

def expandInstantly():
    global injectingKey
    expansion = findExactShortcut()
    if not expansion:
        return
    typed = bufferKey
    clearBufferKey()
    injectingKey = True
    try:
        pressBackspace(len(typed))
        typeWithCursor(expansion)
        print(f"Expanded instantly: {typed} -> {expansion}")
    finally:
        injectingKey = False

def normalizeKey(key):
    if hasattr(key, "char") and key.char:
        return key.char.lower()
    if hasattr(key, "vk") and key.vk == 190:
        return "."
    return key

def onRelease(key):
    normalized = normalizeKey(key)
    pressedKeys.discard(normalized)
    global hotkeyLockCycle
    if normalized in [kb.Key.ctrl, kb.Key.ctrl_l, kb.Key.ctrl_r, kb.Key.alt, kb.Key.alt_l, kb.Key.alt_r, "ctrl", "ctrl_l", "ctrl_r", "alt", "alt_l", "alt_r", "."]:
        hotkeyLockCycle = False

def preserveCase(original, corrected):
    if original.isupper():
        return corrected.upper()
    if original[:1].isupper():
        return corrected[:1].upper() + corrected[1:]
    return corrected

def similarity(a, b):
    return difflib.SequenceMatcher(None, a.lower(), b.lower()).ratio()

def isSafeWord(word):
    lower = word.lower()
    if lower in skipWords:
        return True
    if len(word) <= 1:
        return True
    if any(ch.isdigit() for ch in word):
        return True
    if "_" in word:
        return True
    if re.search(r"[A-Z]{2,}", word):
        return True
    if word.startswith(("http", "www")):
        return True
    return False

def chooseCorrection(word):
    lower = word.lower()
    if isSafeWord(word):
        return word
    if lower in forceCorrections:
        return preserveCase(word, forceCorrections[lower])
    if lower in spell:
        if lower == "i":
            return "I"
        return word
    candidates = spell.candidates(lower)
    if not candidates:
        return word
    best = max(candidates, key=lambda candidate: similarity(lower, candidate))
    correction = spell.correction(lower) or best
    if similarity(lower, correction) < 0.55 and lower not in forceCorrections:
        correction = best
    return preserveCase(word, correction)

def applyContextCorrection(current):
    global writingWords
    if not writingWords:
        writingWords.append(current)
        return current, len(current), 0
    previous = writingWords[-1]
    key = (previous.lower(), current.lower())
    if key not in contextCorrections:
        writingWords.append(current)
        return current, len(current), 0
    new_previous, new_current = contextCorrections[key]
    old_text = previous + " " + current
    new_text = preserveCase(previous, new_previous) + " " + preserveCase(current, new_current)
    writingWords[-1] = preserveCase(previous, new_previous)
    writingWords.append(preserveCase(current, new_current))
    return new_text, len(old_text), len(current)
def replacePreviousWord(new_text, delimiter_key=None):
    global injectingKey

    injectingKey = True

    try:
        controller.press(kb.Key.ctrl)
        controller.press(kb.Key.shift)
        controller.press(kb.Key.left)
        controller.release(kb.Key.left)
        controller.release(kb.Key.shift)
        controller.release(kb.Key.ctrl)

        time.sleep(0.01)

        controller.type(new_text)

        if delimiter_key == kb.Key.space:
            controller.press(kb.Key.space)
            controller.release(kb.Key.space)
        elif delimiter_key == kb.Key.enter:
            controller.press(kb.Key.enter)
            controller.release(kb.Key.enter)
        elif delimiter_key == kb.Key.tab:
            controller.press(kb.Key.tab)
            controller.release(kb.Key.tab)

    finally:
        injectingKey = False

def autoCorrectCurrentWord(delimiter_key=None):
    global bufferKey

    if not bufferKey or len(bufferKey) <= 1:
        clearBufferKey()
        return

    original = bufferKey
    corrected = chooseCorrection(original)

    clearBufferKey()

    if corrected == original:
        return

    replacePreviousWord(corrected, delimiter_key)

    print(f"[AUTO] {original} -> {corrected}")
    
def toggleAutocorrect():
    global autocorrect_enabled
    autocorrect_enabled = not autocorrect_enabled
    if autocorrect_enabled:
        setMode("writing")
        clearBufferKey()
        print("[STEP] Autocorrect ON | Writing mode ON")
    else:
        clearBufferKey()
        print("[STEP] Autocorrect OFF")

def processCompletedToken(delimiter_key):
    if mode == "coding" and bufferKey.startswith(">"):
        expandShortcut(delimiter_key)

def onPress(key):
    global injectingKey, activeKey, autocorrect_enabled, hotkeyLockCycle, writingWords
    if injectingKey:
        return

    normalized = normalizeKey(key)
    pressedKeys.add(normalized)

    ctrlPressed = any(k in pressedKeys for k in [kb.Key.ctrl, kb.Key.ctrl_l, kb.Key.ctrl_r, "ctrl", "ctrl_l", "ctrl_r"])
    altPressed = any(k in pressedKeys for k in [kb.Key.alt, kb.Key.alt_l, kb.Key.alt_r, "alt", "alt_l", "alt_r"])

    if ctrlPressed and altPressed and normalized == ".":
        if not hotkeyLockCycle:
            hotkeyLockCycle = True
            _cycleMode()
        return
    else:
        hotkeyLockCycle = False

    if ctrlPressed and altPressed and normalized == "1":
        setLanguage("c")
        return
    if ctrlPressed and altPressed and normalized == "2":
        setLanguage("cpp")
        return
    if ctrlPressed and altPressed and normalized == "3":
        setLanguage("python")
        return

    if not activeKey or mode == "off":
        return

    if key == kb.Key.backspace:
        removeLastCharacter()
        if writingWords:
            writingWords = writingWords[:-1]
        print("BUFFER:", repr(bufferKey))
        return

    if isDelimeter(key):
        if not bufferKey:
            return
        print("FINAL TOKEN:", repr(bufferKey))
        if mode == "coding":
            expandShortcut(key)
        elif mode == "writing" and autocorrect_enabled:
            autoCorrectCurrentWord(key)
            clearBufferKey()
        return

    try:
        char = key.char
    except AttributeError:
        char = None

    if char is not None:
        updateBufferKey(char)
        if bufferKey:
            print("BUFFER:", repr(bufferKey))
            if mode == "coding" and findExactShortcut():
                expandInstantly()

def main():
    print("\n===== STEP =====")
    print(f"Language    : {language}")
    print(f"Mode        : {mode}")
    print(f"Autocorrect : {'ON' if autocorrect_enabled else 'OFF'}")
    print("Shortcuts:")
    print("Ctrl + Alt + . : Cycle mode")
    print("Ctrl + Alt + 1 : C")
    print("Ctrl + Alt + 2 : C++")
    print("Ctrl + Alt + 3 : Python")
    print("\nExample:")
    print("Coding mode  -> type >pr")
    print("Writing mode -> type a word and press space/punctuation")
    print("================\n")
    updateMenuBar()
    with kb.Listener(on_press=onPress, on_release=onRelease) as listener:
        listener.join()

if __name__ == "__main__":
    main()
