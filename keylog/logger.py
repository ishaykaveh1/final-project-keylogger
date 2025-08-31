import datetime
import socket

class EventLogger:
    def __init__(self):
        self.events = []
        self.hostname = socket.gethostname()

    def add_event(self, text: str):
        """ מוסיף אירוע עם טקסט, זמן, ושם מחשב """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        event = f"{timestamp} | {self.hostname} | {text}"
        self.events.append(event)

    def get_events(self):
        return self.events

    def clear_events(self):
        self.events = []