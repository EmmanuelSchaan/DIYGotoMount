##############################################33
#
import numpy as np

import subprocess
import yaml
from time import sleep


import sys
from PyQt4 import QtGui, QtCore

class Window(QtGui.QMainWindow):

   def __init__(self, motorRa, motorDec):
      super(Window, self).__init__()
      self.setGeometry(50, 50, 500, 500)
      self.setWindowTitle("Goto Mount Controller")
      self.setWindowIcon(QtGui.QIcon('pythonlogo.png'))
      self.home()

      # motors
      self.motorRa = motorRa
      self.motorDec = motorDec

      # default mode: sidereal tracking
      self.motorRa.setTargetStepVelocity(self.motorRa.stepSpeedSiderealTracking)

   def home(self):

      # Quit button 
      self.btnQuit = QtGui.QPushButton("Quit", self)
      #self.btnQuit.clicked.connect(QtCore.QCoreApplication.instance().quit)
      self.btnQuit.clicked.connect(self.quit)
      self.btnQuit.resize(100,100)
      self.btnQuit.move(300,400)

      # tracking toggle button
      self.btnTracking = QtGui.QPushButton("Tracking ON", self)
      self.btnTracking.setCheckable(True)
      self.btnTracking.setStyleSheet("background-color : lightgreen")
      self.btnTracking.clicked.connect(self.toggleTracking)
      self.btnTracking.resize(100,100)
      self.btnTracking.move(100,400)

      # RA minus
      self.btnRaMinus = QtGui.QPushButton("RA-", self)
      #self.btnRaMinus.clicked.connect(self.slewBtnPressed)
      self.btnRaMinus.pressed.connect(lambda : self.slewBtnPressed('raMinus'))
      self.btnRaMinus.released.connect(lambda : self.slewBtnReleased('raMinus'))
      self.btnRaMinus.resize(100,100)
      self.btnRaMinus.move(100,100)

      # RA plus
      self.btnRaPlus = QtGui.QPushButton("RA+", self)
      #self.btnRaPlus.clicked.connect(self.increaseRa)
      self.btnRaPlus.pressed.connect(lambda : self.slewBtnPressed('raPlus'))
      self.btnRaPlus.released.connect(lambda : self.slewBtnReleased('raPlus'))
      self.btnRaPlus.resize(100,100)
      self.btnRaPlus.move(300,100)

      # Dec minus
      self.btnDecMinus = QtGui.QPushButton("Dec-", self)
      #self.btnDecMinus.clicked.connect(self.decreaseDec)
      self.btnDecMinus.pressed.connect(lambda : self.slewBtnPressed('decMinus'))
      self.btnDecMinus.released.connect(lambda : self.slewBtnReleased('decMinus'))
      self.btnDecMinus.resize(100,100)
      self.btnDecMinus.move(200,200)

      # Dec plus
      self.btnDecPlus = QtGui.QPushButton("Dec+", self)
      #self.btnDecPlus.clicked.connect(self.increaseDec)
      self.btnDecPlus.pressed.connect(lambda : self.slewBtnPressed('decPlus'))
      self.btnDecPlus.released.connect(lambda : self.slewBtnReleased('decPlus'))
      self.btnDecPlus.resize(100,100)
      self.btnDecPlus.move(200,0)

      # Stop
      self.btnStop = QtGui.QPushButton("Stop", self)
      self.btnStop.clicked.connect(self.stop)
      self.btnStop.resize(100,100)
      self.btnStop.move(200,100)

      # Current RA
      self.txtRa = QtGui.QLineEdit("RA", self)
      self.txtRa.resize(100,40)
      self.txtRa.move(0, 0)

      # Current Dec
      self.txtDec = QtGui.QLineEdit("Dec", self)
      self.txtDec.resize(100,40)
      self.txtDec.move(0, 45)

      self.update()
      self.show()

   def quit(self):
      self.motorRa.deenergize()
      self.motorDec.deenergize()
      QtCore.QCoreApplication.instance().quit()


   def toggleTracking(self):
        if self.btnTracking.isChecked(): 
            # setting background color to light-blue 
            self.btnTracking.setStyleSheet("background-color : red") 
            self.btnTracking.setText("Tracking OFF")
            self.motorRa.setTargetStepVelocity(0)
        else: 
            # set background color back to light-grey 
            self.btnTracking.setStyleSheet("background-color : lightgreen")
            self.btnTracking.setText("Tracking ON")
            self.motorRa.setTargetStepVelocity(self.motorRa.stepSpeedSiderealTracking)


   def slewBtnPressed(self, direction):
      '''direction = 'raPlus', 'raMinus', 'decPlus', 'decMinus'
      '''
      #print 'button pressed!'
      #print direction
      if direction=='raPlus':
         self.motorRa.setTargetStepVelocity(self.motorRa.maxStepSpeed)
      elif direction=='raMinus':
         self.motorRa.setTargetStepVelocity(-self.motorRa.maxStepSpeed)
      elif direction=='decPlus':
         self.motorDec.setTargetStepVelocity(self.motorDec.maxStepSpeed)
      elif direction=='decMinus':
         self.motorDec.setTargetStepVelocity(-self.motorDec.maxStepSpeed)


   def slewBtnReleased(self, direction):
      '''direction = 'raPlus', 'raMinus', 'decPlus', 'decMinus'
      '''
      #print 'button released!'
      #print direction
      if direction=='raPlus':
         self.motorRa.setTargetStepVelocity(0)
      elif direction=='raMinus':
         self.motorRa.setTargetStepVelocity(0)
      elif direction=='decPlus':
         self.motorDec.setTargetStepVelocity(0)
      elif direction=='decMinus':
         self.motorDec.setTargetStepVelocity(0)



   def stop(self):
      '''Halts the motors, interrupt or not the tracking
      '''
      self.motorRa.halt()
      self.motorDec.halt()
        


##############################################33


def ticcmd(*args):
   return subprocess.check_output(['ticcmd'] + list(args))

class Motor(object):

   def __init__(self, ticid):
      self.ticid = ticid

      # gearbox * pinion-wheel  reduction factor
      # gearbox: 99. + 104./2057.
      # pinion-wheel: 84./20. = 4.2
      self.reductionFactor = (99.+104./2057.) * (84./20.)
      self.stepsPerRotation = 200.  # typical for stepper motors

      # settings
      self.current = 192   # [mA]
      self.microStepping = 16 # [microsteps per step]
      self.maxStepSpeed = 400000000 # [1.e-4 steps/sec]
      self.maxStepAccel = 4000000   # [1.e-2 steps/sec^2]
      self.maxStepDecel = 4000000   # [1.e-2 steps/sec^2]

      # sidereal tracking step speed
      self.stepSpeedSiderealTracking = self.computeStepSpeedTracking()  # [1.e-4 steps/sec]

      # energize the motor
      ticcmd('-d', self.ticid, '--current', str(self.current))
      ticcmd('-d', self.ticid, '--energize')
      # disable safe start
      ticcmd('-d', self.ticid, '--exit-safe-start')
      # microstepping
      ticcmd('-d', self.ticid, '--step-mode', str(self.microStepping))
      # set max speed, acceleration, decay mode
      ticcmd('-d', self.ticid, '--max-speed', str(self.maxStepSpeed))
      ticcmd('-d', self.ticid, '--max-accel', str(self.maxStepAccel))
      ticcmd('-d', self.ticid, '--max-decel', str(self.maxStepDecel))
      ticcmd('-d', self.ticid, '--decay', 'mixed50')

   def computeStepSpeedTracking(self):
      '''result in [1,e-4 steps/sec], as required by ticcmd
      '''
      siderealDay = 23.9344696 * 3600.   # [sec]
      result = self.stepsPerRotation * self.reductionFactor * self.microStepping # [steps per sidereal day]
      result /= siderealDay  # [steps/sec]
      result *= 1.e4 # [1.e-4 steps/sec]
      return np.int(result)

   def getCurrentStepPosition(self):
      status = yaml.load(ticcmd('-d', self.ticid, '-s', '--full'))
      position = status['Current position']
      print("Current position is {}.".format(position))
      return position

   def deenergize(self):
      print("Deenergizing motor")
      ticcmd('-d', self.ticid, '--deenergize')

   def halt(self):
      print("Halting motor")
      ticcmd('-d', self.ticid, '--halt-and-hold')


   def setTargetStepPosition(self, targetPosition):
      print("Setting target position to {}.".format(targetPosition))
      ticcmd('-d', self.ticid, '--position', str(targetPosition))

   def setTargetStepVelocity(self, targetVelocity):
      print("Setting target velocity to {}.".format(targetVelocity))
      ticcmd('-d', self.ticid, '--velocity', str(targetVelocity))



##############################################33


def run():
   # motors
   ticidRa = '00315372'
   ticidDec = '00315338'
   motorRa = Motor(ticidRa)
   motorDec = Motor(ticidDec)

   # gui
   app = QtGui.QApplication(sys.argv)
   GUI = Window(motorRa, motorDec)
   sys.exit(app.exec_())


run()
