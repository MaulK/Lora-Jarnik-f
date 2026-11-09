import zlib


class CRC32Calculator:
    def get_crc32(self, data: bytes) -> str:
        crc = zlib.crc32(data)
        return f"{crc:08x}"
