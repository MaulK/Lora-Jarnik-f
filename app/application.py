from storage.system_logger import SystemLogger
from model.file import File
from storage.file_storage import FileStorage
from storage.data_stream_logger import DataStreamLogger
from .crc32_calculator import CRC32Calculator
from .stream_data_generator import StreamDataGenerator
from .stream_data_verifier import StreamDataVerifier
from datetime import datetime
import time
from typing import Callable


class Application:
    __slots__ = (
        "logger",
        "file_storage",
        "crc32_calculator",
        "loaded_file",
        "stream_data_generator",
        "stream_data_verifier",
        "data_stream_logger",
    )

    logger: SystemLogger
    file_storage: FileStorage
    loaded_file: File | None
    crc32_calculator: CRC32Calculator
    stream_data_generator: StreamDataGenerator
    stream_data_verifier: StreamDataVerifier
    data_stream_logger: DataStreamLogger

    def __init__(
        self,
        logger: SystemLogger,
        file_storage: FileStorage,
        crc32_calculator: CRC32Calculator,
        stream_data_generator: StreamDataGenerator,
        stream_data_verifier: StreamDataVerifier,
        data_stream_logger: DataStreamLogger,
    ):
        self.logger = logger
        self.loaded_file = None
        self.file_storage = file_storage
        self.crc32_calculator = crc32_calculator
        self.stream_data_generator = stream_data_generator
        self.stream_data_verifier = stream_data_verifier
        self.data_stream_logger = data_stream_logger

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

    def send_loaded_file(self):
        self.logger.log_event("[INFO]: Start sending file")
        if self.loaded_file == None:
            self.logger.log_event("[ERROR]: No file loaded.")
            raise FileNotFoundError(f"File not found.")
        time.sleep(5)  # replace with send via LoRa
        self.logger.log_event("[INFO]: File sent")

    def start_sending_stream_data(self, report_sending_data: Callable[[int], None]):
        self.logger.log_event("[INFO]: Start sending stream data")
        self.stream_data_generator.reset()
        while True:
            current_data = self.stream_data_generator.get_data()
            self.logger.log_event(f"[INFO]: Sending stream data: {current_data}")
            report_sending_data(current_data)
            time.sleep(1)  # replace with send with LoRa

    def start_receiving_stream_data(
        self, report_receiving_data: Callable[[int, bool], None]
    ):
        self.logger.log_event("[INFO]: Start receiving stream data")
        self.data_stream_logger.start_session()
        self.stream_data_verifier.reset()
        temp_data = 0  # remove later
        while True:
            # replace with receive data via Lora
            time.sleep(1)
            # received_data must be int
            received_data = temp_data + 1

            if temp_data % 5 == 0:  # remove later
                temp_data = temp_data + 1  # remove later
            temp_data = (temp_data + 1) % 100  # remove later

            is_valid = self.stream_data_verifier.verify(received_data)
            report_receiving_data(received_data, is_valid)
            self.data_stream_logger.log(data=received_data, is_valid=is_valid)
            self.logger.log_event(
                f"[INFO]: Received stream data: {received_data} {'' if is_valid else '(INVALID)'}"
            )
