import serial
import re
import time, random
from PySide import QtCore

class SerialThread(QtCore.QThread):
  dataReady = QtCore.Signal(float)
  serialException = QtCore.Signal(Exception)
  
  def __init__(self, port, regex, baudrate, parity_, bytesize_, simulate = False):
    super(SerialThread, self).__init__()
    self.regex = regex
    self.simulate = simulate
    self.alive = True
    try:
      if not self.simulate:
        self.s = serial.Serial(port, baudrate, parity = parity_, bytesize = bytesize_)
      self.serial_ok = True
    except Exception as e:
      self.serialException.emit(e)
      self.serial_ok = False
  
  def run(self):
    while self.serial_ok and self.isAlive():
      if not self.simulate:
        data_string = ''
        while 1:
          char = self.s.read().decode()
          if char not in ['\n', '\r']:
            data_string += char
          elif data_string is not '':
            break
      else:
        time.sleep(0.3)
      try:
        if not self.simulate:
          data = float(re.search(self.regex, data_string).group())
        else: 
          data = round(10000 *(1 + random.random()), 2)
        self.dataReady.emit(data)
      except Exception as e:
        self.serialException.emit(e)
    if not self.simulate:
      self.s.close()

  def isAlive(self):
    return self.alive
