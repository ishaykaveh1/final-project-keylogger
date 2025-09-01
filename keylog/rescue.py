from cryptography.fernet import Fernet
import json

def decrypt_file(enc_file="events.json.enc", key_file="secret.key"):
    with open(key_file, "rb") as f:
        key = f.read()
    cipher = Fernet(key)

    with open(enc_file, "rb") as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if line:
            decrypted = cipher.decrypt(line)
            data = json.loads(decrypted.decode("utf-8"))
            print(json.dumps(data, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    decrypt_file()