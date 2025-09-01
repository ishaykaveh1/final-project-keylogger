import requests
import os

class FileSender:
    def __init__(self, server_url="http://127.0.0.1:5000/upload"):
        self.server_url = server_url

    def send_file(self, filepath):
        if not os.path.exists(filepath):
            print("⚠️ No file found to send.")
            return
        with open(filepath, "rb") as f:
            res = requests.post(self.server_url, files={"file": f})
            print("תשובת השרת:", res.text)