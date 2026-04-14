from pynput import kb #alias kb

#dictionary of key pair mapping 
c_keyPair = {
    ">pr": "printf();",
    ">if": "if(){};",
    ">for": "for(;;){}",
    ">w": "while(){};",
    ">sw": "switch(){};",
    ">case": "case : break;",
    ">do": "do{} while();",
    ">else": "else{};",
    ">elif": "else if(){};",
    ">main": "int main(){};",
    ">inc": "#include < >",
    ">stru": "struct {} ;",
    ">typedef": "typedef struct {} ;",
    ">union": "union {} ;",
    ">enum": "enum {} ;",
    ">fn": "void () {}",
    ">return": "return ;",
    ">break": "break;",
    ">continue": "continue;",
}

#python key pair mapping
py_keyPair = {
    ">pr": "print()",
    ">if": "if :",
    ">for": "for i in range():",
    ">w": "while :",
    ">def": "def function_name():",
    ">class": "class :",
    ">try": "try: except:",
    ">with": "with as :",
    ">import": "import",
    ">from": "from import",
    ">lambda": "lambda :",
    ">return": "return",
    ">pass": "pass",
    ">break": "break",
    ">continue": "continue",
    ">else": "else:",
    ">elif": "elif :",
}

#cpp key pair mapping
cpp_keyPair = {
    ">pr": "cout << ;",
    ">if": "if(){};",
    ">for": "for(;;){}",
    ">w": "while(){};",
    ">sw": "switch(){};",
    ">case": "case : break;",
    ">do": "do{} while();",
    ">else": "else{};",
    ">elif": "else if(){};",
    ">main": "int main(){};",
    ">inc": "#include < >",
    ">class": "class {};",
    ">stru": "struct {} ;",
    ">try": "try {} catch() {}",
    ">template": "template<> class {} ;",
    ">namespace": "namespace {} ;",
    ">using": "using namespace ;",
    ">fn": "void () {}",
    ">return": "return ;",
    ">break": "break;",
    ">continue": "continue;",
}


#language mapping 
languageMapping = {
    "c": c_keyPair,
    "python": py_keyPair,
    "cpp": cpp_keyPair,
}

#current language key pair mapping
language = "c" #default language is c
currentKeyPair = languageMapping[language] #current key pair mapping based on the language selected

#state variable to determine which language is being used
state = "c" #default state is c

#global stating
bufferKey = "" #buffer to store the keys pressed
activeKey = True #flag to determine if the key pair is active
injectingKey = False #flag to determine if the key pair is being injected


#function to get the current key pair mapping based on the language selected
def getCurrentKeyPair():
    return languageMapping[language]


def isDelimeter(key):
    #check if the key is a delimiter
    delimiters = [' ', '\n', '\t', '(', ')', '{', '}', '[', ']', ';']
    return key in (kb.Key.space, kb.Key.enter, kb.Key.tab) or key.char in delimiters



#clear buffer key 
def clearBufferKey():
    global bufferKey
    bufferKey = ""

def removeLastCharacter():
    global bufferKey
    bufferKey = bufferKey[:-1]

#buffer update function to update the buffer key based on the key pressed
def updateBufferKey(key):
    global bufferKey

    if not bufferKey:
        if char == ">":
            bufferKey = ">"
        return
    
    if char.isalpha() or char.isdigit() or char in ['>', '_']:
        bufferKey += char
    else:
        clearBufferKey()

    if isDelimeter(key):
        clearBufferKey()

def pressBackspace(times):
    global injectingKey
    injectingKey = True

    #try
    try:
        for _ in range(times):
            kb.Controller().press(kb.Key.backspace)
            kb.Controller().release(kb.Key.backspace)
    except Exception as e:
        print(f"Error pressing backspace: {e}")
    finally:
        injectingKey = False


def typeText(text):
    global injectingKey
    injectingKey = True
    try:
        controller.type(text)
    except Exception as e:
        print(f"Error typing text: {e}")
    finally:
        injectingKey = False



def expandShortcut(delimeterKey):
    currentKeyPair = getCurrentKeyPair()
    if bufferKey in currentKeyPair:
        expansion = currentKeyPair[bufferKey]
        pressBackspace(len(bufferKey))
        typeText(expansion)
    

    if delimeterKey:
        pressBackspace(1)
    elif delimeterKey == kb.Key.space:
        typeText(" ")
    elif delimeterKey == kb.Key.enter:
        controller.press(kb.Key.enter)
        controller.release(kb.Key.enter)
    elif delimeterKey == kb.Key.tab:
        controller.press(kb.Key.tab)
        controller.release(kb.Key.tab)

    elif delimeterKey == kb.Key.backspace:
        controller.press(kb.Key.backspace)
        controller.release(kb.Key.backspace)
    elif delimeterKey == kb.Key.esc:
        controller.press(kb.Key.esc)
        controller.release(kb.Key.esc)
    elif delimeterKey == kb.Key.shift:
        controller.press(kb.Key.shift)
        controller.release(kb.Key.shift)
    elif delimeterKey == kb.Key.ctrl:
        controller.press(kb.Key.ctrl)
        controller.release(kb.Key.ctrl)
    elif delimeterKey == kb.Key.alt:
        controller.press(kb.Key.alt)
        controller.release(kb.Key.alt)
    elif delimeterKey == kb.Key.cmd:
        controller.press(kb.Key.cmd)
        controller.release(kb.Key.cmd)
    elif delimeterKey == kb.Key.caps_lock:
        controller.press(kb.Key.caps_lock)
        controller.release(kb.Key.caps_lock)
    elif delimeterKey == kb.Key.num_lock:
        controller.press(kb.Key.num_lock)
        controller.release(kb.Key.num_lock)

    printf(f"Buffer Key: {bufferKey}, Delimiter Key: {delimeterKey}")

    clearBufferKey()

