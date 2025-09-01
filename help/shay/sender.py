import requests

class NetworkWriter:
    def __init__(self, server_url="http://127.0.0.1:5000/upload"):
        self.server_url = server_url

    def send_data(self, data: str, machine_name: str):
        """שולח את הנתונים המוצפנים לשרת"""
        payload = {"data": data, "machine": machine_name}
        response = requests.post(self.server_url, json=payload)
        print("תשובת השרת:", response.text)