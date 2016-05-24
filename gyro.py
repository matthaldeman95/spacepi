import smbus

def int_sw_swap(x):
    xl = x & 0xff
    xh = x >> 8
    xx = (xl << 8) + xh
    return xx - 0xffff if xx > 0x7fff else xx

class itg3200(object):
    def __init__(self, bus_nr, addr, lpf, div):
        self.bus = smbus.SMBus(bus_nr)
        self.addr = addr
        self.bus.write_byte_data(self.addr, 0x15, div-1)
        self.bus.write_byte_data(self.addr, 0x16, 0x18 | lpf)

    def read_data(self):
        gx = int_sw_swap(self.bus.read_word_data(self.addr, 0x1d))
        gy = int_sw_swap(self.bus.read_word_data(self.addr, 0x1f))
        gz = int_sw_swap(self.bus.read_word_data(self.addr, 0x21))
        return (gx, gy, gz)

if __name__ == '__main__':
	import sys
	import datetime
	samples = 10000
	sensor = itg3200(1, 0x69, 0, 0)
	starttime = datetime.datetime.now()
	for n in range (0, samples):
		gx, gy, gz = sensor.read_data()
    		#print gx, gy, gz
	endtime = datetime.datetime.now()
	td = (endtime-starttime).total_seconds()
	print samples/td

