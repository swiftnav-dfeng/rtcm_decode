
from rtcm_decode.next_bits import next_bits

class MSMMsg():
    def __init__(self, msg_type, data):
        # bit array - include message payload
        self.msg_type = msg_type
        self.data = data
        self.reference_station_ID = None
        self.gnss_epoch_time = None
        self.glo_dow = None
        self.glo_epoch_time = None
        self.multiple_message_bit = None
        self.iods = None
        self.reserved1 = None
        self.clock_steering = None
        self.ext_clock = None
        self.smoothing = None
        self.smoothing_int = None
        self.nsat = None
        self.sat_mask = None
        self.nsig = None
        self.sat_list = []
        self.signal_mask = None
        self.signal_list = []
        self.num_cell = None
        self.cell_mask = None
        self.observations = []

        self.parse_msg()
        self.parse_signal_data()

    def parse_msg(self):
        #print(f'msg type is {self.msg_type}')

        # 12 bits - reference station ID
        self.reference_station_ID = 0
        for b in range(12):
            self.reference_station_ID = (self.reference_station_ID << 1) + self.data.pop(0)
        #print(f'station is {self.reference_station_ID}')

        # 30 bits gnss epoch time
        self.gnss_epoch_time = 0
        for b in range(30):
            self.gnss_epoch_time = (self.gnss_epoch_time << 1) + self.data.pop(0)
        if str(self.msg_type)[2] == '8':
            ##  GLOnass time
            self.glo_dow = self.gnss_epoch_time >> 27
            self.glo_epoch_time = self.gnss_epoch_time & 0x7ffffff


        # 1 bit multiple message bit
        self.multiple_message_bit = self.data.pop(0)

        # 3 bits IODS
        self.iods = 0
        for b in range(3):
            self.iods = (self.iods << 1) + self.data.pop(0)

        # 7 bits reserved
        self.reserved1 = 0
        for b in range(7):
            self.reserved1 = (self.reserved1 << 1) + self.data.pop(0)
        
        # 2 bits clock steering
        self.clock_steering = 0
        for b in range(2):
            self.clock_steering = (self.clock_steering << 1) + self.data.pop(0)
        

        # 2 bit external clock
        self.ext_clock = 0
        for b in range(2):
            self.ext_clock = (self.ext_clock << 1) + self.data.pop(0)

        # 1 bit smooting
        self.smoothing = self.data.pop(0)

        # 3 bits smooting interval
        self.smoothing_int = 0
        for b in range(3):
            self.smoothing_int = (self.smoothing_int << 1) + self.data.pop(0)

        
        # 64 bit satellite mask
        self.nsat = 0
        self.sat_mask = 0
        for b in range(64):
            bit = self.data.pop(0)
            self.sat_mask = (self.sat_mask << 1) + bit
            if bit > 0:
                self.nsat = self.nsat + 1
                self.sat_list.append(b+1)

        # 32 bit signal mask
        self.nsig = 0
        self.signal_mask = 0
        for b in range(32):
            bit = self.data.pop(0)
            self.signal_mask = (self.signal_mask << 1) + bit
            if bit > 0:
                self.nsig = self.nsig + 1
                self.signal_list.append(b+1)

        # nsat*nsig bits for cell mask
        self.cell_mask = 0
        self.num_cell = 0
        for b in range(self.nsat * self.nsig):
            bit = self.data.pop(0)
            self.cell_mask = (self.cell_mask << 1) + bit
            if bit > 0:
                self.num_cell = self.num_cell + 1

    def parse_signal_data(self):

        # list of MSMXSat objects, one per satellite
        sat_info_list = []

        for sat in self.sat_list:
            if str(self.msg_type)[3] == '4':
                # MSM4
                sat_info_list.append(MSM4Sat(self.data))
            elif str(self.msg_type)[3] == '5':
                # MSM5
                sat_info_list.append(MSM5Sat(self.data))

        # parse signal objects
        cell_mask_str =  format(self.cell_mask,f'0>{self.nsat*self.nsig}b')
        for nsat in range(self.nsat):
            sigmask = cell_mask_str[ nsat*self.nsig : nsat*self.nsig+self.nsig ]
            for nsig in range(self.nsig):
                if sigmask[nsig] == '1':
                    if str(self.msg_type)[3] == '4':
                        # MSM4
                        signal = MSM4Signal(self.data)
                        pseudorange = sat_info_list[nsat].rough_int_millisec + sat_info_list[nsat].rough_mod_millisec * 2.0**-10 + signal.pseudorange_fine * 2.0**-24
                        extended_info = sat_info_list[nsat].extended_info
                        phaserange = signal.phase_fine * 2.0**-29
                        lock_time = signal.phase_locktime
                        half_cycle_amb = signal.half_cycle_amb
                        cn0 = signal.cn0
                        doppler = None

                    elif str(self.msg_type)[3] == '5':
                        # MSM5
                        signal = MSM5Signal(self.data)
                        pseudorange = sat_info_list[nsat].rough_int_millisec + sat_info_list[nsat].rough_mod_millisec * 2.0**-10 + signal.pseudorange_fine * 2.0**-24
                        extended_info = sat_info_list[nsat].extended_info
                        phaserange = signal.phase_fine * 2.0**-29
                        lock_time = signal.phase_locktime
                        half_cycle_amb = signal.half_cycle_amb
                        cn0 = signal.cn0
                        doppler = signal.phase_range_rate
                    
                    self.observations.append(Observation(self.sat_list[nsat], self.signal_list[nsig], pseudorange, extended_info, phaserange, lock_time, half_cycle_amb, cn0, doppler))
        
    # def next_bits(self, bits):
    #     word = 0
    #     for b in range(bits):
    #         word = (word << 1) + self.data.pop(0)
    #     return word

class MSM4Sat():
    def __init__(self, data):
        self.data = data

        self.rough_int_millisec = None
        self.rough_mod_millisec = None

        self.parse_msg()

    def parse_msg(self):
        self.rough_int_millisec = next_bits(self.data, 8)
        self.rough_mod_millisec = next_bits(self.data, 10)
    

class MSM5Sat():
    def __init__(self, data):
        self.data = data

        self.rough_int_millisec = None
        self.extended_info = None
        self.rough_mod_millisec = None
        self.rough_phaserange = None

        self.parse_msg()

    def parse_msg(self):
        self.rough_int_millisec = next_bits(self.data,8)
        self.extended_info = next_bits(self.data,4)
        self.rough_mod_millisec = next_bits(self.data,10)
        self.rough_phaserange = next_bits(self.data,14)
    pass

class MSM4Signal():
    def __init__(self, data):
        self.data = data
        
        self.pseudorange_fine = None
        self.phase_fine = None
        self.phase_locktime = None
        self.half_cycle_amb = None
        self.cn0 = None


        self.parse_msg()

    def parse_msg(self):
        self.pseudorange_fine = next_bits(self.data,15)
        self.phase_fine = next_bits(self.data,22)
        self.phase_locktime = next_bits(self.data,4)
        self.half_cycle_amb = next_bits(self.data,1)
        self.cn0 = next_bits(self.data,6)
        pass
    pass

class MSM5Signal():
    def __init__(self, data):
        self.data = data
        
        self.pseudorange_fine = None
        self.phase_fine = None
        self.phase_locktime = None
        self.half_cycle_amb = None
        self.cn0 = None
        self.phase_range_rate = None
        
        self.parse_msg()

    def parse_msg(self):
        self.pseudorange_fine = next_bits(self.data,15)
        self.phase_fine = next_bits(self.data,22)
        self.phase_locktime = next_bits(self.data,4)
        self.half_cycle_amb = next_bits(self.data,1)
        self.cn0 = next_bits(self.data,6)
        self.phase_range_rate = next_bits(self.data,15)
    pass

class Observation():
    def __init__(self, sat_id, sig_id, pseudorange, extended_info, phaserange, lock_time, half_cycle_amb, cn0, doppler):
        self.sat_id = sat_id
        self.sig_id = sig_id

        self.pseudorange = pseudorange
        self.extended_info = extended_info
        self.phaserange = phaserange
        self.lock_time = lock_time
        self.half_cycle_amb = half_cycle_amb
        self.cn0  = cn0
        self.doppler = doppler