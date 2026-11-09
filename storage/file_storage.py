from pathlib import Path
from model.file import File


class FileStorage:
    def read_file(self, path: str) -> File:
        target_path = Path(path)

        if not target_path.is_file():
            raise FileNotFoundError(f"File not found.")

        data = target_path.read_bytes()
        return File(path=str(target_path.resolve()), data=data)

    def save_file(self, file: File):
        target_path = Path(file.path)

        target_path.parent.mkdir(parents=True, exist_ok=True)

        target_path.write_bytes(file.data)
