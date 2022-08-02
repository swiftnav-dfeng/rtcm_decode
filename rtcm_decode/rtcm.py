from bitarray import bitarray
from bitarray.util import ba2int
from rtcm_decode.data_fields import *
from crc import CrcCalculator, Configuration
import logging


class CRCQ24:
    def __init__(self):
        self.crc_configuration = Configuration(width=24, polynomial=0x1864CFB)
        self.crc_calculator = CrcCalculator(self.crc_configuration, True)

    def calculate_checksum(self, msg):
        checksum = self.crc_calculator.calculate_checksum(msg)
        return checksum


class RTCMMsg:
    dfs = []

    def __init__(self, msg:bytearray, crcq24: CRCQ24 = None):
        self.msg = msg
        self._ba = bitarray(buffer = msg, endian='big')

        self.current_bit = 0
        # header info
        self.preamble = ba2int(self._get_n_bits(8))
        self.reserved1 = ba2int(self._get_n_bits(6))
        self.length = self._get_n_bits(10)
        self.msg_type = ba2int(self._get_n_bits(12))

        self.body_obj = None

        self.crc = self.get_crc()

        # check crc
        if crcq24 is None:
            crcq24 = CRCQ24()

        self.checksum = crcq24.calculate_checksum(msg[:-3])
        if self.checksum_passed():
            body_cls = rtcm_lookup.get(self.msg_type, None)
            if body_cls is not None:
                self.body_obj = body_cls(self._ba[self.current_bit:])
        else:
            logging.warn(f'checksum failed header crc = {self.crc}, calculated = {self.checksum}')

    def get_crc(self):
        return ba2int(self._ba[-24:])
    
    def checksum_passed(self):
        return self.checksum == self.crc

    def _get_n_bits(self, n):
        val = self._ba[self.current_bit:self.current_bit+n]
        self.current_bit += n
        return val
    
            
class RTCMBody:
    def __init__(self, body: bitarray) -> None:
        self._ba = body
        self.current_bit = 0
        self.body_data = []
        pass

    def _get_n_bits(self, n):
        val = self._ba[self.current_bit:self.current_bit+n]
        self.current_bit += n
        return val

    def _get_body_data(self):
        for df in self.dfs:
            self.body_data.append(df(self._get_n_bits(df.length)))
    
class RTCMMsm5(RTCMBody):
    # header
    dfs = [
        DF003,
        GNSSEpochTime,
        DF393,
        DF409,
        DF001,
        DF411,
        DF412,
        DF417,
        DF418,
        DF394,
        DF395
        # cell mask last (DF396)
    ]

    def __init__(self, body: bitarray) -> None:
        super().__init__(body)

        self._get_body_data()
        
        self.nsat = self.body_data[-2].nsat
        self.nsig = self.body_data[-1].nsig
        self.sat_data = []
        self.sig_data = []

        cellmask_length = self.nsat * self.nsig

        self.body_data.append(DF396(self._get_n_bits(cellmask_length)))

        self.sat_data.append(SatDataMSM5(self._ba, self.nsat, self.current_bit))
        self.current_bit = self.sat_data[-1].current_bit

        self.sig_data.append(SignalDataMSM5(self._ba, self.nsig, self.current_bit))
        self.current_bit = self.sig_data[-1].current_bit

class SatData:

    dfs = []

    def __init__(self, msg, nsat, current_bit) -> None:
        self.msg = msg
        self.nsat = nsat
        self.current_bit = current_bit
        pass

    def _get_n_bits(self, n):
        val = self.msg[self.current_bit:self.current_bit+n]
        self.current_bit += n
        return val

    def _collect_sat_data(self):
        fields = []
        for df in self.dfs:
            df_list = []
            for _ in range(self.nsat):
                df_list.append(df(self._get_n_bits(df.length)))
            fields.append(df_list)
        
        return fields

class SatDataMSM5(SatData):
    dfs = [
        DF397,
        ExtendedSatInfo,
        DF398,
        DF399
    ]
    def __init__(self, msg, nsat, current_bit) -> None:
        super().__init__(msg, nsat, current_bit)

        self.sat_data = self._collect_sat_data()

class SignalData:
    dfs = []

    def __init__(self, msg, nsig, current_bit) -> None:
        self._ba = msg
        self.nsig = nsig
        self.current_bit = current_bit
        pass

    def _get_n_bits(self, n):
        val = self._ba[self.current_bit:self.current_bit+n]
        self.current_bit += n
        return val

    def _collect_sig_data(self):
        fields = []
        for df in self.dfs:
            df_list = []
            for _ in range(self.nsig):
                df_list.append(df(self._get_n_bits(df.length)))
            fields.append(df_list)
        
        return fields

class SignalDataMSM5(SignalData):
    dfs = [DF400, DF401, DF402, DF420, DF403, DF404]

    def __init__(self, msg, nsig, current_bit) -> None:
        super().__init__(msg, nsig, current_bit)

        self.signal_data = self._collect_sig_data()

class RTCM1005(RTCMBody):

    dfs = [DF003, DF021, DF022, DF023, DF024, DF141, DF025, DF142, DF001, DF026, DF364, DF027]

    def __init__(self, body: bitarray) -> None:
        super().__init__(body)

        self._get_body_data()

        

rtcm_lookup = {
    1005: RTCM1005,
    1075: RTCMMsm5,
    1085: RTCMMsm5,
    1095: RTCMMsm5,
    1105: RTCMMsm5,
    1115: RTCMMsm5,
    1125: RTCMMsm5
}
    