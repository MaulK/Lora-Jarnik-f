from storage.system_logger import SystemLogger
from model.file import File
from storage.file_storage import FileStorage
from .crc32_calculator import CRC32Calculator


class Application:
    __slots__ = ("logger", "file_storage", "crc32_calculator", "loaded_file")

    logger: SystemLogger
    file_storage: FileStorage
    loaded_file: File | None
    crc32_calculator: CRC32Calculator

    def __init__(
        self,
        logger: SystemLogger,
        file_storage: FileStorage,
        crc32_calculator: CRC32Calculator,
    ):
        self.logger = logger
        self.loaded_file = None
        self.file_storage = file_storage
        self.crc32_calculator = crc32_calculator

    def load_file(self, path: str):
        self.logger.log_event(f"[INFO]: Load file {path}")
        try:
            self.loaded_file = self.file_storage.read_file(path=path)
            self.logger.log_event("[INFO]: File loaded.")
        except Exception as e:
            self.logger.log_event(f"[ERROR]: {e}")
            raise e

    def get_loaded_file_path(self) -> str | None:
        if self.loaded_file == None:
            return None
        else:
            return self.loaded_file.path

    def calculate_crc32_of_loaded_file(self) -> str:
        self.logger.log_event("[INFO]: Calculating CRC32 of loaded file")
        if self.loaded_file == None:
            self.logger.log_event("[ERROR]: No file loaded.")
            raise FileNotFoundError(f"File not found.")
        crc_result = self.crc32_calculator.get_crc32(self.loaded_file.data)
        self.logger.log_event(f"[INFO]: CRC32 result {crc_result}")
        return crc_result
