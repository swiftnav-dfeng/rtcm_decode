# BDS ephemeris data

class RTCM1042():
    def __init__(self, msg_type, data) -> None:
        self.msg_type = msg_type
        self.data = data
        
        self.sat_id = None
        self.week = None
        self.urai = None
        self.idot = None
        self.aode = None
        self.toc = None
        self.a2 = None
        self.a1 = None
        self.a0 = None
        self.aodc = None
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
        self.omega_dot = None
        self.tgd1 = None
        self.tgd2 = None
        self.health = None

        
        #self.parse_msg()

    def next_bits(self, bits):
        word = 0
        for b in range(bits):
            word = (word << 1) + self.data.pop(0)
        return word

    def parse_msg(self):

        self.sat_id = self.next_bits(6)
        self.week = self.next_bits(13)

        self.urai = self.next_bits(4)

        self.idot = self.next_bits(14)

        self.aode = self.next_bits(5)

        self.toc = self.next_bits(17)

        self.a2 = self.next_bits(11)

        self.a1 = self.next_bits(22)

        self.a0 = self.next_bits(24)

        self.aodc = self.next_bits(5)

        self.crs = self.next_bits(18)

        self.delta_n = self.next_bits(16)

        self.m0 = self.next_bits(32)

        self.cuc = self.next_bits(18)

        self.e = self.next_bits(32)

        self.cus = self.next_bits(18)

        self.a_12 = self.next_bits(32)

        self.toe = self.next_bits(17)

        self.cic = self.next_bits(18)

        self.omega0 = self.next_bits(32)

        self.cis = self.next_bits(18)

        self.i0 = self.next_bits(32)

        self.crc = self.next_bits(18)

        self.omega = self.next_bits(32)

        self.omega_dot = self.next_bits(24)

        self.tgd1 = self.next_bits(10)

        self.tgd2 = self.next_bits(10)

        self.health = self.next_bits(1)
