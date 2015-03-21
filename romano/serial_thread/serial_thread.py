import serial
import re
import time, random
from PySide import QtCore

class SerialThread(QtCore.QThread):
  dataReady = QtCore.Signal(float)
  serialException = QtCore.Signal(Exception)
  
  def __init__(self, port, regex, end_char, baudrate, parity_, bytesize_, simulate = False):
    super(SerialThread, self).__init__()
    self.regex = regex
    self.end_char = end_char
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
          char = self.s.read()
          if char is not self.end_char:
            data_string += char
          else:
            break
      else:
        time.sleep(0.3)
      try:
        if not self.simulate:
          data = float(re.search(self.regex, data_string).group())
        else: 
          data = round(1000 * random.random(), 2)
      except:
        data = -1
      self.dataReady.emit(data)
    if not self.simulate:
      self.s.close()

  def isAlive(self):
    return self.alive
