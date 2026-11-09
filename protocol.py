import struct
import zlib
import base64
import secrets
import binascii

MAGIC = b"LORA"
VERSION = 1
MAX_CHUNK_SIZE = 1024

HEADER_FORMAT = "!4sBIIIH"
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)
CRC_SIZE = 4

class ProtocolError(Exception):
    pass

def create_packets(data, chunk_size=MAX_CHUNK_SIZE):
    if not isinstance(data, bytes):
        raise TypeError("Data harus berupa bytes")

    if chunk_size <= 0 or chunk_size > MAX_CHUNK_SIZE:
        raise ValueError("Ukuran chunk tidak valid")

    transfer_id = secrets.randbits(32)
    total_packets = max(1, (len(data) + chunk_size - 1) // chunk_size)
    packets = []

    for sequence in range(total_packets):
        start = sequence * chunk_size
        end = start + chunk_size
        payload = data[start:end]
        header = struct.pack(
            HEADER_FORMAT,
            MAGIC,
            VERSION,
            transfer_id,
            sequence,
            total_packets,
            len(payload)
        )
        checksum = zlib.crc32(header + payload) & 0xFFFFFFFF
        packet = header + struct.pack("!I", checksum) + payload
        encoded_packet = base64.b64encode(packet).decode("ascii")
        packets.append(encoded_packet)
    return packets

def decode_packet(encoded_packet):
    try:
        packet = base64.b64decode(encoded_packet, validate=True)
    except (binascii.Error, ValueError):
        raise ProtocolError("Format Base64 tidak valid")

    if len(packet) < HEADER_SIZE + CRC_SIZE:
        raise ProtocolError("Ukuran paket terlalu kecil")
    
    header = packet[:HEADER_SIZE]
    (
        magic,
        version,
        transfer_id,
        sequence,
        total_packets,
        payload_length
    ) = struct.unpack(HEADER_FORMAT, header)

    received_crc = struct.unpack(
        "!I",
        packet[HEADER_SIZE:HEADER_SIZE + CRC_SIZE]
    )[0]

    payload = packet[HEADER_SIZE + CRC_SIZE:]

    if magic != MAGIC:
        raise ProtocolError("Magic number tidak valid")
    if version != VERSION:
        raise ProtocolError("Versi protokol tidak didukung")
    if total_packets == 0 or sequence >= total_packets:
        raise ProtocolError("Nomor paket tidak valid")
    if payload_length > MAX_CHUNK_SIZE:
        raise ProtocolError("Payload terlalu besar")
    if len(payload) != payload_length:
        raise ProtocolError("Panjang payload tidak sesuai")
    
    calculated_crc = zlib.crc32(header + payload) & 0xFFFFFFFF
    if calculated_crc != received_crc:
        raise ProtocolError("CRC32 tidak cocok, data rusak")

    return {
        "transfer_id": transfer_id,
        "sequence": sequence,
        "total_packets": total_packets,
        "payload": payload
    }

def reassemble_packets(encoded_packets):
    received_data = {}
    transfer_id = None
    total_packets = None

    for encoded_packet in encoded_packets:
        packet = decode_packet(encoded_packet)

        if transfer_id is None:
            transfer_id = packet["transfer_id"]
            total_packets = packet["total_packets"]
        if packet["transfer_id"] != transfer_id:
            raise ProtocolError("Transfer ID berbeda")
        if packet["total_packets"] != total_packets:
            raise ProtocolError("Jumlah paket tidak konsisten")

        sequence = packet["sequence"]
        payload = packet["payload"]

        if sequence in received_data:
            if received_data[sequence] != payload:
                raise ProtocolError("Duplikasi paket dengan data berbeda")
        else:
            received_data[sequence] = payload

    if total_packets is None:
        raise ProtocolError("Tidak ada paket yang diterima")

    if len(received_data) != total_packets:
        missing = [
            i for i in range(total_packets)
            if i not in received_data
        ]
        raise ProtocolError(f"Paket hilang: {missing}")

    result = b""

    for sequence in range(total_packets):
        result += received_data[sequence]

    return result