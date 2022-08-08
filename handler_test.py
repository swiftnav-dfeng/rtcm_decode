from rtcm_decode.handler import Handler
from crc import Configuration
from rtcm_decode.rtcm import CRCQ24, RTCM1005, RTCMFrame, rtcm_lookup

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

def process_frame(frame: RTCMFrame):
    print(f'{frame.msg_type} {frame.checksum_passed()}')
    if frame.checksum_passed() is True:
        if (frame.msg_type in [1075, 1085, 1095, 1105, 1115, 1125, 1135]):
            for df in frame.msg.data_fields:
                print(f'{df.value} {df.name} {df.unit}')
            print(frame.msg.get_msg_dict())
            print(frame.msg.observations)
    else:
        print(frame.msg)
    pass

def main():
    with open('/Users/dfeng/dev/rtcm_decode/data/d1_30s.rtcm', 'rb') as f:
        h = Handler(f, process_frame)
        h.process()

    crcq24 = CRCQ24()
    r = RTCMFrame(sample_msg, crcq24)
    print(r.checksum_passed())
    for field in r.msg.data_fields:
        print(f'{field.name} {field.value} {field.unit}')

    print(r.msg.get_msg_dict())

if __name__ == "__main__":
    main()