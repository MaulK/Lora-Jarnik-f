import socket
import time

try:
    import serial
except ImportError:
    serial = None


class BaseTransport:
    def open(self, is_receiver=False):
        pass

    def send(self, data_str: str):
        pass

    def recv(self, timeout=1.0) -> str:
        pass

    def close(self):
        pass


class SdrUdpTransport(BaseTransport):
    def __init__(self, listen_ip="0.0.0.0", listen_port=5005, target_ip="127.0.0.1", target_port=5005):
        self.listen_ip = listen_ip
        self.listen_port = listen_port
        self.target_ip = target_ip
        self.target_port = target_port
        self.sock = None

    def open(self, is_receiver=False):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if is_receiver:
            self.sock.bind((self.listen_ip, self.listen_port))
            self.sock.settimeout(2.0)
        else:
            self.sock.settimeout(2.0)

    def send(self, data_str: str):
        payload = (data_str + "\n").encode("utf-8")
        self.sock.sendto(payload, (self.target_ip, self.target_port))

    def recv(self, timeout=1.0) -> str:
        if timeout is not None:
            self.sock.settimeout(timeout)
        try:
            data, _ = self.sock.recvfrom(4096)
            return data.decode("utf-8", errors="ignore").strip()
        except (socket.timeout, BlockingIOError):
            return None

    def close(self):
        if self.sock:
            try:
                self.sock.close()
            except Exception:
                pass


class SerialTransport(BaseTransport):
    def __init__(self, port="COM3", baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self.ser = None

    def open(self, is_receiver=False):
        if serial is None:
            raise ImportError("Pustaka 'pyserial' belum terinstall. Install dengan: pip install pyserial")
        self.ser = serial.Serial(self.port, self.baudrate, timeout=1.0)
        time.sleep(1.0)

    def send(self, data_str: str):
        payload = (data_str + "\n").encode("utf-8")
        self.ser.write(payload)

    def recv(self, timeout=1.0) -> str:
        if self.ser.in_waiting > 0:
            line = self.ser.readline().decode("utf-8", errors="ignore").strip()
            return line if line else None
        return None

    def close(self):
        if self.ser:
            try:
                self.ser.close()
            except Exception:
                pass
