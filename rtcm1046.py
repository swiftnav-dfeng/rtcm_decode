# GAL ephemeris data
# RTCM 10403.3 Table 3.5-111

class RTCM1046():
    def __init__(self, msg_type, data) -> None:
        self.msg_type = msg_type
        self.data = data
        
        self.sat_id = None
        self.week = None
        self.iodnav = None
        self.sisa_index_e1e5b = None
        self.idot = None
        self.toc = None
        self.af2 = None
        self.af1 = None
        self.af0 = None
        self.crs = None
        self.delta_n = None
        self.m0 = None
        self.cuc = None
        self.e = None
        self.cus = None
        self.a_12 = None
        self.toe = None
        self.cic = None
        self.omega0 = None
        self.cis = None
        self.i0 = None
        self.crc = None
        self.omega = None
        self.omegadot = None
        self.bgd_e5ae1 = None
        self.bgd_e5be1 = None
        self.e5b_health = None
        self.e5b_data_valid = None
        self.e1b_health = None
        self.e1b_data_valid = None
        self.reserved1 = None
        
        #self.parse_msg()

    def next_bits(self, bits):
        word = 0
        for b in range(bits):
            word = (word << 1) + self.data.pop(0)
        return word

    def parse_msg(self):

        self.sat_id = self.next_bits(6)
        self.week = self.next_bits(12)
        self.iodnav = self.next_bits(10)
        self.sisa_index_e1e5b = self.next_bits(8)
        self.idot = self.next_bits(14)
        self.toc = self.next_bits(14)
        self.af2 = self.next_bits(6)
        self.af1 = self.next_bits(21)
        self.af0 = self.next_bits(31)
        self.crs = self.next_bits(16)
        self.delta_n = self.next_bits(16)
        self.m0 = self.next_bits(32)
        self.cuc = self.next_bits(16)
        self.e = self.next_bits(32)
        self.cus = self.next_bits(16)
        self.a_12 = self.next_bits(32)
        self.toe = self.next_bits(14)
        self.cic = self.next_bits(16)
        self.omega0 = self.next_bits(32)
        self.cis = self.next_bits(16)
        self.i0 = self.next_bits(32)
        self.crc = self.next_bits(16)
        self.omega = self.next_bits(32)
        self.omegadot = self.next_bits(24)
        self.bgd_e5ae1 = self.next_bits(10)
        self.bgd_e5be1 = self.next_bits(10)
        self.e5b_health = self.next_bits(2)
        self.e5b_data_valid = self.next_bits(1)
        self.e1b_health = self.next_bits(2)
        self.e1b_data_valid = self.next_bits(1)
        self.reserved1 = self.next_bits(2)

