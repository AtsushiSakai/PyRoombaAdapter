def get_2_bytes(value):
    """ returns two bytes (ints) in high, low order
    whose bits form the input value when interpreted in
    two's complement
    """
    # if positive or zero, it's OK
    if value >= 0:
        eqBitVal = value
    # if it's negative, I think it is this
    else:
        eqBitVal = (1 << 16) + value

    return (eqBitVal >> 8) & 0xFF, eqBitVal & 0xFF
