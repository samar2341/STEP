from pynput import keyboard

def on_press(key):
    try:
        print("You pressed:", key.char)
    except AttributeError:
        print("Special key pressed:", key)

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()