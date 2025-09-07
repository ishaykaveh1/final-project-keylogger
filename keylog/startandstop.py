import requests
import time

# The URL of the backend server's start endpoint
backend_url = "http://127.0.0.1:5000"

def notify_backend():
    print("Notifying backend that the script is starting...")
    try:
        response = requests.post(f"{backend_url}/alive")
        if response.status_code == 200:
            print("Successfully notified backend.")
        else:
            print(f"Failed to notify backend. Status code: {response.status_code}")
    except requests.exceptions.ConnectionError as e:
        print(f"Could not connect to the backend server. Make sure server.py is running. Error: {e}")


def start_or_stop():
    """Polls the backend until approval is granted."""
    print("Waiting for approval from the backend...")
    while True:
        try:
            response = requests.get(f"{backend_url}/check-approval")
            if response.status_code == 200:
                data = response.json()
                if data.get('approved'):
                    print("Approval received! Continuing script execution.")
                else:
                    print("Approval denied. Retrying in 5 seconds...")
            else:
                print(f"Failed to get approval status. Status code: {response.status_code}")
        except requests.exceptions.ConnectionError as e:
            print(f"Connection error while checking for approval: {e}")

        time.sleep(10)

if __name__ == '__main__':
    notify_backend()
    start_or_stop()