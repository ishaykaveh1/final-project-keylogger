from flask import Flask, jsonify, send_file, request
import threading
import time
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Initial status
current_status = "Not Running"
approval_granted = False

@app.route('/')
def serve_frontend():
    return send_file('index.html')

@app.route('/status')
def get_status():
    return jsonify({'status': current_status})

@app.route('/start', methods=['POST'])
def start_script():
    global current_status
    current_status = "Running"
    print("Script started. Status updated.")
    return jsonify({'message': 'Status updated to Running'})

@app.route('/approve', methods=['GET'])
def grant_approval():
    global approval_granted
    approval_granted = True
    print("Approval granted. The script can now continue.")
    return jsonify({'message': 'Approval granted'})

# New route for the script to check for approval
@app.route('/check-approval', methods=['GET'])
def check_approval():
    return jsonify({'approved': approval_granted})

# def run_backend():
#     app.run(host="127.0.0.1", port=6000, debug=True)

if __name__ == '__main__':
    # backend_thread = threading.Thread(target=run_backend)
    # backend_thread.start()
    app.run(host="127.0.0.1", port=5000, debug=True)
    print("Backend server is running on http://127.0.0.1:6000")