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
        self.n_sat = None
        self.sat_mask = None
        self.nsig = None
        self.signal_mask = None
        self.cell_mask = None
        self.parse_msg()

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

        # 32 bit signal mask
        self.nsig = 0
        self.signal_mask = 0
        for b in range(32):
            bit = self.data.pop(0)
            self.signal_mask = (self.signal_mask << 1) + bit
            if bit > 0:
                self.nsig = self.nsig + 1

        # nsat*nsig bits for cell mask
        self.cell_mask = 0
        ncell = 0
        for b in range(self.nsat * self.nsig):
            bit = self.data.pop(0)
            self.cell_mask = (self.cell_mask << 1) + bit
            if bit > 0:
                ncell = ncell + 1