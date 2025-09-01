from cryptography.fernet import Fernet
import os, json

class EncryptedJSONWriter:
    def __init__(self, filename="events.json.enc", keyfile="secret.key"):
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
        """שומר אירועים לקובץ JSON מוצפן"""
        if not events:
            return
        json_data = json.dumps(events, ensure_ascii=False, indent=2)
        encrypted = self.cipher.encrypt(json_data.encode("utf-8"))
        with open(self.filename, "ab") as f:
            f.write(encrypted + b"\n")