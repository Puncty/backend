import json


class Storage:
    def __init__(self, storage_file="./data.json", autoload=True) -> None:
        self.data = {}
        self.storage_file = storage_file
        if autoload:
            self.load()

    def __setitem__(self, key: str, value):
        self.data[key] = value
        self.store()

    def __getitem__(self, key):
        return self.data[key]

    def store(self) -> None:
        with open(self.storage_file, "w") as f:
            f.write(json.dumps(self.data))

    def load(self) -> None:
        try:
            with open(self.storage_file, "r") as f:
                self.data = self.data | json.loads(f.read())
        except:
            pass
