from pynput import keyboard as kb
import time
from spellchecker import SpellChecker

spell = SpellChecker(distance=1)

#controller for simulating key presses
controller = kb.Controller()

#state variable to determine which language is being used
language = "c" #default language

#dictionary of key pair mapping 
c_keyPair = {
    ">pr": "printf(\"|\");",
    ">if": "if(|){}",
    ">for": "for(|;;){}",
    ">w": "while(|){}",
    ">sw": "switch(|){}",
    ">case": "case |: break;",
    ">do": "do{} while(|);",
    ">else": "else{}",
    ">elif": "else if(|){}",
    ">main": "int main(|){}",
    ">inc": "#include <|>",
    ">stru": "struct {|};",
    ">typedef": "typedef struct {|};",
    ">union": "union {|};",
    ">enum": "enum {|};",
    ">fn": "void (|) {}",
    ">return": "return |;",
    ">break": "break;",
    ">continue": "continue;",
}

#python key pair mapping
py_keyPair = {
    ">pr": "print(\"|\")",
    ">if": "if |:",
    ">for": "for i in range(|):",
    ">w": "while |:",
    ">def": "def function_name(|):",
    ">class": "class |:",
    ">try": "try: except|:",
    ">with": "with | as:",
    ">import": "import \"|\"",
    ">from": "from \"|\" import",
    ">lambda": "lambda |:",
    ">return": "return |;",
    ">pass": "pass",
    ">break": "break",
    ">continue": "continue",
    ">else": "else:",
    ">elif": "elif |:",
}

#cpp key pair mapping
cpp_keyPair = {
    ">pr": "cout << \"|\";",
    ">if": "if(|){}",
    ">for": "for(|;;){}",
    ">w": "while(|){}",
    ">sw": "switch(|){}",
    ">case": "case |: break;",
    ">do": "do{} while(|);",
    ">else": "else{}",
    ">elif": "else if(|){}",
    ">main": "int main(|){}",
    ">inc": "#include <|>",
    ">class": "class {|};",
    ">stru": "struct {|};",
    ">try": "try {} catch(|) {}",
    ">template": "template<|> class {};",
    ">namespace": "namespace {|};",
    ">using": "using namespace |;",
    ">fn": "void (|) {}",
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

def setLanguage(lang):
    global language

    if lang not in languageMapping:
        print(f"[ERROR] Unknown language: {lang}")
        return

    language = lang
    clearBufferKey()
    print(f"[STEP] Language switched to: {language}")


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
    global injectingKey
    injectingKey = True

    try:
        for _ in range(times):
            controller.press(kb.Key.backspace)
            controller.release(kb.Key.backspace)
        time.sleep(0.05)
    except Exception as e:
        print(f"Error pressing backspace: {e}")
    finally:
        injectingKey = False

def typeText(text):
    global injectingKey
    injectingKey = True

    try:
        controller.type(text)
        time.sleep(0.05)
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

    if bufferKey in currentKeyPair:
        expansion = currentKeyPair[bufferKey]

        injectingKey = True

        try:
        
            # Select the entire word backward
            controller.press(kb.Key.ctrl)
            controller.press(kb.Key.shift)
            controller.press(kb.Key.left)
            controller.release(kb.Key.left)
            controller.release(kb.Key.shift)
            controller.release(kb.Key.ctrl)

            typeWithCursor(expansion)

            # re-type delimiter properly
            if delimiter_key == kb.Key.space:
                controller.press(kb.Key.space)
                controller.release(kb.Key.space)
            elif delimiter_key == kb.Key.enter:
                controller.press(kb.Key.enter)
                controller.release(kb.Key.enter)
            elif delimiter_key == kb.Key.tab:
                controller.press(kb.Key.tab)
                controller.release(kb.Key.tab)

            print(f"Expanded: {bufferKey} -> {expansion}")

        finally:
            injectingKey = False 

    clearBufferKey()


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



def expandInstantly():
    global injectingKey

    expansion = findExactShortcut()
    if not expansion:
        return

    typed = bufferKey

    injectingKey = True
    try:
        # Select the entire word backward
        controller.press(kb.Key.ctrl)
        controller.press(kb.Key.shift)
        controller.press(kb.Key.left)
        controller.release(kb.Key.left)
        controller.release(kb.Key.shift)
        controller.release(kb.Key.ctrl)

        typeWithCursor(expansion)
        print(f"Expanded instantly: {typed} -> {expansion}")

    finally:
        injectingKey = False
        clearBufferKey()


def normalizeKey(key):
    try:
        return key.char.lower()
    except AttributeError:
        return key


def onRelease(key):
    normalized = normalizeKey(key)
    pressedKeys.discard(normalized)



#main function onPress key listener
def onPress(key):
    global injectingKey, activeKey, autocorrect_enabled, hotkeyLockCycle

    if injectingKey:
        return

    normalized = normalizeKey(key)
    pressedKeys.add(normalized)

    ctrlPressed = (
        kb.Key.ctrl in pressedKeys or
        kb.Key.ctrl_l in pressedKeys or
        kb.Key.ctrl_r in pressedKeys
    )

    altPressed = (
        kb.Key.alt in pressedKeys or
        kb.Key.alt_l in pressedKeys or
        kb.Key.alt_r in pressedKeys
    )

    # Ctrl + Alt + F2 → cycle: coding → writing → off → coding
    if ctrlPressed and altPressed and key == kb.Key.f10                                 :
        if not hotkeyLockCycle:
            hotkeyLockCycle = True
            _cycleMode()
        return
    else:
        hotkeyLockCycle = False

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

            if key == kb.Key.space:
                controller.press(kb.Key.space)
                controller.release(kb.Key.space)
            elif key == kb.Key.enter:
                controller.press(kb.Key.enter)
                controller.release(kb.Key.enter)
            elif key == kb.Key.tab:
                controller.press(kb.Key.tab)
                controller.release(kb.Key.tab)
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


def autoCorrectCurrentWord():
    global bufferKey, injectingKey

    if not bufferKey:
        return

    if len(bufferKey) <= 2:
        return

    # get all candidates
    candidates = spell.candidates(bufferKey)

    if not candidates:
        return

    # pick closest word manually
    def similarity(a, b):
        return sum(1 for x, y in zip(a, b) if x == y)

    best_match = max(candidates, key=lambda w: similarity(bufferKey, w))

    # avoid bad corrections
    if best_match == bufferKey:
        return

    if abs(len(best_match) - len(bufferKey)) > 1:
        return

    injectingKey = True
    try:
        # Select the entire word backward
        controller.press(kb.Key.ctrl)
        controller.press(kb.Key.shift)
        controller.press(kb.Key.left)
        controller.release(kb.Key.left)
        controller.release(kb.Key.shift)
        controller.release(kb.Key.ctrl)

        controller.type(best_match)
        print(f"[AUTO] {bufferKey} -> {best_match}")

    finally:
        injectingKey = False


#main function
def main():
    print("Starting STEP...")
    print("Language:", language)
    print("Press F8 to toggle ON/OFF")
    print("Try: >pr then space")

    with kb.Listener(on_press = onPress, on_release = onRelease) as listener:
        listener.join()


if __name__ == "__main__":
    main()
