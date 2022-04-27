# GPS ephemeris data

class RTCM1019():
    def __init__(self, msg_type, data) -> None:
        self.msg_type = msg_type
        self.data = data
        
        self.sat_id = None
        self.week = None
        self.sv_accuracy = None
        self.code_on_l2 = None
        self.idot = None
        self.iode = None
        self.toc = None
        self.af2 = None
        self.af1 = None
        self.af0 = None
        self.iodc = None
        self.crs = None
        self.delta_n = None
        self.m0 = None
        self.cuc = None
        self.eccen = None
        self.cus = None
        self.a_12 = None
        self.toe = None
        self.cic = None
        self.omega0 = None
        self.cis = None
        self.i0 = None
        self.crc = None
        self.perigee = None
        self.omega_dot = None
        self.tgd = None
        self.sv_health = None
        self.l2p_flag = None
        self.fit_int = None
        
        self.parse_msg()

    def parse_msg(self):

        self.sat_id = 0
        for b in range(6):
            self.sat_id = (self.sat_id << 1) + self.data.pop(0)


        self.week = 0
        for b in range(10):
            self.week = (self.week << 1) + self.data.pop(0)

        self.sv_accuracy = 0
        for b in range(4):
            self.sv_accuracy = (self.sv_accuracy << 1) + self.data.pop(0)

        self.code_on_l2 = 0
        for b in range(2):
            self.code_on_l2 = (self.code_on_l2 << 1) + self.data.pop(0)

        self.idot = 0
        for b in range(14):
            self.idot = (self.idot << 1) + self.data.pop(0)


        self.iode = 0
        for b in range(8):
            self.iode = (self.iode << 1) + self.data.pop(0)

        self.toc = 0
        for b in range(16):
            self.toc = (self.toc << 1) + self.data.pop(0)

        self.af2 = 0
        for b in range(8):
            self.af2 = (self.af2 << 1) + self.data.pop(0)

        self.af1 = 0
        for b in range(16):
            self.af1 = (self.af1 << 1) + self.data.pop(0)

        self.af0 = 0
        for b in range(22):
            self.af0 = (self.af0 << 1) + self.data.pop(0)

        self.iodc = 0
        for b in range(10):
            self.iodc = (self.iodc << 1) + self.data.pop(0)

        self.crs = 0
        for b in range(16):
            self.crs = (self.crs << 1) + self.data.pop(0)

        self.delta_n = 0
        for b in range(16):
            self.delta_n = (self.delta_n << 1) + self.data.pop(0)

        self.m0 = 0
        for b in range(32):
            self.m0 = (self.m0 << 1) + self.data.pop(0)

        self.cuc = 0
        for b in range(16):
            self.cuc = (self.cuc << 1) + self.data.pop(0)

        self.eccen = 0
        for b in range(32):
            self.eccen = (self.eccen << 1) + self.data.pop(0)

        self.cus = 0
        for b in range(16):
            self.cus = (self.cus << 1) + self.data.pop(0)

        self.a_12 = 0
        for b in range(32):
            self.a_12 = (self.a_12 << 1) + self.data.pop(0)

        self.toe = 0
        for b in range(16):
            self.toe = (self.toe << 1) + self.data.pop(0)

        self.cic = 0
        for b in range(16):
            self.cic = (self.cic << 1) + self.data.pop(0)

        self.omega0 = 0
        for b in range(32):
            self.omega0 = (self.omega0 << 1) + self.data.pop(0)

        self.cis = 0
        for b in range(16):
            self.cis = (self.cis << 1) + self.data.pop(0)

        self.i0 = 0
        for b in range(32):
            self.i0 = (self.i0 << 1) + self.data.pop(0)

        self.crc = 0
        for b in range(16):
            self.crc = (self.crc << 1) + self.data.pop(0)

        self.perigee = 0
        for b in range(32):
            self.perigee = (self.perigee << 1) + self.data.pop(0)

        self.omega_dot = 0
        for b in range(24):
            self.omega_dot = (self.omega_dot << 1) + self.data.pop(0)

        self.tgd = 0
        for b in range(8):
            self.tgd = (self.tgd << 1) + self.data.pop(0)

        self.sv_health = 0
        for b in range(6):
            self.sv_health = (self.sv_health << 1) + self.data.pop(0)

        self.l2p_flag = 0
        for b in range(1):
            self.l2p_flag = (self.l2p_flag << 1) + self.data.pop(0)

        self.fit_int = 0
        for b in range(1):
            self.fit_int = (self.fit_int << 1) + self.data.pop(0)