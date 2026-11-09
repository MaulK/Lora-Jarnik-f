from transport import SdrUdpTransport, SerialTransport
from ui.ui_screen import UIScreen

from storage.system_logger import SystemLogger
from storage.file_storage import FileStorage

from app.stream_data_generator import StreamDataGenerator
from app.application import Application
from app.crc32_calculator import CRC32Calculator

system_logger = SystemLogger()
file_storage = FileStorage()
crc32_calculator = CRC32Calculator()
stream_data_generator = StreamDataGenerator()

application = Application(
    logger=system_logger,
    file_storage=file_storage,
    crc32_calculator=crc32_calculator,
    stream_data_generator=stream_data_generator,
)

ui_screen = UIScreen(application=application)
ui_screen.show()
from protocol import create_packets, decode_packet, reassemble_packets
