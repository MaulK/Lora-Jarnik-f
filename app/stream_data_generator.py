class StreamDataGenerator:
    __slots__ = "current_data"

    current_data: int

    def __init__(self):
        self.reset()

    def reset(self):
        self.current_data = 0

    def get_data(self) -> int:
        used_data = self.current_data + 1  # convert 0-99 to 1-100
        self.current_data = (self.current_data + 1) % 100
        return used_data
