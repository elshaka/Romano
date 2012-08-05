import serial
import time, random
from PySide import QtCore

class SerialThread(QtCore.QThread):
  dataReady = QtCore.Signal(float)
  serialException = QtCore.Signal(Exception)
  
  def __init__(self, port, simulate = False):
    super(SerialThread, self).__init__()
    self.simulate = simulate
    self.alive = True
    try:
      if not self.simulate:      
        self.s = serial.Serial(port)
      self.serial_ok = True
    except Exception, e:
      self.serialException.emit(e)
      self.serial_ok = False
  
  def run(self):
    while self.serial_ok and self.isAlive():
      if not self.simulate:
        data_string = self.s.readline()
      else:
        time.sleep(0.3)
      try:
        if not self.simulate:
          data = float(data_string.split()[1][:data_string.split()[1].find('K')])
        else: 
          data = round(1000 * random.random(), 2)
      except:
        data = -1
      self.dataReady.emit(data)
    if not self.simulate:
      self.s.close()

  def isAlive(self):
    return self.alive
