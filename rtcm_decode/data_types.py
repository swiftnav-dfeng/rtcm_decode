from bitarray import bitarray
from bitarray.util import ba2int
import logging

logger = logging.getLogger(__name__)

class RTCMDataType:
    def __init__(self, length:int, data:bitarray) -> None:
        self.length = length
        self.data = data
        self.value = self.get_value(data)

    def get_value(self, data):
        if len(data) != self.length:
            raise Exception(f'len of data is {len(data)}, should be {self.length}')
        
        return ba2int(data)

class RTCMBit(RTCMDataType):
    def __init__(self, length: int, data: bitarray) -> None:
        super().__init__(length, data)

    def get_value(self, data: bitarray) -> bitarray:
        if len(data) != self.length:
            raise Exception(f'len of data is {len(data)}, should be {self.length}')
        
        return data

class RTCMInt(RTCMDataType):
    def __init__(self, length: int, data: bitarray) -> None:
        super().__init__(length, data)

    def get_value(self, data):
        if len(data) != self.length:
            raise Exception(f'len of data is {len(data)}, should be {self.length}')

        return ba2int(data, signed=True)

class RTCMUint(RTCMDataType):
    def __init__(self, length: int, data: bitarray) -> None:
        super().__init__(length, data)

class RTCMSint(RTCMDataType):
    def __init__(self, length: int, data: bitarray) -> None:
        super().__init__(length, data)

    def get_value(self, data):
        if len(data) != self.length:
            raise Exception(f'len of data is {len(data)}, should be {self.length}')

        if data == bitarray('1' + '0'*(self.length-1)):
            # negative zero condition, should not be used
            return None
            
        if data[0] == 0:
            return ba2int(data[1:])
        else:
            return -1 * ba2int(data[1:])

