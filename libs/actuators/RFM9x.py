# -*- coding: utf-8 -*-
###############################################################################
# RFM9x.py                                                                    #
# Library for the RFM9x LoRa Module.                                          #
# Sourcecode taken and modified from:                                         #
# * https://github.com/ladecadence/pyRF95                                     #
# * https://github.com/PiInTheSky/lora-gateway/blob/master/gateway.c          #
# * https://pypi.org/project/pyLoraRFM9x/                                     #
# (c) https://github.com/thomaspfeiffer-git 2018, 2020                        #
###############################################################################
"""Library for the RFM9x LoRa Module."""

# Useful links:
# * Data sheet: http://www.hoperf.com/upload/rf/RFM95_96_97_98W.pdf
# * Adafruit: https://learn.adafruit.com/adafruit-rfm69hcw-and-rfm96-rfm95-rfm98-lora-packet-padio-breakouts
# Hints on distance tuning:
# http://wiki.dragino.com/index.php?title=LoRa_Questions#Check_the_Modem_Setting_in_Software


import RPi.GPIO as GPIO
import spidev
import sys
import time


from Logging import Log
from actuators.RFM9x_constants import *


class RFM9x (object):
    def __init__ (self, config, frequency, int_pin, reset_pin, cs=0):
        self.spi = spidev.SpiDev()
        self.spi_cs = cs
        self.config = config
        self.frequency = frequency
        self.int_pin = int_pin
        self.reset_pin = reset_pin
        self.mode = RADIO_MODE_INITIALISING
        self.buf=[]         # RX Buffer for interrupts
        self.buflen=0       # RX Buffer length
        self.last_rssi=-99  # last packet RSSI
        self.rx_bad = 0     # rx error count
        self.tx_good = 0    # tx packets sent
        self.rx_good = 0    # rx packets recv
        self.rx_buf_valid = False

    def init (self):
        """open SPI and initialize RF95"""
        self.spi.open(0, self.spi_cs)
        self.spi.max_speed_hz = 244000

        # set interrupt pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(self.int_pin, GPIO.IN)
        GPIO.add_event_detect(self.int_pin, GPIO.RISING,
                              callback=self.handle_interrupt)

        # set reset pin
        if self.reset_pin != None:
            GPIO.setup(self.reset_pin, GPIO.OUT)
            GPIO.output(self.reset_pin, GPIO.LOW)
            time.sleep(0.05)
            GPIO.output(self.reset_pin, GPIO.HIGH)
        # wait for reset
        time.sleep(0.05)

        # set sleep mode and LoRa mode
        self.spi_write(REG_01_OP_MODE, MODE_SLEEP | LONG_RANGE_MODE)

        time.sleep(0.05)
        # check if we are set
        if self.spi_read(REG_01_OP_MODE) != (MODE_SLEEP | LONG_RANGE_MODE):
            return False

        # set up FIFO
        self.spi_write(REG_0E_FIFO_TX_BASE_ADDR, 0)
        self.spi_write(REG_0F_FIFO_RX_BASE_ADDR, 0)

        # default mode
        self.set_mode_idle()

        self.set_modem_config()
        self.set_preamble_length(8)
        self.set_frequency(self.frequency)

        return True

    def handle_interrupt(self, channel):
        # Read the interrupt register
        irq_flags = self.spi_read(REG_12_IRQ_FLAGS)

        if self.mode == RADIO_MODE_RX and irq_flags & (RX_TIMEOUT | PAYLOAD_CRC_ERROR):
            self.rx_bad = self.rx_bad + 1
            Log("Error: Bad packet received; irq_flags: {:x}".format(irq_flags))
        elif self.mode == RADIO_MODE_RX and irq_flags & RX_DONE:
            # packet received
            length = self.spi_read(REG_13_RX_NB_BYTES)
            # Reset the fifo read ptr to the beginning of the packet
            self.spi_write(REG_0D_FIFO_ADDR_PTR, self.spi_read(REG_10_FIFO_RX_CURRENT_ADDR))
            self.buf = self.spi_read_data(REG_00_FIFO, length)
            self.buflen = length
            # clear IRQ flags
            self.spi_write(REG_12_IRQ_FLAGS, 0xff)

            # AFC shall be done only if a correct packet was receveived.
            # Therefore AFC shall be called by after verification of
            # the received data.
            # self.afc()

            # save RSSI
            self.last_rssi = self.spi_read(REG_1A_PKT_RSSI_VALUE) - 137
            # We have received a message
            self.rx_good = self.rx_good + 1
            self.rx_buf_valid = True
            self.set_mode_idle()

        elif self.mode == RADIO_MODE_TX and irq_flags & TX_DONE:
            self.tx_good = self.tx_good + 1
            self.set_mode_idle()

        elif self.mode == RADIO_MODE_CAD and irq_flags & CAD_DONE:
            self.cad = irq_flags & CAD_DETECTED
            self.set_mode_idle()

        self.spi_write(REG_12_IRQ_FLAGS, 0xff) # Clear all IRQ flags

    def afc (self):
        """automatic frequency control; taken from
           https://github.com/PiInTheSky/lora-gateway/blob/master/gateway.c"""

        self.set_mode_rx()

        r28 = self.spi_read(REG_28_FREQ_ERROR)
        r29 = self.spi_read(REG_28_FREQ_ERROR+1)
        r30 = self.spi_read(REG_28_FREQ_ERROR+2)
        r28_2 = self.spi_read(REG_28_FREQ_ERROR)

        t = r28 & 7
        t = t << 8
        t += r29
        t = t << 8
        t += r30
        if r28_2 & 8:
            t -= 524288

        f_err = -(t * (1 << 24) / 32000000.0) * (self.config[LR_Cfg_BW] / 500.0)
        Log("Frequency Error: {:.2f} Hz".format(f_err))
        self.set_frequency(self.frequency+f_err)

        self.set_mode_idle()

    def spi_write(self, reg, data):
        self.spi.open(0,self.spi_cs)
        # transfer one byte
        self.spi.xfer2([reg | SPI_WRITE_MASK, data])
        self.spi.close()

    def spi_read(self, reg):
        self.spi.open(0,self.spi_cs)
        data = self.spi.xfer2([reg & ~SPI_WRITE_MASK, 0])
        self.spi.close()
        return data[1]

    def spi_write_data(self, reg, data):
        self.spi.open(0, self.spi_cs)
        # transfer byte list
        self.spi.xfer2([reg | SPI_WRITE_MASK] + data)
        self.spi.close()

    def spi_read_data(self, reg, length):
        data = []
        self.spi.open(0, self.spi_cs)
        # start address + amount of bytes to read
        data = self.spi.xfer2([reg & ~SPI_WRITE_MASK] + [0]*length)
        self.spi.close()
        return data[1:] # all but first byte

    def set_frequency(self, freq):
        self.frequency = freq
        Log("Setting frequency to {:.2f} Hz".format(freq))
        freq_value = int(freq / FSTEP)

        self.spi_write(REG_06_FRF_MSB, (freq_value>>16)&0xff)
        self.spi_write(REG_07_FRF_MID, (freq_value>>8)&0xff)
        self.spi_write(REG_08_FRF_LSB, (freq_value)&0xff)

    def set_mode_idle(self):
        if self.mode != RADIO_MODE_IDLE:
            self.spi_write(REG_01_OP_MODE, MODE_STDBY)
            self.mode = RADIO_MODE_IDLE

    def sleep(self):
        if self.mode != RADIO_MODE_SLEEP:
            self.spi_write(REG_01_OP_MODE, MODE_SLEEP)
            self.mode = RADIO_MODE_SLEEP
        return True

    def set_mode_rx(self):
        if self.mode != RADIO_MODE_RX:
            self.spi_write(REG_01_OP_MODE, MODE_RXCONTINUOUS)
            self.spi_write(REG_40_DIO_MAPPING1, 0x00)
            self.mode = RADIO_MODE_RX

    def set_mode_tx(self):
        if self.mode != RADIO_MODE_TX:
            self.spi_write(REG_01_OP_MODE, MODE_TX)
            self.spi_write(REG_40_DIO_MAPPING1, 0x40)
            self.mode = RADIO_MODE_TX
        return True

    def set_tx_power(self, power):
        #self.spi_write(REG_09_PA_CONFIG, power)
        PA_SELECT = 0x80
        # TODO https://github.com/mugpahug/pyLoraRFM9x/blob/master/pyLoraRFM9x/lora.py#L112
        self.spi_write(REG_4D_PA_DAC, PA_DAC_ENABLE)
        self.spi_write(REG_09_PA_CONFIG, PA_SELECT | 23)

    def set_lna(self, lna):
        self.spi_write(REG_0C_LNA, lna)

    # set a default mode
    def set_modem_config(self):
        self.spi_write(REG_1D_MODEM_CONFIG1, self.config[LR_Cfg_Reg1])
        self.spi_write(REG_1E_MODEM_CONFIG2, self.config[LR_Cfg_Reg2])
        self.spi_write(REG_26_MODEM_CONFIG3, self.config[LR_Cfg_Reg3])

    def set_preamble_length(self, length):
        self.spi_write(REG_20_PREAMBLE_MSB, length >> 8)
        self.spi_write(REG_21_PREAMBLE_LSB, length & 0xff)

    # send data list
    def send(self, data):
        if len(data) > MAX_MESSAGE_LEN:
            return False

        self.wait_packet_sent()
        self.set_mode_idle()
        self.spi_write(REG_0D_FIFO_ADDR_PTR, 0)

        # write data
        self.spi_write_data(REG_00_FIFO, data)
        self.spi_write(REG_22_PAYLOAD_LENGTH, len(data))

        # put radio in TX mode
        self.set_mode_tx()
        return True

    def wait_packet_sent(self):
        while self.mode == RADIO_MODE_TX:
            pass
        return True

    def available(self):
        if self.mode == RADIO_MODE_TX:
            return False
        self.set_mode_rx()
        return self.rx_buf_valid

    def clear_rx_buf(self):
        self.rx_buf_valid = False
        self.buflen = 0

    # receive data list
    def recv(self):
        if not self.available():
            return False
        data = self.buf
        self.clear_rx_buf()
        return data

    # helper method to send bytes
    def bytes_to_data(self, bytelist):
        data = []
        for i in bytelist:
            data.append(i)
        return data

    # helper method to send strings
    def str_to_data(self, string):
        data = []
        for i in string:
            data.append(ord(i))
        return data

    # cleans all GPIOs, etc
    def cleanup(self):
        self.spi.close()
        if self.reset_pin:
            GPIO.output(self.reset_pin, GPIO.LOW)
            GPIO.cleanup(self.reset_pin)
        if self.int_pin:
            GPIO.cleanup(self.int_pin)

# eof #

