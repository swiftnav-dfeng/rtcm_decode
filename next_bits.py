# data = array of bits
# bits = number of bits
def next_bits(data, bits):
    word = 0
    for b in range(bits):
        word = (word << 1) + data.pop(0)
    return word