import time
import threading
from logger import EventLogger
from writer import EncryptedFileWriter
from sender import FileSender

logger = EventLogger()
writer = EncryptedFileWriter()
sender = FileSender()

INTERVAL = 10  # כל כמה שניות לשמור ולשלוח

def collect_events():
    """ סימולציה - הוספת אירועים לרשימה """
    for i in range(3):
        logger.add_event(f"Simulated event {i+1}")
        time.sleep(2)

def save_and_send():
    """ שמירת אירועים לקובץ ושליחה לשרת """
    events = logger.get_events()
    if events:
        writer.save_events(events)
        logger.clear_events()
        sender.send_file(writer.filename)
    else:
        print("אין אירועים לשמור.")

    # קריאה חוזרת של הפונקציה בעוד INTERVAL שניות
    threading.Timer(INTERVAL, save_and_send).start()

def main():
    # התחלת איסוף אירועים ברקע
    threading.Thread(target=collect_events, daemon=True).start()

    # התחלת טיימר ראשוני
    save_and_send()

    # שומר את התוכנית רצה
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()