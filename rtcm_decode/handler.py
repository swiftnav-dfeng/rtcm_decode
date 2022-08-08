from crc import CrcCalculator, Configuration
import logging

from rtcm_decode.rtcm import RTCMFrame, CRCQ24

logger = logging.getLogger(__name__)

class Handler():
    def __init__(self, handle, callback):
        self.handle = handle
        self.data = bytearray()
        self.frame = bytearray()
        self.frame_length = None
        self.header = None

        self.crcq24 = CRCQ24()

        self.callback = callback


    def process(self):
        while True:
            buf = bytearray(b'')
            if self.handle is not None:
                buf = bytearray(self.handle.read(1024))
            
            self.insert_data(buf)
            if len(self.data) == 0:
                break
            self.framer()
        
        logging.info('no data available, returning')

    def insert_data(self, data:bytearray):
        self.data += data

    def framer(self):
        while True:
            try:
                b = self.data.pop(0)
                if len(self.frame) == 0:
                    # 1st byte, preamble
                    if b == 0xd3:
                        self.frame.append(b)
                elif len(self.frame) == 1:
                    # 2nd byte, first 6 bits reserved, standard says to ignore
                    self.frame.append(b)
                elif len(self.frame) == 2:
                    # third byte of "header"
                    self.frame.append(b)
                    self.frame_length = (self.frame[2]) + ((self.frame[1] & 0x03) << 8)
                    if self.frame_length > 1023:
                        # valid lengths are 0-1023, reset frame
                        logging.warn(f"invalid frame length {self.frame_length}, frame {self.frame}")
                        self.data = self.frame[1:] + self.data
                        self.reset_frame()
                elif (self.frame_length is not None) and (len(self.frame) == self.frame_length + 5):
                    # frame_length does not include header (3 bytes) and crc (3 bytes)
                    self.frame.append(b)

                    # frame complete
                    msg = RTCMFrame(self.frame, self.crcq24)
                    if msg.checksum_passed() is False:
                        logging.warn(f"CRC check failed on frame {self.frame}")
                        # crc failed, reset frame
                        # reinsert all bytes, except the preamble back into data
                        self.data = self.frame[1:] + self.data
                    self.callback(msg)      
                    self.reset_frame()
                else:
                    # in middle of SBF message, read more
                    self.frame.append(b)
            except IndexError as e:
                # self.data is empty, get more data
                break

    def reset_frame(self):
        self.header = None
        self.frame_length = None
        self.frame = bytearray()

    def check_frame(config, crc, data):
        # perform crc check
        crc_calculator = CrcCalculator(config, True)

        checksum = crc_calculator.calculate_checksum(data)
        if checksum == crc:
            return True
        else:
            logging.warn(f'checksum failed header crc = {crc}, calculated = {checksum}')
            return False
        


        