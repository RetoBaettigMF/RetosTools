from fileoperations import read_file, write_file
import json

class history:
    def __init__(self, filename):
        self.filename = filename
        self.load()

    def save(self):
        write_file(self.filename, json.dumps(self.history))

    def load(self):
        try:
            self.history = json.loads(read_file(self.filename))
        except:
            self.history = []

    def add(self, state):
        if state:
            self.history.append(state)

    def get(self):
        return self.history