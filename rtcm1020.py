# GLO ephemeris data

class RTCM1020():
    def __init__(self, msg_type, data) -> None:
        self.msg_type = msg_type
        self.data = data
        
        self.sat_id = None
        self.fcn = None
        self.alm_health = None
        self.alm_health_avail = None
        self.p1 = None
        self.tk = None
        self.msb_bn = None
        self.p2 = None
        self.tb = None
        self.xn_tb_1st = None
        self.xn_tb = None
        self.xn_tb_2nd = None
        self.yn_tb_1st = None
        self.yn_tb = None
        self.yn_tb_2nd = None
        self.zn_tb_1st = None
        self.zn_tb = None
        self.an_tb_2nd = None
        self.p3 = None
        self.gamma_tb = None
        self.m_p = None
        self.m_ln_3rd = None
        self.tau_n_tb = None
        self.delta_tau_n = None
        self.en = None
        self.m_p4 = None
        self.m_ft = None
        self.m_nt = None
        self.m_m = None
        self.additional_data = None
        self.n_a = None
        self.tau_c = None
        self.m_n4 = None
        self.tau_gps = None
        self.m_ln_5th = None
        self.reserved1 = None

        
        #self.parse_msg()

    def parse_msg(self):

        self.sat_id = 0
        for b in range(6):
            self.sat_id = (self.sat_id << 1) + self.data.pop(0)

        self.fcn = 0
        for b in range(5):
            self.fcn = (self.fcn << 1) + self.data.pop(0)

        self.alm_health = 0
        for b in range(1):
            self.alm_health = (self.alm_health << 1) + self.data.pop(0)

        self.alm_health_avail = 0
        for b in range(1):
            self.alm_health_avail = (self.alm_health_avail << 1) + self.data.pop(0)

        self.p1 = 0
        for b in range(2):
            self.p1 = (self.p1 << 1) + self.data.pop(0)

        self.tk = 0
        for b in range(12):
            self.tk = (self.tk << 1) + self.data.pop(0)

        self.msb_bn = 0
        for b in range(1):
            self.msb_bn = (self.msb_bn << 1) + self.data.pop(0)

        self.p2 = 0
        for b in range(1):
            self.p2 = (self.p2 << 1) + self.data.pop(0)

        self.tb = 0
        for b in range(7):
            self.tb = (self.tb << 1) + self.data.pop(0)

        self.xn_tb_1st = 0
        for b in range(24):
            self.xn_tb_1st = (self.xn_tb_1st << 1) + self.data.pop(0)

        self.xn_tb = 0
        for b in range(27):
            self.xn_tb = (self.xn_tb << 1) + self.data.pop(0)

        self.xn_tb_2nd = 0
        for b in range(5):
            self.xn_tb_2nd = (self.xn_tb_2nd << 1) + self.data.pop(0)

        self.yn_tb_1st = 0
        for b in range(24):
            self.yn_tb_1st = (self.yn_tb_1st << 1) + self.data.pop(0)

        self.yn_tb = 0
        for b in range(27):
            self.yn_tb = (self.yn_tb << 1) + self.data.pop(0)

        self.yn_tb_2nd = 0
        for b in range(5):
            self.yn_tb_2nd = (self.yn_tb_2nd << 1) + self.data.pop(0)

        self.zn_tb_1st = 0
        for b in range(24):
            self.zn_tb_1st = (self.zn_tb_1st << 1) + self.data.pop(0)

        self.zn_tb = 0
        for b in range(27):
            self.zn_tb = (self.zn_tb << 1) + self.data.pop(0)

        self.an_tb_2nd = 0
        for b in range(5):
            self.an_tb_2nd = (self.an_tb_2nd << 1) + self.data.pop(0)

        self.p3 = 0
        for b in range(1):
            self.p3 = (self.p3 << 1) + self.data.pop(0)

        self.gamma_tb = 0
        for b in range(11):
            self.gamma_tb = (self.gamma_tb << 1) + self.data.pop(0)

        self.m_p = 0
        for b in range(2):
            self.m_p = (self.m_p << 1) + self.data.pop(0)

        self.m_ln_3rd = 0
        for b in range(1):
            self.m_ln_3rd = (self.m_ln_3rd << 1) + self.data.pop(0)

        self.tau_n_tb = 0
        for b in range(22):
            self.tau_n_tb = (self.tau_n_tb << 1) + self.data.pop(0)

        self.delta_tau_n = 0
        for b in range(5):
            self.delta_tau_n = (self.delta_tau_n << 1) + self.data.pop(0)

        self.en = 0
        for b in range(5):
            self.en = (self.en << 1) + self.data.pop(0)

        self.m_p4 = 0
        for b in range(1):
            self.m_p4 = (self.m_p4 << 1) + self.data.pop(0)

        self.m_ft = 0
        for b in range(4):
            self.m_ft = (self.m_ft << 1) + self.data.pop(0)

        self.m_nt = 0
        for b in range(11):
            self.m_nt = (self.m_nt << 1) + self.data.pop(0)

        self.m_m = 0
        for b in range(2):
            self.m_m = (self.m_m << 1) + self.data.pop(0)

        self.additional_data = 0
        for b in range(1):
            self.additional_data = (self.additional_data << 1) + self.data.pop(0)

        self.n_a = 0
        for b in range(11):
            self.n_a = (self.n_a << 1) + self.data.pop(0)

        self.tau_c = 0
        for b in range(32):
            self.tau_c = (self.tau_c << 1) + self.data.pop(0)

        self.m_n4 = 0
        for b in range(5):
            self.m_n4 = (self.m_n4 << 1) + self.data.pop(0)

        self.tau_gps = 0
        for b in range(22):
            self.tau_gps = (self.tau_gps << 1) + self.data.pop(0)

        self.m_ln_5th = 0
        for b in range(1):
            self.m_ln_5th = (self.m_ln_5th << 1) + self.data.pop(0)

        self.reserved1 = 0
        for b in range(7):
            self.reserved1 = (self.reserved1 << 1) + self.data.pop(0)
