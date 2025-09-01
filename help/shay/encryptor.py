class Encryptor:
    def __init__(self, key: int = 42):
        self.key = key

    def encrypt(self, text: str) -> str:
        """מבצע הצפנת XOR פשוטה"""
        return ''.join(chr(ord(c) ^ self.key) for c in text)

    def decrypt(self, text: str) -> str:
        """מבצע פענוח XOR (זהה להצפנה)"""
        return self.encrypt(text)