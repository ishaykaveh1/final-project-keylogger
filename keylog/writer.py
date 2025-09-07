class FileWriter:
    def __init__(self, filename):
        self.filename = filename

    def write_data(self, data: str):
        """שומר את הנתונים המוצפנים לקובץ"""
        with open(self.filename, "a", encoding="utf-8") as f:
            f.write(data + "\n")