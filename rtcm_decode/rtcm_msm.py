from rtcm_decode.rtcm import RTCMMsg
from rtcm_decode.data_fields import *

class RTCMMsm(RTCMMsg):
    # header
    df_types = [
        DF003,
        GNSSEpochTime,
        DF393,
        DF409,
        DF001,
        DF001,
        DF001,
        DF001,
        DF001,
        DF001,
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
        
        self.sat_data.append(SatDataMSM5(self.msg, self.nsat, self.current_bit))
        self.current_bit = self.sat_data[-1].current_bit

        self.sig_data.append(SignalDataMSM5(self.msg, self.nsig, self.current_bit))
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