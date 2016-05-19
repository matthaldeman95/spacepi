# RockSat-C 2016
## Marshall University

Raspberry Pi payload that collects three axis gyroscope data and four channels of ADC data, with the ADC channels connected to op amps measuring the current output of solar panels.

Main data collection routine for flight is the `rsc16.py` file, which needs to be updated with correct timing parameters for flight.

Requires the `spilib.py` library, which defines basic SPI communication functions for the Pi to communicate with the MCP3008 ADC.

Requires the `gyro.py` library, which defines I2C communication functions for the ITG3200 gyroscope.

Please see `https://github.com/matthaldeman95/spacepi` for most recent version of code.