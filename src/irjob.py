# -*- coding:utf-8 -*-

from abc import abstractmethod
import time

BANK_MAX = 640


class irjob(object):
    def __init__(self, ir_serial):
        self._ir_serial = ir_serial

    @abstractmethod
    def do(self):
        raise NotImplementedError()


class version_job(irjob):
    def __init__(self, ir_serial, timeout=1.5):
        irjob.__init__(self, ir_serial)
        self._timeout = timeout
    
    def do(self):
        start_time = time.time()
        self._ir_serial.write('v\r\n'.encode('utf-8'))
        version = None
        while(1):
            elapse = time.time() - start_time
            if elapse >= self._timeout:
                break
            version = self._ir_serial.readline().strip().decode('utf-8')
            if len(version) > 0 and 'OK' not in version:
                break
        self._ir_serial.readline()
        return version


class led_job(irjob):
    def __init__(self, ir_serial, light_on=True, wait=1.0):
        irjob.__init__(self, ir_serial)
        self._light_on = light_on
        self._wait = wait
    
    def do(self):
        light_value = None
        if(self._light_on):
            light_value = 1
        else:
            light_value = 0
        self._ir_serial.write(('l,' + str(light_value) + '\r\n').encode('utf-8'))
        
        time.sleep(self._wait)
        status = self._ir_serial.readline().strip().decode('utf-8')


class capture_job(irjob):
    def __init__(self, ir_serial, timeout=10.0):
        irjob.__init__(self, ir_serial)
        self._timeout = timeout
    
    def do(self):
        self._ir_serial.write('c\r\n'.encode('utf-8'))
        dots_str = self._ir_serial.read(3).decode('utf-8')
        if dots_str != '...':
              return
        serial_str = ''
        start_time = time.time()
        while '\r\n' not in serial_str:
            elapse = time.time() - start_time
            if elapse >= self._timeout:
                return
            serial_str = self._ir_serial.readline().decode('utf-8')

        data_size = 0
        if 'Time Out !' in serial_str or 'Ready' in serial_str:
            return data_size
        else:
            try:
                data_size = int(serial_str.strip())
                return data_size
            except ValueError:
                return


class read_job(irjob):
    def __init__(self, ir_serial):
        irjob.__init__(self, ir_serial)

    def do(self):
        data = []
        for n in range(BANK_MAX):
            bank = n / 64
            pos = n % 64
            if pos == 0:
                self._ir_serial.write(("b,%d\r\n" % bank).encode('utf-8'))
            self._ir_serial.write(("d,%d\n\r" % pos).encode('utf-8'))
            x_str = self._ir_serial.read(3).decode('utf-8')
            x_data = None
            try:
                x_data = int(x_str, 16)
                if x_data == 0:
                    break
                data.append(x_data)
            except ValueError:
                break
        return data


class write_job(irjob):
    def __init__(self, ir_serial, data):
        irjob.__init__(self, ir_serial)
        self.data = data
    
    def do(self):
        data_size = len(self.data)
        for n in range(data_size):
            bank = n / 64
            pos = n % 64
            if (pos == 0):
                self._ir_serial.write(("b,%d\r\n" % bank).encode('utf-8'))
            self._ir_serial.write(("w,%d,%d\n\r" % (pos, self.data[n])).encode('utf-8'))


class send_job(irjob):
    def __init__(self, ir_serial):
        irjob.__init__(self, ir_serial)
    
    def do(self):
        self._ir_serial.write(("p\r\n").encode('utf-8'))
        serial_str = ''
        while '\r\n' not in serial_str:
            serial_str = self._ir_serial.readline().decode('utf-8')