import requests
import time

# In the main loop of the agent
def poll_commands(server_url, machine_info):
    hostname = machine_info["hostname"]
    while True:
        try:
            response = requests.get(f"{server_url}/api/command/{hostname}")
            data = response.json()
            cmd = data.get("command", "none")
            if cmd == "start":
                # Call start_logging()
                pass
            elif cmd == "stop":
                # Call stop_logging()
                pass
        except Exception as e:
            print(f"Error polling command: {e}")
        time.sleep(30)  # Poll every 30 seconds