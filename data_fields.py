from bitarray import bitarray
from data_types import *


class DataField:
    length = None
    name = None
    unit = None
    def __init__(self, bits: bitarray):
        pass

class GNSSEpochTime():
    length = 30
    name = "GNSS Epoch Time"
    def __init__(self, bits: bitarray):
        super().__init__(bits)

        df = RTCMUint(self.length, bits)
        self.value = df.value

# Reserved
class DF001(DataField):
    length = 1
    name = "Reserved"

    def __init__(self, bits: bitarray):
        super().__init__(bits)

        df = RTCMBit(self.length, bits)
        self.value = df.value

# Message Number
class DF002(DataField):
    length = 12
    name = "Message Number"
    def __init__(self, bits: bitarray):
        super().__init__(bits)

        df = RTCMUint(self.length, bits)
        self.value = df.value

# Reference Station ID
class DF003(DataField):
    length = 12
    name = "Reference Station ID"

    def __init__(self, bits: bitarray):
        super().__init__(bits)

        df = RTCMUint(self.length, bits)
        self.value = df.value

# Reserved for ITRF Realization Year
class DF021(DataField):
    length = 6
    name = "Reserved for ITRF Realization Year"
    def __init__(self, bits: bitarray):
        super().__init__(bits)

        df = RTCMUint(self.length, bits)
        self.value = df.value

# GPS Indicator
class DF022(DataField):
    length = 1
    name = "GPS Indicator"

    def __init__(self, bits: bitarray):
        super().__init__(bits)

        df = RTCMBit(self.length, bits)
        self.value = df.value

# GLONASS Indicator
class DF023(DataField):
    length = 1
    name = "GLONASS Indicator"

    def __init__(self, bits: bitarray):
        super().__init__(bits)

        df = RTCMBit(self.length, bits)
        self.value = df.value

# Reserved for Galileo Indicator
class DF024(DataField):
    length = 1
    name = "Reserved for Galileo Indicator"

    def __init__(self, bits: bitarray):
        super().__init__(bits)

        df = RTCMBit(self.length, bits)
        self.value = df.value

# Antenna reference point ECEF-X
class DF025(DataField):
    length = 38
    name = "Antenna Reference Point ECEF-X"
    unit = "meters"

    def __init__(self, bits: bitarray):
        super().__init__(bits)

        
        df = RTCMInt(self.length, bits)
        self.value = df.value * 0.0001

# Antenna reference point ECEF-Y
class DF026(DataField):
    length = 38
    name = "Antenna Reference Point ECEF-Y"
    unit = "meters"

    def __init__(self, bits: bitarray):
        super().__init__(bits)

        
        df = RTCMInt(self.length, bits)
        self.value = df.value * 0.0001

# Antenna reference point ECEF-Z
class DF027(DataField):
    length = 38
    name = "Antenna Reference Point ECEF-Z"
    unit = "meters"
    def __init__(self, bits: bitarray):
        super().__init__(bits)

        
        df = RTCMInt(self.length, bits)
        self.value = df.value * 0.0001

# Reference Station Indicator
class DF141(DataField):
    length = 1
    name = "Reference Station Indicator"
    def __init__(self, bits: bitarray):
        super().__init__(bits)

        df = RTCMBit(self.length, bits)
        self.value = df.value

# Single Receiver Oscillator Indicator
class DF142(DataField):
    length = 1
    name = "Single Receiver Oscillator Indicator"
    def __init__(self, bits: bitarray):
        super().__init__(bits)

        df = RTCMBit(self.length, bits)
        self.value = df.value

# Quarter Cycle Indicator
class DF364(DataField):
    length = 2
    name = "Quarter Cycle Indicator"

    def __init__(self, bits: bitarray):
        super().__init__(bits)
        
        df = RTCMBit(self.length, bits)
        self.value = df.value


class DF393(DataField):
    length = 1
    name = "Multiple Message Bit"

    def __init__(self, bits: bitarray):
        super().__init__(bits)
        
        df = RTCMBit(self.length, bits)
        self.value = df.value

class DF394(DataField):
    length = 64
    name = "Satellite Mask"

    def __init__(self, bits: bitarray):
        super().__init__(bits)
        
        df = RTCMBit(self.length, bits)
        self.value = df.value
        self.nsat = self.value.count(value=1)

class DF395(DataField):
    length = 32
    name = "Signal Mask"

    def __init__(self, bits: bitarray):
        super().__init__(bits)
        
        df = RTCMBit(self.length, bits)
        self.value = df.value
        self.nsig = self.value.count(value=1)

class DF396(DataField):
    name = "Cell Mask"

    def __init__(self, bits: bitarray, length:int):
        super().__init__(bits)
        
        # length will be nsat * nsig
        self.length = length
        df = RTCMBit(self.length, bits)
        self.value = df.value

class DF409(DataField):
    length = 3
    name = "IODS"
    def __init__(self, bits: bitarray):
        super().__init__(bits)

        df = RTCMUint(self.length, bits)
        self.value = df.value

class DF411(DataField):
    length = 2
    name = "Clock Steering Indicator"
    def __init__(self, bits: bitarray):
        super().__init__(bits)

        df = RTCMUint(self.length, bits)
        self.value = df.value

class DF412(DataField):
    length = 2
    name = "External Clock Indicator"
    def __init__(self, bits: bitarray):
        super().__init__(bits)

        df = RTCMUint(self.length, bits)
        self.value = df.value

class DF417(DataField):
    length = 1
    name = "GNSS Divergence-free Smoothing Indicator"

    def __init__(self, bits: bitarray):
        super().__init__(bits)
        
        df = RTCMBit(self.length, bits)
        self.value = df.value

class DF418(DataField):
    length = 3
    name = "GNSS Smoothing Interval"

    def __init__(self, bits: bitarray):
        super().__init__(bits)
        
        df = RTCMBit(self.length, bits)
        self.value = df.value

