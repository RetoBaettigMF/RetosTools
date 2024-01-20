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
    
    def clear(self):
        self.history = []
    
    def print_statistics(self):
        print("Number of entries in history: %d" % len(self.history))
        if len(self.history) == 0:
            return
        
        ok = 0
        for entry in self.history:
            if entry["ok"]:
                ok += 1
        
        print("Percentage of good answers in history: %.2f%%" % ((ok / len(self.history)*100)))