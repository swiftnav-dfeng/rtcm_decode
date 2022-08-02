from handler import Handler
from crc import Configuration
from rtcm import CRCQ24, RTCM1005, RTCMMsg, rtcm_lookup

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

def process_frame(msg: RTCMMsg):
    print(msg.msg_type)

def main():
    with open('data/d1_30s.rtcm', 'rb') as f:
        h = Handler(f, process_frame)
        h.process()

    crcq24 = CRCQ24()
    r = RTCMMsg(sample_msg, crcq24)
    print(r.checksum_passed())
    for field in r.body_obj.body_data:
        print(f'{field.name} {field.value} {field.unit}')

if __name__ == "__main__":
    main()