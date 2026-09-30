from pathlib import Path
import tomllib


class Settings:
    def __init__(self, path: str | Path):
        self.path = Path(path)

        with self.path.open("rb") as file:
            self.data = tomllib.load(file)

    def get(self, key: str, default=None):
        return self.data.get(key, default)

    def __getitem__(self, key: str):
        return self.data[key]