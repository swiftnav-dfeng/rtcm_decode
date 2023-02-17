from bitarray import bitarray
from bitarray.util import ba2int
from rtcm_decode.data_fields import *
from crc import Calculator, Configuration
import logging
from copy import deepcopy

logger = logging.getLogger(__name__)


class CRCQ24:
    def __init__(self):
        self.crc_configuration = Configuration(width=24, polynomial=0x1864CFB)
        self.crc_calculator = Calculator(self.crc_configuration, True)

    def calculate_checksum(self, msg):
        checksum = self.crc_calculator.checksum(msg)
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

    def get_observations(self):
        pass




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
        self.sats = self.data_fields[10].value
        self.sig_data = []
        self.sigs = self.data_fields[11].value
        self.observations = []
        

        cellmask_length = self.nsat * self.nsig
        self.data_fields.append(DF396(self._get_n_bits(cellmask_length)))
        self.cellmask = self.data_fields[-1].value


class RTCMMsm5(RTCMMsm):
    def __init__(self, body: bitarray) -> None:
        super().__init__(body)
        
        self.sat_data = SatDataMSM5(self.msg, self.nsat, self._current_bit)
        self._current_bit = self.sat_data._current_bit

        self.sig_data = SignalDataMSM5(self.msg, self.data_fields[-1].ncell, self._current_bit)

        self.calc_obs()

    def calc_obs(self):
        cellmask_index = 0
        signal_index = 0
        for sat in range(len(self.sats)):
            for sig in self.sigs:
                if bool(self.cellmask[cellmask_index]):
                    observation = {
                        'sat': self.sats[sat],
                        'sig': sig,
                        'pseudorange': self.sig_data.sig_data[signal_index]['fine_range'] + self.sat_data.sat_data[sat]['rough_range'],
                        'phaserange': self.sig_data.sig_data[signal_index]['fine_phaserange'],
                        'phaserangerate': self.sig_data.sig_data[signal_index]['fine_phaserangerate'] + self.sat_data.sat_data[sat]['rough_phaserangerate'],
                        'extended_sat_info': self.sat_data.sat_data[sat]["extended_sat_info"],
                        'lock_time': self.sig_data.sig_data[signal_index]['lock_time'],
                        'CNR': self.sig_data.sig_data[signal_index]['CNR'],
                        'half_cycle_amb_ind': self.sig_data.sig_data[signal_index]['half_cycle_amb_ind']
                    }
                    self.observations.append(observation)
                    signal_index += 1
                cellmask_index += 1

class SatData:

    dfs = []

    SAT_DATA = {
        "rough_range": 0,
        "rough_phaserangerate": 0,
        "extended_sat_info": None
    }

    def __init__(self, msg, nsat, current_bit) -> None:
        self.msg = msg
        self.nsat = nsat
        self._current_bit = current_bit
        self.data_fields = []
        self.sat_data = []
        pass

    def _get_n_bits(self, n):
        val = self.msg[self._current_bit:self._current_bit+n]
        self._current_bit += n
        return val

    def _collect_sat_data(self):
        fields = []
        for df in self.dfs:
            df_list = []
            for _ in range(self.nsat):
                df_list.append(df(self._get_n_bits(df.length)))
            fields.append(df_list)
        
        return fields

    def _parse_sat_data(self):
        for sat_data in list(zip(*self.data_fields)):
            d = deepcopy(self.SAT_DATA)

            d["rough_range"] = sat_data[0].value + sat_data[2].value * 2**-10
            d["rough_phaserangerate"] = sat_data[3].value
            d["extended_sat_info"] = sat_data[1].value

            self.sat_data.append(d)



class SatDataMSM5(SatData):
    dfs = [
        DF397,
        ExtendedSatInfo,
        DF398,
        DF399
    ]
    def __init__(self, msg, nsat, current_bit) -> None:
        super().__init__(msg, nsat, current_bit)

        self.data_fields = self._collect_sat_data()
        self._parse_sat_data()

class SignalData:
    dfs = []

    SIG_DATA = {
        "fine_range": 0,
        "fine_phaserange": 0,
        "lock_time": None,
        "half_cycle_amb_ind": None,
        "CNR": None,
        "fine_phaserangerate": 0
    }

    def __init__(self, msg, nsig, current_bit) -> None:
        self._ba = msg
        self.nsig = nsig
        self._current_bit = current_bit

        self.data_fields = []
        self.sig_data = []

    def _get_n_bits(self, n):
        val = self._ba[self._current_bit:self._current_bit+n]
        self._current_bit += n
        return val

    def _collect_sig_data(self):
        fields = []
        for df in self.dfs:
            df_list = []
            for _ in range(self.nsig):
                df_list.append(df(self._get_n_bits(df.length)))
            fields.append(df_list)
        
        return fields

    def _parse_sig_data(self):
        for sig_data in list(zip(*self.data_fields)):
            d = deepcopy(self.SIG_DATA)

            d["fine_range"] = sig_data[0].value * 2**-24
            d["fine_phaserange"] = sig_data[1].value * 2**-29
            d["fine_phaserangerate"] = sig_data[5].value * 0.0001
            d["half_cycle_amb_ind"] = sig_data[3].value
            d["CNR"] = sig_data[4].value
            d["lock_time"] = sig_data[2].value

            self.sig_data.append(d)

class SignalDataMSM5(SignalData):
    dfs = [DF400, DF401, DF402, DF420, DF403, DF404]

    def __init__(self, msg, nsig, current_bit) -> None:
        super().__init__(msg, nsig, current_bit)

        self.data_fields = self._collect_sig_data()
        self._parse_sig_data()


rtcm_lookup = {
    1005: RTCM1005,
    1075: RTCMMsm5,
    1085: RTCMMsm5,
    1095: RTCMMsm5,
    1105: RTCMMsm5,
    1115: RTCMMsm5,
    1125: RTCMMsm5
}
    