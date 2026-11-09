class File:
    __slots__ = ("path", "data")

    def __init__(self, path: str, data: bytes):
        self.path = path
        self.data = data
