from bitarray import bitarray
from bitarray.util import ba2int
from rtcm_decode.data_fields import *
from crc import CrcCalculator, Configuration
import logging

logger = logging.getLogger(__name__)


class CRCQ24:
    def __init__(self):
        self.crc_configuration = Configuration(width=24, polynomial=0x1864CFB)
        self.crc_calculator = CrcCalculator(self.crc_configuration, True)

    def calculate_checksum(self, msg):
        checksum = self.crc_calculator.calculate_checksum(msg)
        return checksum

# RTCM transport frame as defined in RTCM 10403.3, section 4
class RTCMFrame:
    dfs = []

    def __init__(self, frame:bytearray, crcq24: CRCQ24 = None):
        self.frame = frame
        self._ba = bitarray(buffer = frame, endian='big')

        self.current_bit = 0
        # transport info, RTCM 10403.3, section 4.1
        self.preamble = ba2int(self._ba[0:8])
        self.reserved1 = ba2int(self._ba[8:14])
        self.length = ba2int(self._ba[14:24])
        self.msg_type = None
        if self.length > 0:
            self.msg_type = ba2int(self._ba[24:36])

        self.msg = None

        self.crc = ba2int(self._ba[-24:])

        # check crc
        if crcq24 is None:
            crcq24 = CRCQ24()

        self.checksum = crcq24.calculate_checksum(frame[:-3])
        
        if self.checksum_passed():
            # empty messages allowed for keep alive
            if self.length > 0:
                body_cls = rtcm_lookup.get(self.msg_type, None)
                if body_cls is not None:
                    self.msg = body_cls(self._ba[24:-24])
        else:
            logging.warn(f'checksum failed header crc = {self.crc}, calculated = {self.checksum}')

    
    def checksum_passed(self):
        return self.checksum == self.crc

    # def _get_n_bits(self, n):
    #     val = self._ba[self.current_bit:self.current_bit+n]
    #     self.current_bit += n
    #     return val
    
# RTCM message (presentation layer) as defined in RTCM 10403.3, section 3
class RTCMMsg:

    df_types = []

    def __init__(self, msg: bitarray) -> None:
        self.msg = msg

        self._current_bit = 0
        
        self.data_fields = []


    def _get_n_bits(self, n):
        val = self.msg[self._current_bit:self._current_bit+n]
        self._current_bit += n
        return val

    def _get_data_fields(self):
        for df_type, length in self.df_types:
            if length == None:
                self.data_fields.append(df_type(self._get_n_bits(df_type.length)))
            else:
                self.data_fields.append(df_type(self._get_n_bits(length), length=length))

    def get_msg_dict(self):
        msg_dict = {}

        for cls in self.data_fields:
            msg_dict[cls.name] = (cls.value, cls.unit)

        return msg_dict




class RTCM1005(RTCMMsg):

    df_types = [
        (DF002, None), 
        (DF003, None), 
        (DF021, None), 
        (DF022, None), 
        (DF023, None), 
        (DF024, None), 
        (DF141, None), 
        (DF025, None), 
        (DF142, None), 
        (DF001, None), 
        (DF026, None), 
        (DF364, None), 
        (DF027, None)
    ]


    def __init__(self, msg: bitarray) -> None:
        super().__init__(msg)

        self._get_data_fields()


class RTCMMsm(RTCMMsg):
    # header
    df_types = [
        (DF002, None),
        (DF003, None),
        (GNSSEpochTime, None),
        (DF393, None),
        (DF409, None),
        (DF001, 7),
        (DF411, None),
        (DF412, None),
        (DF417, None),
        (DF418, None),
        (DF394, None),
        (DF395, None)
        # cell mask last (DF396)
    ]

    def __init__(self, body: bitarray) -> None:
        super().__init__(body)

        self._get_data_fields()
        
        self.nsat = self.data_fields[-2].nsat
        self.nsig = self.data_fields[-1].nsig
        self.sat_data = []
        self.sig_data = []

        cellmask_length = self.nsat * self.nsig

        self.data_fields.append(DF396(self._get_n_bits(cellmask_length)))


class RTCMMsm5(RTCMMsm):
    def __init__(self, body: bitarray) -> None:
        super().__init__(body)
        
        self.sat_data = SatDataMSM5(self.msg, self.nsat, self._current_bit)
        self._current_bit = self.sat_data.current_bit

        self.sig_data = SignalDataMSM5(self.msg, self.nsig, self._current_bit)

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


rtcm_lookup = {
    1005: RTCM1005,
    1075: RTCMMsm5,
    1085: RTCMMsm5,
    1095: RTCMMsm5,
    1105: RTCMMsm5,
    1115: RTCMMsm5,
    1125: RTCMMsm5
}
    