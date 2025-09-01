import time
from logger import EventLogger
from writer import EncryptedJSONWriter
from sender import FileSender

def main():
    logger = EventLogger()
    writer = EncryptedJSONWriter()
    sender = FileSender()

    print("📡 התחלת איסוף אירועים...")

    while True:
        # סימולציה של איסוף אירועים
        logger.add_event("משתמש לחץ על כפתור")
        logger.add_event("התקבלה בקשה מהדפדפן")

        # קבלת האירועים שנאספו
        events = logger.get_events()
        if events:
            # שמירה ל־JSON מוצפן
            writer.save_events(events)
            print(f"✅ נשמרו {len(events)} אירועים לקובץ מוצפן.")

            # שליחת הקובץ לשרת Flask
            sender.send_file("events.json.enc")

            # ניקוי האירועים מהזיכרון
            logger.clear_events()

        # המתנה לפני הסיבוב הבא
        time.sleep(10)  # כל 10 שניות

if __name__ == "__main__":
    main()