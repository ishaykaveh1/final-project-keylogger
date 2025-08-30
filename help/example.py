import keyboard
import sys

def f(event):                           #תתנו לי רעיון לשם של הפונקציה
    print(f"You pressed: {event.name}")

def stop_program():
    pass                                # לא הבנתי איך עוצרים את התוכנה


keyboard.on_press(f)


keyboard.add_hotkey('ctrl+shift', stop_program)

print("Press keys (Ctrl+Shift+F to quit).")
keyboard.wait()
                                        #האם צריך להוסיף עוד משהו???