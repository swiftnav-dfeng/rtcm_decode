from bitarray import bitarray
from bitarray.util import ba2int
from data_fields import *
from crc import CrcCalculator, Configuration


class RTCMMsg:
    dfs = []

    def __init__(self, msg:bytearray):
        self.msg = msg
        self._ba = bitarray(buffer = msg, endian='big')
        self.length = self.get_length()
        self.msg_type = self.get_msg_type()
        self.crc = self.get_crc()

        self.current_bit = 0

        self.obj_data = []
        self._get_obj_data()

    def get_length(self):
        return ba2int(self._ba[14:24])

    def get_msg_type(self):
        return ba2int(self._ba[24:36])

    def get_crc(self):
        return ba2int(self._ba[-24:])

    def get_n_bits(self, n):
        val = self._ba[self.current_bit:self.current_bit+n]
        self.current_bit += n
        return val
    
    def _get_obj_data(self):
        for df in self.dfs:
            self.obj_data.append(df(self.get_n_bits(df.length)))
            

    
class RTCMMsm5(RTCMMsg):
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

    def __init__(self, msg):
        super().__init__(msg)
    
        self.current_bit = 36

        self._get_obj_data()

        cellmask_length = self.obj_data[-2].nsat * self.obj_data[-1].nsig
        self.obj_data.append(DF396(self.get_n_bits(cellmask_length)))

class RTCM1005(RTCMMsg):

    dfs = [DF003, DF021, DF022, DF023, DF024, DF141, DF025, DF142, DF001, DF026, DF364, DF027]

    def __init__(self, msg):
        super().__init__(msg)

        self.current_bit = 36

        self._get_obj_data()

        

rtcm_lookup = {
    1005: RTCM1005,
    1075: RTCMMsm5,
    1085: RTCMMsm5,
    1095: RTCMMsm5,
    1105: RTCMMsm5,
    1115: RTCMMsm5,
    1125: RTCMMsm5
}
    