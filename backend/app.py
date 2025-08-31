from flask import Flask, jsonify
import os

app = Flask(__name__)

# Path to the "computers" directory
BASE_DIR = os.path.join(os.path.dirname(__file__), "computers")

@app.route("/computers")
def list_computers():
    """Return list of all computers (folders inside /computers)."""
    try:
        computers = [
            d for d in os.listdir(BASE_DIR)
            if os.path.isdir(os.path.join(BASE_DIR, d))
        ]
        return jsonify(computers)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/computer/<name>")
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


if __name__ == "__main__":
    app.run(debug=True)
