import requests

class NetworkWriter:
    def __init__(self, server_url="http://127.0.0.1:5000/api/upload"):   # the backend ip
        self.server_url = server_url

    def send_data(self, data: str, machine_info: dict,encryption_key):
        """שולח את הנתונים המוצפנים לשרת"""
        payload = {"data": data, "machine_info": machine_info , "encryption_key":encryption_key}
        response = requests.post(self.server_url, json=payload)
        print("תשובת השרת:", response.text)