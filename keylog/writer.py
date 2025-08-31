from cryptography.fernet import Fernet
import os

class EncryptedFileWriter:
    def __init__(self, filename="events.enc", keyfile="secret.key"):
        self.filename = filename
        self.keyfile = keyfile
        self.key = self._load_or_generate_key()
        self.cipher = Fernet(self.key)

    def _load_or_generate_key(self):
        if os.path.exists(self.keyfile):
            with open(self.keyfile, "rb") as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(self.keyfile, "wb") as f:
                f.write(key)
            return key

    def save_events(self, events):
        """שומר אירועים לקובץ בצורה מוצפנת"""
        if not events:
            return
        data = "\n".join(events).encode("utf-8")
        encrypted = self.cipher.encrypt(data)
        with open(self.filename, "ab") as f:
            f.write(encrypted + b"\n")