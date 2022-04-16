import serial
import time


class Sensor:
    def __init__(self):
        self.ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=0)  # mini UART serial device
        if not self.ser.isOpen():
            self.ser.open()  # open serial port if not open
        self.set_samp_rate(200)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ser.close()

    def set_samp_rate(self, samp_rate=100):
        ##########################
        # change the sample rate
        samp_rate_packet = [0x5a, 0x06, 0x03, samp_rate, 00, 00]  # sample rate byte array
        self.ser.write(samp_rate_packet)  # send sample rate instruction
        time.sleep(0.1)  # wait for change to take effect

    def read_data(self):
        while True:
            counter = self.ser.in_waiting  # count the number of bytes of the serial port
            if counter > 8:
                bytes_serial = self.ser.read(9)  # read 9 bytes
                self.ser.reset_input_buffer()  # reset buffer

                if bytes_serial[0] == 0x59 and bytes_serial[1] == 0x59:  # check first two bytes
                    distance = bytes_serial[2] + bytes_serial[3] * 256  # distance in next two bytes
                    strength = bytes_serial[4] + bytes_serial[5] * 256  # signal strength in next two bytes
                    temperature = bytes_serial[6] + bytes_serial[7] * 256  # temp in next two bytes
                    temperature = (temperature / 8.0) - 256.0  # temp scaling and offset
                    return distance, strength, temperature
