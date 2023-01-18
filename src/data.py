from __future__ import annotations

import json


class Data:
    __instance: Data

    def __init__(self) -> None:
        Data.__instance = self
        self.read()

    def read(self) -> dict:
        if self.data == None:
            with open("data.json", "r") as f:
                self.data = json.loads(f.read())
        return self.data

    def write(self, key: str, value: dict):
        self.data[key] = value
        with open("data.json", "w") as f:
            f.write(json.dumps(self.data))

    @classmethod
    def get(cls):
        return cls.__instance
