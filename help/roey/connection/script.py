import requests
import time

# The URL of the backend server's start endpoint
backend_url = "http://127.0.0.1:5000"

def notify_backend():
    print("Notifying backend that the script is starting...")
    try:
        response = requests.post(f"{backend_url}/start")
        if response.status_code == 200:
            print("Successfully notified backend.")
        else:
            print(f"Failed to notify backend. Status code: {response.status_code}")
    except requests.exceptions.ConnectionError as e:
        print(f"Could not connect to the backend server. Make sure server.py is running. Error: {e}")


def wait_for_approval():
    """Polls the backend until approval is granted."""
    print("Waiting for approval from the backend...")
    while True:
        try:
            response = requests.get(f"{backend_url}/check-approval")
            if response.status_code == 200:
                data = response.json()
                if data.get('approved'):
                    print("Approval received! Continuing script execution.")
                    break  # Exit the loop and continue with the script
                else:
                    print("Approval not yet granted. Retrying in 5 seconds...")
            else:
                print(f"Failed to get approval status. Status code: {response.status_code}")
        except requests.exceptions.ConnectionError as e:
            print(f"Connection error while checking for approval: {e}")

        time.sleep(5)  # Wait 5 seconds before checking again

if __name__ == '__main__':
    notify_backend()
    wait_for_approval()