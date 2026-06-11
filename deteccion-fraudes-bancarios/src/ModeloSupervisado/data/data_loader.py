import pandas as pd

class DataLoader:

    def __init__(self, filepath):
        self.filepath = filepath

    def load(self):
        return pd.read_csv(self.filepath)