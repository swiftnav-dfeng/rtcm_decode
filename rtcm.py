import rtcm_decode.rtcm1019 as rtcm1019
import rtcm_decode.rtcm1020 as rtcm1020
import rtcm_decode.rtcm1046 as rtcm1046
import rtcm_decode.rtcm1042 as rtcm1042
from rtcm_decode.rtcmmsm import MSMMsg

msm5_ids = [1075, 1085, 1095, 1105, 1115, 1125]
msm4_ids = [1074, 1084, 1094, 1104, 1114, 1124]

# data is byte array
def create_bitarray(data):
    bit_array = []
    for b in data:
        bit_array.append(b >> 7)
        bit_array.append((b & 0b01000000)>> 6)
        bit_array.append((b & 0b00100000)>> 5)
        bit_array.append((b & 0b00010000)>> 4)
        bit_array.append((b & 0b00001000)>> 3)
        bit_array.append((b & 0b00000100)>> 2)
        bit_array.append((b & 0b00000010)>> 1)
        bit_array.append(b & 0b00000001)
    return bit_array

class RTCMDecode():
    def __init__(self, handle, callback):
        self.handle = handle
        self.key = self.create_crc_key('1100001100100110011111011')
        self.crc_pass = None
        self.msg_length = None
        self.msg_type = None
        self.msg_array = []
        self.msg_found_callback = callback
        self.parse_data()
        
    def create_crc_key(self, poly):
        # CRC qualcomm 24
        #key = 0b100101011101110001000001
        key_array = []

        for bit in poly:
            if bit == '1':
                key_array.append(1)
            else:
                key_array.append(0)

        return key_array

    def check_crc(self, data, key):
        remainder = data.copy()
        for j in range(len(data) - (len(key)-1)):
            if remainder.pop(0) == 1:
                for i in range(len(key)-1):
                    if key[i+1] != remainder[i]:
                        remainder[i] = 1
                    else:
                        remainder[i] = 0

        for i in remainder:
            if i != 0:
                return False
        
        return True


    def parse_data(self):
        while True:
            data = self.handle.read(1)

            if data == b'\xd3':  #preamble

                # obtain msg length
                data1 = self.handle.read(2)
                data1_int = int.from_bytes(data1, byteorder='big') # first 6 == zero, last ten bits = length of message
                if data1_int >> 10 != 0:
                    #invalid msg format
                    continue
                self.msg_length = data1_int & 0b11111111111
                
                data2 = self.handle.read(self.msg_length)
                if len(data2) < self.msg_length:
                    print("not enough bytes read")
                    break

                data_bit_array = create_bitarray(data2)
                
                crc = create_bitarray(self.handle.read(3))

                full_msg_bitarray = create_bitarray(data+data1)+data_bit_array+crc
                if self.check_crc(full_msg_bitarray, self.key):
                    self.crc_pass = True
                else:
                    self.crc_pass = False
                    continue

                #rtcm_msg = RTCMMsg(create_bitarray(data2))

                #data_bit_array = create_bitarray(data2)
                

                # 12bits - msg_type    
                self.msg_type = 0
                for b in range(12):
                    self.msg_type = (self.msg_type << 1) + data_bit_array.pop(0)
                
                # parse only msm5 obs messages below
                parsed_msg = None
                if self.msg_type in msm5_ids + msm4_ids:
                    parsed_msg = MSMMsg(self.msg_type, data_bit_array)
                elif self.msg_type == 1019:
                    parsed_msg = rtcm1019.RTCM1019(self.msg_type, data_bit_array)
                elif self.msg_type == 1020:
                    parsed_msg = rtcm1020.RTCM1020(self.msg_type, data_bit_array)
                elif self.msg_type == 1046:
                    parsed_msg = rtcm1046.RTCM1046(self.msg_type, data_bit_array)
                elif self.msg_type == 1042:
                    parsed_msg = rtcm1042.RTCM1042(self.msg_type, data_bit_array)

                self.msg_found_callback(RTCMMsg(self.msg_type, self.crc_pass, parsed_msg))
                
            elif data == b'':
                print("eof")
                break


class RTCMMsg():
    def __init__(self, msg_type, crc_pass, parsed):
        self.msg_type = msg_type
        self.crc_pass = crc_pass
        self.parsed = parsed





if __name__ == "__main__":
    with open('data/bd990_30s.rtcm', 'rb') as f:
        decoder = RTCMDecode(f)

    for msg in decoder.msg_array:
        print(msg.parsed.msg_type)
    