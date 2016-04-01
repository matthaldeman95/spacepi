import spidev
import datetime
import sys
import gyro

sensor = gyro.itg3200(1, 0x69, 0, 0)
spi = spidev.SpiDev()
spi.open(0,0);
spi.max_speed_hz = 32000000

def buildReadCommand(channel):
        startBit = 0x01
        singleEnded = 0x08
        return [startBit, singleEnded|(channel<<4),0]

def processAdcValue(result):
        byte2 = (result[1] & 0x03)
        return (byte2 << 8 | result[2])

def readAdc(channel):
        if ((channel > 7) or (channel < 0)):
                return -1
        r = spi.xfer2(buildReadCommand(channel))
        return processAdcValue(r)

if __name__ == '__main__':
        try:
                samples = 1000
                starttime = datetime.datetime.now()
                for n in range(0,samples):
                        val0, val1, val2, val3  = readAdc(0), readAdc(1), readAdc(2), readAdc(3)
                        #print val0, val1, val2, val3
                        gx, gy, gz = sensor.read_data()
                        n = n+1
                endtime = datetime.datetime.now()
                print samples, starttime, endtime
        except KeyboardInterrupt:
                spi.close()
                sys.exit(0)
