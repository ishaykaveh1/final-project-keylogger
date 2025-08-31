from cryptography.fernet import Fernet

def decrypt_file(enc_file="events.enc", key_file="secret.key"):
    with open(key_file, "rb") as f:
        key = f.read()
    cipher = Fernet(key)

    with open(enc_file, "rb") as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if line:
            decrypted = cipher.decrypt(line)
            print(decrypted.decode("utf-8"))

if __name__ == "__main__":
    decrypt_file()