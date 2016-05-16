def buildReadCommand(channel):
    startBit = 0x01
    singleEnded = 0x08
    return [startBit, singleEnded | (channel << 4), 0]


def processAdcValue(result):
    byte2 = (result[1] & 0x03)
    return (byte2 << 8 | result[2])


def readAdc(channel):
    if ((channel > 7) or (channel < 0)):
        return -1
    r = spi.xfer2(buildReadCommand(channel))
    return processAdcValue(r)

