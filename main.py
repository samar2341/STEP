# Windows compatibility: ensure pynput works and add fallback for menu bar
import sys
import time
from spellchecker import SpellChecker
from pynput import keyboard as kb
try:
    import ctypes
    import threading
except ImportError:
    ctypes = None
    threading = None


# Aggressive autocorrect: distance=2 for more tolerance
spell = SpellChecker(distance=2)

#controller for simulating key presses
controller = kb.Controller()


# State variable to determine which language is being used
language = "c"  # default language

#dictionary of key pair mapping 
c_keyPair = {
    ">pr": 'printf("|");',
    ">if": "if (|) {\n    \n}",
    ">for": "for (int i = 0; i < |; i++) {\n    \n}",
    ">w": "while (|) {\n    \n}",
    ">sw": (
        "switch (|) {\n"
        "    case :\n"
        "        break;\n"
        "    default:\n"
        "        break;\n"
        "}"
    ),
    ">case": "case |:\n    break;",
    ">do": "do {\n    \n} while (|);",
    ">else": "else {\n    \n}",
    ">elif": "else if (|) {\n    \n}",
    ">main": (
        "#include <stdio.h>\n\n"
        "int main() {\n"
        "    \n"
        "    return 0;\n"
        "}"
    ),
    ">inc": "#include <|>",
    ">stdio": "#include <stdio.h>",
    ">stdlib": "#include <stdlib.h>",
    ">string": "#include <string.h>",
    ">math": "#include <math.h>",
    ">stru": (
        "struct | {\n"
        "    \n"
        "};"
    ),
    ">typedef": (
        "typedef struct {\n"
        "    \n"
        "} |;"
    ),
    ">union": (
        "union | {\n"
        "    \n"
        "};"
    ),
    ">enum": (
        "enum | {\n"
        "    \n"
        "};"
    ),
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
    ">class": (
        "class |:\n"
        "    def __init__(self):\n"
        "        "
    ),
    ">try": (
        "try:\n"
        "    \n"
        "except Exception as e:\n"
        "    "
    ),
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
    ">sw": (
        "switch (|) {\n"
        "    case :\n"
        "        break;\n"
        "    default:\n"
        "        break;\n"
        "}"
    ),
    ">case": "case |:\n    break;",
    ">do": "do {\n    \n} while (|);",
    ">else": "else {\n    \n}",
    ">elif": "else if (|) {\n    \n}",
    ">main": (
        "#include <iostream>\n"
        "using namespace std;\n\n"
        "int main() {\n"
        "    \n"
        "    return 0;\n"
        "}"
    ),
    ">inc": "#include <|>",
    ">iostream": "#include <iostream>",
    ">vector": "#include <vector>",
    ">string": "#include <string>",
    ">algorithm": "#include <algorithm>",
    ">class": (
        "class | {\n"
        "public:\n"
        "    \n"
        "};"
    ),
    ">stru": (
        "struct | {\n"
        "    \n"
        "};"
    ),
    ">try": (
        "try {\n"
        "    \n"
        "} catch (const exception& e) {\n"
        "    \n"
        "}"
    ),
    ">template": (
        "template <typename T>\n"
        "class | {\n"
        "public:\n"
        "    \n"
        "};"
    ),
    ">namespace": (
        "namespace | {\n"
        "    \n"
        "}"
    ),
    ">using": "using namespace |;",
    ">fn": "void |() {\n    \n}",
    ">return": "return |;",
    ">break": "break;",
    ">continue": "continue;",
}


#language mapping 
languageMapping = {
    "c": c_keyPair,
    "python": py_keyPair,
    "cpp": cpp_keyPair,
}


# Update menu bar (Windows only, fallback to print)
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


#mode of use
mode = "coding"


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

    
#autocorrect setting
autocorrect_enabled = True
gui_open = False
pressedKeys = set()
hotkeyLockAuto = False
hotkeyLockMode = False
hotkeyLockCycle = False

#global stating
bufferKey = "" #buffer to store the keys pressed
activeKey = True #flag to determine if the key pair is active
injectingKey = False #flag to determine if the key pair is being injected


#function to get the current key pair mapping based on the language selected
def getCurrentKeyPair():
    return languageMapping[language]


def isDelimeter(key):
    try:
        char = key.char
    except AttributeError:
        char = None

    delimiters = ['(', ')', '{', '}', '[', ']']

    return key in (kb.Key.space, kb.Key.enter, kb.Key.tab) or (char in delimiters if char else False)

#clear buffer key 
def clearBufferKey():
    global bufferKey
    bufferKey = ""

def removeLastCharacter():
    global bufferKey
    bufferKey = bufferKey[:-1]


#buffer update function to update the buffer key based on the key pressed
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
        if char.isalpha():
            bufferKey += char
        else:
            clearBufferKey()

            
def pressBackspace(times):
    try:
        for _ in range(times):
            controller.press(kb.Key.backspace)
            controller.release(kb.Key.backspace)
            time.sleep(0.01)
    except Exception as e:
        print(f"Error pressing backspace: {e}")


def typeText(text):
    global injectingKey
    injectingKey = True

    try:
        controller.type(text)
        time.sleep(0.01)
    except Exception as e:
        print(f"Error typing text: {e}")
    finally:
        injectingKey = False



def expandShortcut(delimiter_key):
    global injectingKey

    currentKeyPair = getCurrentKeyPair()
    expansion = findExactShortcut()

    if not expansion:
        clearBufferKey()
        return

    typed = bufferKey
    clearBufferKey()

    if typed in currentKeyPair:
        expansion = currentKeyPair[typed]
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
    else:  # off
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
    # For '.' key, check vk (virtual key code) for reliability
    if hasattr(key, 'char') and key.char:
        return key.char.lower()
    elif hasattr(key, 'vk') and key.vk == 190:
        return '.'
    return key



def onRelease(key):
    normalized = normalizeKey(key)
    pressedKeys.discard(normalized)
    global hotkeyLockCycle
    # Reset hotkey lock if Ctrl or Alt or . is released
    if normalized in [kb.Key.ctrl, kb.Key.ctrl_l, kb.Key.ctrl_r, kb.Key.alt, kb.Key.alt_l, kb.Key.alt_r, 'ctrl', 'ctrl_l', 'ctrl_r', 'alt', 'alt_l', 'alt_r', '.']:
        hotkeyLockCycle = False



#main function onPress key listener

# Language switching hotkeys: 1 (C), 2 (Python), 3 (C++)
def onPress(key):
    global injectingKey, activeKey, autocorrect_enabled, hotkeyLockCycle

    if injectingKey:
        return

    normalized = normalizeKey(key)
    pressedKeys.add(normalized)

    # Robust modifier detection
    ctrlPressed = any(k in pressedKeys for k in [kb.Key.ctrl, kb.Key.ctrl_l, kb.Key.ctrl_r, 'ctrl', 'ctrl_l', 'ctrl_r'])
    altPressed = any(k in pressedKeys for k in [kb.Key.alt, kb.Key.alt_l, kb.Key.alt_r, 'alt', 'alt_l', 'alt_r'])

    # Ctrl + Alt + . → cycle: coding → writing → off → coding
    if ctrlPressed and altPressed and normalized == '.':
        if not hotkeyLockCycle:
            hotkeyLockCycle = True
            _cycleMode()
        return
    else:
        hotkeyLockCycle = False

    # Language switching: 1 (C), 2 (C++), 3 (Python)
    if normalized == '1':
        setLanguage('c')
        return
    elif normalized == '2':
        setLanguage('cpp')
        return
    elif normalized == '3':
        setLanguage('python')
        return

    if not activeKey or mode == "off":
        return

    if key == kb.Key.backspace:
        removeLastCharacter()
        print("BUFFER:", repr(bufferKey))
        return

    if isDelimeter(key):
        if not bufferKey:
            return
        print("FINAL TOKEN:", repr(bufferKey))
        if mode == "coding":
            expandShortcut(key)
        elif mode == "writing" and autocorrect_enabled:
            autoCorrectCurrentWord()
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


def findExactShortcut():
    currentKeyPair = getCurrentKeyPair()
    return currentKeyPair.get(bufferKey)


def processCompletedToken(delimiter_key):
    if mode == "coding":
        if bufferKey.startswith(">"):
            expandShortcut(delimiter_key)

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

#autocorrect function to autocorrect the current word based on the spell checker
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



# Aggressive autocorrect: always correct, no mercy, never repeat first word
def autoCorrectCurrentWord():
    global bufferKey, injectingKey

    if not bufferKey:
        return

    if len(bufferKey) <= 1:
        return

    candidates = spell.candidates(bufferKey)
    if not candidates:
        return

    # Always pick the best match, even if very different
    def similarity(a, b):
        # Use Levenshtein distance for better accuracy
        import difflib
        return difflib.SequenceMatcher(None, a, b).ratio()

    best_match = max(candidates, key=lambda w: similarity(bufferKey, w))

    # If the best match is the same as the buffer, but the buffer is not a valid word, force correction
    if best_match == bufferKey and bufferKey not in spell:
        best_match = spell.correction(bufferKey)

    # Fix: never repeat the first word
    if best_match == bufferKey:
        return

    original = bufferKey
    clearBufferKey()

    injectingKey = True
    try:
        time.sleep(0.01)
        pressBackspace(len(original))
        time.sleep(0.01)
        controller.type(best_match)
        print(f"[AUTO] {original} -> {best_match}")
    finally:
        injectingKey = False


#main function

def main():
    print("\n===== STEP =====")
    print(f"Language    : {language}")
    print(f"Mode        : {mode}")
    print(f"Autocorrect : {'ON' if autocorrect_enabled else 'OFF'}")
    print("Shortcuts:")
    print("Ctrl + Alt + . : Cycle mode (make sure to use the period key)")
    print("1: C | 2: C++ | 3: Python (switch language)")
    print("\nExample:")
    print("  Coding mode -> type >pr")
    print("  Writing mode -> type a word and press space")
    print("================\n")
    updateMenuBar()

    with kb.Listener(on_press=onPress, on_release=onRelease) as listener:
        listener.join()

if __name__ == "__main__":
    main()
