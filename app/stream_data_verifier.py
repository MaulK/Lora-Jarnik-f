class StreamDataVerifier:
    __slots__ = "last_data"

    last_data: int | None

    def __init__(self):
        self.reset()

    def reset(self):
        self.last_data = None

    def verify(self, data: int) -> bool:
        result = False

        if self.last_data == None:
            result = True
        else:
            if (self.last_data == 100 and data == 1) or (data == self.last_data + 1):
                result = True
            else:
                result = False

        self.last_data = data
        return result
