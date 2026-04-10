from pynput import keyboard

def on_press(key):
    try:
        print("\nYou pressed:", key.char, "\n")
    except AttributeError:
        print("\n\Special key pressed:", key, "\n")

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()