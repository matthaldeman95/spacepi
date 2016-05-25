from datetime import datetime
import sys
import gyro
import time
import math as m
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

sensor = gyro.itg3200(1, 0x69, 0, 0)        # Initialize gyroscope
SPI_PORT = 0                              # Initialize hardware SPI comm
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

"""
USER INPUTS
"""

sleeptime = 5                               # Time to wait at start of flight before sampling gyroscope
                                            # to check for spin-up

gyrothreshold = 200                         # Z-axis gyro value that must be reached to indicate spin-up
                                            # Should be around 3 Hz for launch

totalrecordtime = 30                        # Duration to record data after spin up begins







"""FUNCTIONS"""




""" CHECKS WHETHER ABSOLUTE VALUE OF VERTICAL AXIS ROTATION IS HIGH ENOUGH TO INDICATE
    ROCKET'S SPIN-UP, WHERE DATA COLLECTION WILL BEGIN """

def checkgyro(gyrothreshold):
    gx, gy, gz = sensor.read_data()                 # Read all three axes of data
    print "Checking gyro threshold:", gx, gy, gz
    while m.fabs(gz) < gyrothreshold:               # If absolute value of z-axis rate is lower than threshold,
        time.sleep(3)                               # wait three seconds, then read and check again
        gx, gy, gz = sensor.read_data()
	    print "Checking gyro threshold:", gx, gy, gz
    time.sleep(3)                                   # When threshold is exceeded, wait three seconds,
    gx, gy, gz = sensor.read_data()                 # then check again
    if m.fabs(gz) < gyrothreshold:                  # If threshold is not reached again, start the entire
        checkgyro(gyrothreshold)                    # threshold routine over again
    else: return                                    # If threshold is continuously exceeded, move on to data collection

""" COLLECTIONS TIME, ADC, AND GYROSCOPE DATA.  STORES DATA IN LISTS UNTIL 10000 SAMPLES COLLECTED,
    THEN STOPS COLLECTING AND DUMPS ALL DATA INTO DATA FILE"""


def datawrite(outfile):
    print "Recording data now"
    t, gx, gy, gz = [], [], [], []                  # Empty lists for all data
    val0, val1, val2, val3 = [], [], [], []
    starttime = datetime.now()                      # Record start time for collection of 10000 samples
    for n in range(0, samples):                     # For total number of samples,
        t.append(datetime.now().time())             # Append current time to time lists
        val0.append(mcp.read_adc(0))                # Read 4 channels of ADC data
        val1.append(mcp.read_adc(1))
        val2.append(mcp.read_adc(2))
        val3.append(mcp.read_adc(3))
        if n % 100 == 0:                                     # Gyroscope data only collected on certain iterations
            gxval, gyval, gzval = sensor.read_data()
        gx.append(gxval)
        gy.append(gyval)
        gz.append(gzval)
    endtime = datetime.now()                                # Record end time for rate calculation
    td = (endtime - starttime).total_seconds()                      # Total record time in seconds for 10000 samples
    for m in range(0, len(val0)):
        outfile.write('%s, %d, %d, %d, %d, %f, %f, %f \n' % (t[m], val0[m], val1[m], val2[m], val3[m], gx[m], gy[m], gz[m]))
                                                            # Dumps all data into CSV output file
    print "10000 samples recorded at ", samples/td, " Hz \n"        # Prints data rate
    outfile.write('\n 1000 samples recorded at %f Hz' %td)          # Writes data rate to file for checking later
    outfile.write('\n \n \n \n \n')





"""FLIGHT ROUTINE"""



print "Sleeping..."
time.sleep(sleeptime)                                               # Wait until a certain point in flight to begin checking gyro

outfile = open('testdata.csv', 'w')                                 # Open data file, write column headers
outfile.write('time, adc1, adc2, adc3, adc4, gx, gy, gz \n')

checkgyro(gyrothreshold)                                            # Check gyroscope threshold, continue only when exceeded
print "Gyro requirement satisfied"

starttime = datetime.now()                                          # Start time for controlling how long data is recorded for
elaptime = (datetime.now() - starttime).total_seconds()             # Elapsed time since data collection began

while elaptime < totalrecordtime:                                   # If elapsed time has not exceeded total data collection time,
    datawrite(outfile)                                              # Call data record function to take 10000 samples
    print "Data record complete"
    time.sleep(3)                                                   # Sleep for a few seconds
    elaptime = (datetime.now() - starttime).total_seconds()         # Take elapsed time again

outfile.close()                                                     # Close output data file

sys.exit()                                                          # Close Python

os.system("sudo shutdown -h now")                                   # Shutdown the Raspberry Pi
