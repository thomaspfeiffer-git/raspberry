# -*- coding: utf-8 -*-
###############################################################################
# TSL2561.py                                                                  #
# under construction                                                          #
# TODO: try for i2c access                                                    #
###############################################################################


# Taken from and slightly modified:
# https://github.com/seanbechhofer/raspberrypi/blob/master/python/TSL2561.py


import sys
import time

sys.path.append('../libs')
from i2c import I2C


TSL2561_DELAY_INTTIME_13MS = 15
TSL2561_DELAY_INTTIME_101MS = 120
TSL2561_DELAY_INTTIME_402MS = 450

TSL2561_VISIBLE = 2         # channel 0 - channel 1
TSL2561_INFRARED = 1        # channel 1
TSL2561_FULLSPECTRUM = 0    # channel 0

# I2C address options
TSL2561_ADDR_LOW = 0x29
TSL2561_ADDR_FLOAT = 0x39   # Default address (pin left floating)
TSL2561_ADDR_HIGH = 0x49

TSL2561_COMMAND_BIT = 0x80    # Must be 1
TSL2561_CLEAR_BIT = 0x40      # Clears any pending interrupt (write 1 to clear)
TSL2561_WORD_BIT = 0x20       # 1 = read/write word (rather than byte)
TSL2561_BLOCK_BIT = 0x10      # 1 = using block read/write

TSL2561_CONTROL_POWERON = 0x03
TSL2561_CONTROL_POWEROFF = 0x00

TSL2561_LUX_LUXSCALE = 14             # Scale by 2^14
TSL2561_LUX_RATIOSCALE = 9            # Scale ratio by 2^9
TSL2561_LUX_CHSCALE = 10              # Scale channel values by 2^10
TSL2561_LUX_CHSCALE_TINT0 = 0x7517    # 322/11 * 2^TSL2561_LUX_CHSCALE
TSL2561_LUX_CHSCALE_TINT1 = 0x0FE7    # 322/81 * 2^TSL2561_LUX_CHSCALE

# T, FN and CL package values
TSL2561_LUX_K1T = 0x0040    # 0.125 * 2^RATIO_SCALE
TSL2561_LUX_B1T = 0x01f2    # 0.0304 * 2^LUX_SCALE
TSL2561_LUX_M1T = 0x01be    # 0.0272 * 2^LUX_SCALE
TSL2561_LUX_K2T = 0x0080    # 0.250 * 2^RATIO_SCALE
TSL2561_LUX_B2T = 0x0214    # 0.0325 * 2^LUX_SCALE
TSL2561_LUX_M2T = 0x02d1    # 0.0440 * 2^LUX_SCALE
TSL2561_LUX_K3T = 0x00c0    # 0.375 * 2^RATIO_SCALE
TSL2561_LUX_B3T = 0x023f    # 0.0351 * 2^LUX_SCALE
TSL2561_LUX_M3T = 0x037b    # 0.0544 * 2^LUX_SCALE
TSL2561_LUX_K4T = 0x0100    # 0.50 * 2^RATIO_SCALE
TSL2561_LUX_B4T = 0x0270    # 0.0381 * 2^LUX_SCALE
TSL2561_LUX_M4T = 0x03fe    # 0.0624 * 2^LUX_SCALE
TSL2561_LUX_K5T = 0x0138    # 0.61 * 2^RATIO_SCALE
TSL2561_LUX_B5T = 0x016f    # 0.0224 * 2^LUX_SCALE
TSL2561_LUX_M5T = 0x01fc    # 0.0310 * 2^LUX_SCALE
TSL2561_LUX_K6T = 0x019a    # 0.80 * 2^RATIO_SCALE
TSL2561_LUX_B6T = 0x00d2    # 0.0128 * 2^LUX_SCALE
TSL2561_LUX_M6T = 0x00fb    # 0.0153 * 2^LUX_SCALE
TSL2561_LUX_K7T = 0x029a    # 1.3 * 2^RATIO_SCALE
TSL2561_LUX_B7T = 0x0018    # 0.00146 * 2^LUX_SCALE
TSL2561_LUX_M7T = 0x0012    # 0.00112 * 2^LUX_SCALE
TSL2561_LUX_K8T = 0x029a    # 1.3 * 2^RATIO_SCALE
TSL2561_LUX_B8T = 0x0000    # 0.000 * 2^LUX_SCALE
TSL2561_LUX_M8T = 0x0000    # 0.000 * 2^LUX_SCALE

# Auto-gain thresholds
TSL2561_AGC_THI_13MS = 4850     # Max value at Ti 13ms = 5047
TSL2561_AGC_TLO_13MS = 100
TSL2561_AGC_THI_101MS = 36000   # Max value at Ti 101ms = 37177
TSL2561_AGC_TLO_101MS = 200
TSL2561_AGC_THI_402MS = 63000   # Max value at Ti 402ms = 65535
TSL2561_AGC_TLO_402MS = 500

# Clipping thresholds
TSL2561_CLIPPING_13MS = 4900
TSL2561_CLIPPING_101MS = 37000
TSL2561_CLIPPING_402MS = 65000

TSL2561_REGISTER_CONTROL = 0x00
TSL2561_REGISTER_TIMING = 0x01
TSL2561_REGISTER_THRESHHOLDL_LOW = 0x02
TSL2561_REGISTER_THRESHHOLDL_HIGH = 0x03
TSL2561_REGISTER_THRESHHOLDH_LOW = 0x04
TSL2561_REGISTER_THRESHHOLDH_HIGH = 0x05
TSL2561_REGISTER_INTERRUPT = 0x06
TSL2561_REGISTER_CRC = 0x08
TSL2561_REGISTER_ID = 0x0A
TSL2561_REGISTER_CHAN0_LOW = 0x0C
TSL2561_REGISTER_CHAN0_HIGH = 0x0D
TSL2561_REGISTER_CHAN1_LOW = 0x0E
TSL2561_REGISTER_CHAN1_HIGH = 0x0F

TSL2561_INTEGRATIONTIME_13MS = 0x00     # 13.7ms
TSL2561_INTEGRATIONTIME_101MS = 0x01    # 101ms
TSL2561_INTEGRATIONTIME_402MS = 0x02    # 402ms

TSL2561_GAIN_1X = 0x00    # No gain
TSL2561_GAIN_16X = 0x10   # 16x gain


class TSL2561(I2C):
    def __init__ (self, lock=None):
        if sys.version_info >= (3,0):
            super().__init__(lock)
        else:
            super(TSL2561, self).__init__(lock)

        self.__lastvalue = 0

        self.address = TSL2561_ADDR_FLOAT

        self.integration_time = TSL2561_DELAY_INTTIME_402MS
        self.gain = TSL2561_GAIN_1X
        self.autogain = False

        self._begin()


    def _begin(self):
        '''Initializes I2C and configures the sensor (call this function before
        doing anything else)
        '''
        # Make sure we're actually connected
        x = I2C._bus.read_byte_data(self.address, TSL2561_REGISTER_ID)

        if not x & 0x0A:
            raise Exception('TSL2561 not found!')
        ##########

        # Set default integration time and gain
        self.set_integration_time(self.integration_time)
        self.set_gain(self.gain)

        # Note: by default, the device is in power down mode on bootup
        self.disable()

    def enable(self):
        '''Enable the device by setting the control bit to 0x03'''
        I2C._bus.write_byte_data(self.address,
                                 TSL2561_COMMAND_BIT | TSL2561_REGISTER_CONTROL,
                                 TSL2561_CONTROL_POWERON)

    def disable(self):
        '''Disables the device (putting it in lower power sleep mode)'''
        I2C._bus.write_byte_data(self.address,
                                 TSL2561_COMMAND_BIT | TSL2561_REGISTER_CONTROL,
                                 TSL2561_CONTROL_POWEROFF)

    @staticmethod
    def delay(value):
        '''Delay times must be specified in milliseconds but as the python
        sleep function only takes (float) seconds we need to convert the sleep
        time first
        '''
        time.sleep(value / 1000.0)

    def _get_data(self):
        '''Private function to read luminosity on both channels'''

        # Enable the device by setting the control bit to 0x03
        self.enable()

        # Wait x ms for ADC to complete
        TSL2561.delay(self.integration_time)

        # Reads a two byte value from channel 0 (visible + infrared)
        broadband = I2C._bus.read_word_data(self.address,
                                            TSL2561_COMMAND_BIT | TSL2561_WORD_BIT |
                                            TSL2561_REGISTER_CHAN0_LOW)

        # Reads a two byte value from channel 1 (infrared)
        ir = I2C._bus.read_word_data(self.address,
                                     TSL2561_COMMAND_BIT | TSL2561_WORD_BIT |
                                     TSL2561_REGISTER_CHAN1_LOW)

        # Turn the device off to save power
        self.disable()

        return (broadband, ir)

    def set_integration_time(self, integration_time):
        '''Sets the integration time for the TSL2561'''

        # Enable the device by setting the control bit to 0x03
        self.enable()

        self.integration_time = integration_time

        # Update the timing register
        I2C._bus.write_byte_data(self.address,
                                 TSL2561_COMMAND_BIT | TSL2561_REGISTER_TIMING,
                                 self.integration_time | self.gain)

        # Turn the device off to save power
        self.disable()

    def set_gain(self, gain):
        '''Adjusts the gain on the TSL2561 (adjusts the sensitivity to light)
        '''

        # Enable the device by setting the control bit to 0x03
        self.enable()

        self.gain = gain

        # Update the timing register
        I2C._bus.write_byte_data(self.address,
                                 TSL2561_COMMAND_BIT | TSL2561_REGISTER_TIMING,
                                 self.integration_time | self.gain)

        # Turn the device off to save power
        self.disable()

    def set_auto_range(self, value):
        '''Enables or disables the auto-gain settings when reading
        data from the sensor
        '''
        self.autogain = value

    def _get_luminosity(self):
        '''Gets the broadband (mixed lighting) and IR only values from
        the TSL2561, adjusting gain if auto-gain is enabled
        '''
        valid = False

        # If Auto gain disabled get a single reading and continue
        if not self.autogain:
            return self._get_data()

        # Read data until we find a valid range
        _agcCheck = False
        broadband = 0
        ir = 0

        while not valid:
            if self.integration_time == TSL2561_INTEGRATIONTIME_13MS:
                _hi = TSL2561_AGC_THI_13MS
                _lo = TSL2561_AGC_TLO_13MS
            elif self.integration_time == TSL2561_INTEGRATIONTIME_101MS:
                _hi = TSL2561_AGC_THI_101MS
                _lo = TSL2561_AGC_TLO_101MS
            else:
                _hi = TSL2561_AGC_THI_402MS
                _lo = TSL2561_AGC_TLO_402MS

            _b, _ir = self._get_data()

            # Run an auto-gain check if we haven't already done so ...
            if not _agcCheck:
                if _b < _lo and self.gain == TSL2561_GAIN_1X:
                    # Increase the gain and try again
                    self.set_gain(TSL2561_GAIN_16X)
                    # Drop the previous conversion results
                    _b, _ir = self._get_data()
                    # Set a flag to indicate we've adjusted the gain
                    _agcCheck = True
                elif _b > _hi and self.gain == TSL2561_GAIN_16X:
                    # Drop gain to 1x and try again
                    self.set_gain(TSL2561_GAIN_1X)
                    # Drop the previous conversion results
                    _b, _ir = self._get_data()
                    # Set a flag to indicate we've adjusted the gain
                    _agcCheck = True
                else:
                    # Nothing to look at here, keep moving ....
                    # Reading is either valid, or we're already at the chips
                    # limits
                    broadband = _b
                    ir = _ir
                    valid = True
            else:
                # If we've already adjusted the gain once, just return the new
                # results.
                # This avoids endless loops where a value is at one extreme
                # pre-gain, and the the other extreme post-gain
                broadband = _b
                ir = _ir
                valid = True

        return (broadband, ir)

    def _calculate_lux(self, broadband, ir):
        '''Converts the raw sensor values to the standard SI lux equivalent.
        Returns 0 if the sensor is saturated and the values are unreliable.
        '''
        # Make sure the sensor isn't saturated!
        if self.integration_time == TSL2561_INTEGRATIONTIME_13MS:
            clipThreshold = TSL2561_CLIPPING_13MS
        elif self.integration_time == TSL2561_INTEGRATIONTIME_101MS:
            clipThreshold = TSL2561_CLIPPING_101MS
        else:
            clipThreshold = TSL2561_CLIPPING_402MS

        # Return 0 lux if the sensor is saturated
        if broadband > clipThreshold or ir > clipThreshold:
            raise Exception('Sensor is saturated')

        # Get the correct scale depending on the integration time
        if self.integration_time == TSL2561_INTEGRATIONTIME_13MS:
            chScale = TSL2561_LUX_CHSCALE_TINT0
        elif self.integration_time == TSL2561_INTEGRATIONTIME_101MS:
            chScale = TSL2561_LUX_CHSCALE_TINT1
        else:
            chScale = 1 << TSL2561_LUX_CHSCALE

        # Scale for gain (1x or 16x)
        if not self.gain:
            chScale = chScale << 4

        # Scale the channel values
        channel0 = (broadband * chScale) >> TSL2561_LUX_CHSCALE
        channel1 = (ir * chScale) >> TSL2561_LUX_CHSCALE

        # Find the ratio of the channel values (Channel1/Channel0)
        ratio1 = 0
        if channel0 != 0:
            ratio1 = (channel1 << (TSL2561_LUX_RATIOSCALE + 1)) / channel0

        # round the ratio value
        # ratio = (ratio1 + 1) >> 1 ########### strange rounding
        ratio = ratio1

        b = 0
        m = 0

        if ratio >= 0 and ratio <= TSL2561_LUX_K1T:
            b = TSL2561_LUX_B1T
            m = TSL2561_LUX_M1T
        elif ratio <= TSL2561_LUX_K2T:
            b = TSL2561_LUX_B2T
            m = TSL2561_LUX_M2T
        elif ratio <= TSL2561_LUX_K3T:
            b = TSL2561_LUX_B3T
            m = TSL2561_LUX_M3T
        elif ratio <= TSL2561_LUX_K4T:
            b = TSL2561_LUX_B4T
            m = TSL2561_LUX_M4T
        elif ratio <= TSL2561_LUX_K5T:
            b = TSL2561_LUX_B5T
            m = TSL2561_LUX_M5T
        elif ratio <= TSL2561_LUX_K6T:
            b = TSL2561_LUX_B6T
            m = TSL2561_LUX_M6T
        elif ratio <= TSL2561_LUX_K7T:
            b = TSL2561_LUX_B7T
            m = TSL2561_LUX_M7T
        elif ratio > TSL2561_LUX_K8T:
            b = TSL2561_LUX_B8T
            m = TSL2561_LUX_M8T

        temp = (channel0 * b) - (channel1 * m)

        # Do not allow negative lux value
        if temp < 0:
            temp = 0

        # Round lsb (2^(LUX_SCALE-1))
        temp += 1 << (TSL2561_LUX_LUXSCALE - 1)

        # Strip off fractional portion
        lux = temp >> TSL2561_LUX_LUXSCALE

        # Signal I2C had no errors
        return lux

    def lux(self):
        '''Read sensor data, convert it to LUX and return it'''
        broadband, ir = self._get_luminosity()

        try:
            v = self._calculate_lux(broadband, ir)
            self.__lastvalue = v
        except:
            print(strftime("%Y%m%d %X:"), "error getting lux in TSL2561.lux()")
        finally:
            return self.__lastvalue

# eof #

