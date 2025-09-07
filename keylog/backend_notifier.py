import requests
import time

class BackendNotifier:
    def __init__(self, backend_url):  # the backend ip
        self.backend_url = backend_url

    def im_alive(self):
            """Tell backend that the script is alive and waiting."""
            print("Notifying backend that the script is alive...")
            while True:
                try:
                    response = requests.post(f"{self.backend_url}/alive")
                    if response.status_code == 200:
                        print("✅ Successfully notified backend.")
                        break
                    else:
                        print(f"⚠️ Failed to notify backend. Status code: {response.status_code}")
                except requests.exceptions.ConnectionError as e:
                    print(f"❌ Could not connect to backend. Error: {e}")
                time.sleep(5)

    def start_or_stop(self):
            """Polls the backend until approval is granted."""
            try:
                response = requests.get(f"{self.backend_url}/check-approval")
                if response.status_code == 200:
                    data = response.json()
                    if data.get('approved'):
                        return True
                    else:
                        return False
                else:
                    print(f"Failed to get approval status. Status code: {response.status_code}")
            except requests.exceptions.ConnectionError as e:
                print(f"Connection error while checking for approval: {e}")

    def disabled(self):
            """Polls the backend until disable status."""
            try:
                response = requests.get(f"{self.backend_url}/check-disable")
                if response.status_code == 200:
                    data = response.json()
                    if data.get('disable'):
                        return True
                    else:
                        return False
                else:
                    print(f"Failed to get disable status. Status code: {response.status_code}")
            except requests.exceptions.ConnectionError as e:
                print(f"Connection error while checking for disable: {e}")
