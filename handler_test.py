from handler import Handler
from crc import Configuration
from rtcm import RTCM1005, RTCMMsg

crc_configuration = Configuration(width=24, polynomial=0x1864CFB)

# from c10403.3 RTCM3 document, section 4.2
# msg 1005, ref sta id 2003, GPS service supported, but not GLO nor GAL
# arp ecef-x 1114104.5999, y -4850729.7108, z 3975521.4643
sample_msg = bytearray([
    0xd3,
    0x00,
    0x13,
    0x3e,
    0xd7,
    0xd3,
    0x02,
    0x02,
    0x98,
    0x0e,
    0xde,
    0xef,
    0x34,
    0xb4,
    0xbd,
    0x62,
    0xac,
    0x09,
    0x41,
    0x98,
    0x6f,
    0x33,
    0x36,
    0x0b,
    0x98
])

def process_frame(frame, crc_pass):
    msg = RTCMMsg(frame)
    print(f'{msg.msg_type} {crc_pass}')

def main():
    # with open('data/bd990_30s.rtcm', 'rb') as f:
    #     h = Handler(f, process_frame)
    #     h.process()

    # crc check
    crc = (sample_msg[-3] << 16) + (sample_msg[-2] << 8) + sample_msg[-1]
    print(Handler.check_frame(crc_configuration, crc, sample_msg[:-3]))

    r = RTCM1005(sample_msg)
    for field in r.obj_data:
        print(f'{field.name} {field.value} {field.unit}')

if __name__ == "__main__":
    main()