# -*- coding:utf-8 -*-

import serial

import irjob

BANK_MAX = 640

class pyMagician(object):    
    def __init__(self, port='/dev/ttyACM0', baudrate=9600, timeout=0.5):
        self._ir_serial = None
        self._port = port
        self._baudrate = baudrate
        self._timeout = timeout
        self._is_connect = False

    @property
    def is_connect(self):
        return self._is_connect

    def connect(self):
        try:
            self._is_connect = True
            self._ir_serial = serial.Serial(self._port, self._baudrate, timeout=self._timeout)
            return True
        except serial.serialutil.SerialException:
            self._is_connect = False
            self._ir_serial = None
            return False

    def close(self):
        self._is_connect = False
        self._ir_serial.close()
    
    def read_version(self, timeout=5.0):
        if self._is_connect:
            vjob = irjob.version_job(self._ir_serial, timeout=timeout)
            return vjob.do()
    
    def led_on(self, wait=1.0):
        if self._is_connect:
            ljob = irjob.led_job(self._ir_serial, light_on=True, wait=wait)
            ljob.do()
    
    def led_off(self, wait=1.0):
        if self._is_connect:
            ljob = irjob.led_job(self._ir_serial, light_on=False, wait=wait)
            ljob.do()
    
    def capture(self, timeout=10.0):
        if self._is_connect:
            cjob = irjob.capture_job(self._ir_serial, timeout=timeout)
            return cjob.do()
    
    def read_ir(self):
        if self._is_connect:
            rjob = irjob.read_job(self._ir_serial)
            return rjob.do()
    
    def write_ir(self, data):
        if self._is_connect:
            if len(data) <= BANK_MAX:
                lack_num = BANK_MAX - len(data)
                for _ in range(lack_num):
                    data.append(0)
            else:
                data = data[:BANK_MAX]
            wjob = irjob.write_job(self._ir_serial, data)
            wjob.do()

    def send_ir(self):
        if self._is_connect:
            sjob = irjob.send_job(self._ir_serial)
            sjob.do()