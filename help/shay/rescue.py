import sys

class Encryptor:
    def __init__(self, key: int):
        self.key = key

    def encrypt(self, text: str) -> str:
        return ''.join(chr(ord(c) ^ self.key) for c in text)

    def decrypt(self, text: str) -> str:
        return self.encrypt(text)  # XOR סימטרי

def decrypt_file(enc_file, key):
    encryptor = Encryptor(int(key))
    with open(enc_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                decrypted = encryptor.decrypt(line)
                print(decrypted)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("שימוש: python rescue.py <נתיב_קובץ> <מפתח>")
        sys.exit(1)
    decrypt_file(sys.argv[1], sys.argv[2])