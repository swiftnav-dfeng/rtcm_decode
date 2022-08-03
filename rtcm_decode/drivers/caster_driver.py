import socket
import base64
from rtcm_decode.drivers.driver import BaseDriver



class CasterDriver(BaseDriver):

    MP_HEADER = """\
GET /{mountpoint} HTTP/1.1\r\n\
Host: {host}\r\n\
Ntrip-Version: Ntrip/1.0\r\n\
User-Agent: NTRIP caster_driver\r\n\
Authorization: Basic {auth}\r\n\
Connection: close\r\n\
\r\n
    """

    def __init__(self, address: str, port: int, mountpoint: str, username: str = None, password: str = None):
        self.address = address
        self.port = port
        self.mountpoint = mountpoint
        self.auth = base64.b64encode(f'{username}:{password}'.encode('ASCII')).decode()

        self.s = None 

        self.buf = bytearray()

    def __enter__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(5)
        self.s.connect((self.address, self.port))
        print('request data')
        self.request_data()

        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.s.close()
        print(exc_type)
        print(exc_value)
        print(exc_traceback)
        pass

    def _send_msg(self, msg):
        totalsent = 0
        while totalsent < len(msg):
            sent = self.s.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent
        pass

    def read(self, bytes):
        b = self.s.recv(min(bytes, 2048))
        print(b)
        if len(b) == 0 and len(self.buf) == 0:
            raise RuntimeError("socket closed")

        self.buf += bytearray(b)

        ret, self.buf = self.buf[:bytes], self.buf[bytes:]
        return ret

    def request_data(self):
        self._send_msg(self.MP_HEADER.format(mountpoint=self.mountpoint, host=self.address, auth=self.auth).encode('ASCII'))

