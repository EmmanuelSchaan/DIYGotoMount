import numpy as np

import subprocess
import yaml
from time import sleep

import sys
import os
from PyQt4 import QtGui, QtCore



##############################################33
# GUI


class Window(QtGui.QMainWindow):

   def __init__(self, motorRa, motorDec):
      
      # First, disable the two-finger right click daemon,
      # it messes up with the python gui
      os.system('killall twofing')

      super(Window, self).__init__()
      self.setGeometry(0, 0, 520, 320)
      self.setWindowTitle("Goto Mount Controller")
      self.setWindowIcon(QtGui.QIcon('pythonlogo.png'))
      self.setupGui()

      # motors
      self.motorRa = motorRa
      self.motorDec = motorDec

      # Path for images
      self.pathTestShots = '/home/pi/Desktop/DIYGotoMount/goto_mount/output/test_shots/'

      # default mode: sidereal tracking
      self.defaultMode()

   def setupGui(self):

      # Quit button 
      self.btnQuit = QtGui.QPushButton("Quit", self)
      self.btnQuit.clicked.connect(self.quit)
      self.btnQuit.resize(100,50)
      self.btnQuit.move(0,200)

      # Home button 
      self.btnHome = QtGui.QPushButton("Home", self)
      self.btnHome.clicked.connect(self.home)
      self.btnHome.resize(100,50)
      self.btnHome.move(0,150)

      # tracking toggle button
      self.btnTracking = QtGui.QPushButton("Tracking ON", self)
      self.btnTracking.setCheckable(True)
      self.btnTracking.setStyleSheet("background-color : lightgreen")
      self.btnTracking.clicked.connect(self.defaultMode)
      self.btnTracking.resize(100,50)
      self.btnTracking.move(0,100)

      # RA minus
      self.btnRaMinus = QtGui.QPushButton("RA-", self)
      #self.btnRaMinus.clicked.connect(self.slewBtnPressed)
      self.btnRaMinus.pressed.connect(lambda : self.slewBtnPressed('raMinus'))
      self.btnRaMinus.released.connect(lambda : self.slewBtnReleased('raMinus'))
      self.btnRaMinus.resize(50,50)
      self.btnRaMinus.move(100,50)

      # RA plus
      self.btnRaPlus = QtGui.QPushButton("RA+", self)
      #self.btnRaPlus.clicked.connect(self.increaseRa)
      self.btnRaPlus.pressed.connect(lambda : self.slewBtnPressed('raPlus'))
      self.btnRaPlus.released.connect(lambda : self.slewBtnReleased('raPlus'))
      self.btnRaPlus.resize(50,50)
      self.btnRaPlus.move(200,50)

      # Dec minus
      self.btnDecMinus = QtGui.QPushButton("Dec-", self)
      #self.btnDecMinus.clicked.connect(self.decreaseDec)
      self.btnDecMinus.pressed.connect(lambda : self.slewBtnPressed('decMinus'))
      self.btnDecMinus.released.connect(lambda : self.slewBtnReleased('decMinus'))
      self.btnDecMinus.resize(50,50)
      self.btnDecMinus.move(150,100)

      # Dec plus
      self.btnDecPlus = QtGui.QPushButton("Dec+", self)
      #self.btnDecPlus.clicked.connect(self.increaseDec)
      self.btnDecPlus.pressed.connect(lambda : self.slewBtnPressed('decPlus'))
      self.btnDecPlus.released.connect(lambda : self.slewBtnReleased('decPlus'))
      self.btnDecPlus.resize(50,50)
      self.btnDecPlus.move(150,0)

      # Stop
      self.btnStop = QtGui.QPushButton("Stop", self)
      self.btnStop.clicked.connect(self.stop)
      self.btnStop.resize(50,50)
      self.btnStop.move(150,50)

      # Current RA
      self.txtRa = QtGui.QLineEdit("RA", self)
      self.txtRa.resize(100,40)
      self.txtRa.move(0, 0)

      # Current Dec
      self.txtDec = QtGui.QLineEdit("Dec", self)
      self.txtDec.resize(100,40)
      self.txtDec.move(0, 45)

      # Camera Shutter
      self.btnShutter = QtGui.QPushButton("Shutter", self)
      self.btnShutter.clicked.connect(self.shutter)
      self.btnShutter.resize(100,50)
      self.btnShutter.move(250,0)

      # Test shot
      self.btnTestShot = QtGui.QPushButton("Test shot", self)
      self.btnTestShot.clicked.connect(self.testShot)
      self.btnTestShot.resize(100,50)
      self.btnTestShot.move(250,50)

      # Camera start/stop
      self.btnCameraStartStop = QtGui.QPushButton("Start", self)
      self.btnCameraStartStop.setCheckable(True)
      self.btnCameraStartStop.setStyleSheet("background-color : lightgreen")
      self.btnCameraStartStop.clicked.connect(self.cameraStartStop)
      self.btnCameraStartStop.resize(100,50)
      self.btnCameraStartStop.move(250,150)


      self.update()
      self.show()

   def quit(self):
      self.motorRa.deenergize()
      self.motorDec.deenergize()

      # re-enable the two-finger right click daemon
      os.system('twofing')

      QtCore.QCoreApplication.instance().quit()

   def home(self):
      self.motorRa.setTargetPulsePosition(0)
      self.motorDec.setTargetPulsePosition(0)
#      # The problem with what's below is that it cannot be stopped
#      # by clicking stop.
#      # wait to reach home position
#      while self.motorRa.getCurrentPulsePosition()<>0 or self.motorDec.getCurrentPulsePosition()<>0:
#         pass
#      # interrupt the tracking
#      self.btnTracking.setChecked(True)
#      self.defaultMode()

   def defaultMode(self):
      if self.btnTracking.isChecked(): 
         self.btnTracking.setStyleSheet("background-color : red") 
         self.btnTracking.setText("Tracking OFF")
         self.motorRa.setTargetPulseSpeed(0)
         self.motorDec.setTargetPulseSpeed(0)
      else: 
         self.btnTracking.setStyleSheet("background-color : lightgreen")
         self.btnTracking.setText("Tracking ON")
         self.motorRa.setTargetPulseSpeed(self.motorRa.pulseSpeedSiderealTracking)
         self.motorDec.setTargetPulseSpeed(0)


   def slewBtnPressed(self, direction):
      '''direction = 'raPlus', 'raMinus', 'decPlus', 'decMinus'
      '''
      #print 'button pressed!'
      #print direction
      if direction=='raPlus':
         self.motorRa.setTargetPulseSpeed(self.motorRa.maxPulseSpeed)
      elif direction=='raMinus':
         self.motorRa.setTargetPulseSpeed(-self.motorRa.maxPulseSpeed)
      elif direction=='decPlus':
         self.motorDec.setTargetPulseSpeed(self.motorDec.maxPulseSpeed)
      elif direction=='decMinus':
         self.motorDec.setTargetPulseSpeed(-self.motorDec.maxPulseSpeed)


   def slewBtnReleased(self, direction):
      '''direction = 'raPlus', 'raMinus', 'decPlus', 'decMinus'
      '''
      #print 'button released!'
      #print direction
#      if direction=='raPlus':
#         self.motorRa.setTargetPulseSpeed(0)
#      elif direction=='raMinus':
#         self.motorRa.setTargetPulseSpeed(0)
#      elif direction=='decPlus':
#         self.motorDec.setTargetPulseSpeed(0)
#      elif direction=='decMinus':
#         self.motorDec.setTargetPulseSpeed(0)
      self.defaultMode()



   def stop(self):
      '''Halts the motors, interrupt or not the tracking
      '''
      self.motorRa.halt()
      self.motorDec.halt()
      # interrupt the tracking
      self.btnTracking.setChecked(True)
      self.defaultMode()


   def shutter(self):
      '''Captures a photo, saves it to camera
      '''
      os.system('gphoto2 --capture-image')


   def testShot(self):
      '''Capture test photo and save it to raspberry pi
      to review it
      '''
      # Take a photo and save it to the Pi
      os.system('gphoto2 --capture-image-and-download --force-overwrite --filename '+self.pathTestShots+'test.jpg')
      # Show the image, so it can be reviewed
      os.system('feh --scale-down --image-bg "black" '+self.pathTestShots+'test.jpg')


   def cameraStartStop(self):
      '''Start/stop the timelapse,
      saving images to the camera
      '''
      if self.btnCameraStartStop.isChecked(): 
         self.btnCameraStartStop.setStyleSheet("background-color : red") 
         self.btnCameraStartStop.setText("Stop")

         # Start the timelapse
         self.subprocTimelapse = subprocess.Popen(['gphoto2', '--capture-image', '--interval', '5'])

      else: 
         self.btnCameraStartStop.setStyleSheet("background-color : lightgreen")
         self.btnCameraStartStop.setText("Start")

         # kill the timelapse, if it was started
         if hasattr(self,'subprocTimelapse'):
            self.subprocTimelapse.kill()


##############################################33
# Motor control


def ticcmd(*args):
   return subprocess.check_output(['ticcmd'] + list(args))

class Motor(object):

   def __init__(self, ticid, name):
      self.ticid = ticid
      self.name = name

      # gearbox * pinion-wheel  reduction factor
      # gearbox: 99. + 104./2057.
      # pinion-wheel: 84./20. = 4.2
      self.reductionFactor = (99.+104./2057.) * (84./20.)
      self.stepsPerRotation = 200.  # typical for stepper motors

      # settings
      self.current = 192   # [mA]
      self.microStepping = 16 # [pulses per step]
      #self.microStepping = 32 # [pulses per step]
      self.maxPulseSpeed = 300000000 #400000000 # [1.e-4 pulses/sec]
      self.maxPulseAccel = 4000000   # [1.e-2 pulses/sec^2]
      self.maxPulseDecel = 4000000   # [1.e-2 pulses/sec^2]

      # sidereal tracking pulse speed
      self.pulseSpeedSiderealTracking = self.computePulseSpeedTracking()  # [1.e-4 pulses/sec]

      # energize the motor
      ticcmd('-d', self.ticid, '--current', str(self.current))
      ticcmd('-d', self.ticid, '--energize')
      # disable safe start
      ticcmd('-d', self.ticid, '--exit-safe-start')
      # microstepping
      ticcmd('-d', self.ticid, '--step-mode', str(self.microStepping))
      # set max speed, acceleration, decay mode
      ticcmd('-d', self.ticid, '--max-speed', str(self.maxPulseSpeed))
      ticcmd('-d', self.ticid, '--max-accel', str(self.maxPulseAccel))
      ticcmd('-d', self.ticid, '--max-decel', str(self.maxPulseDecel))
      ticcmd('-d', self.ticid, '--decay', 'mixed50')

   def angle(self, pulse, unit='deg'):
      '''Convert pulse position to angular position
      '''
      result = pulse * 360.
      result /= self.microstepping * self.stepsPerRotation * self.reductionFactor
      if unit=='rad':
         result *= np.pi / 180.
      return result

   def pulse(self, angle, unit='deg'):
      '''Cinvert angular position to pulse position
      '''
      result = angle / 360.
      result *= self.microstepping * self.stepsPerRotation * self.reductionFactor
      if unit=='rad':
         result /= np.pi / 180.
      return result

   def computePulseSpeedTracking(self):
      '''result in [1,e-4 pulses/sec], as required by ticcmd
      '''
      siderealDay = 23.9344696 * 3600.   # [sec]
      result = self.stepsPerRotation * self.reductionFactor * self.microStepping # [pulses per sidereal day]
      result /= siderealDay  # [pulses/sec]
      result *= 1.e4 # [1.e-4 pulses/sec]
      return np.int(result)

   def getCurrentPulsePosition(self):
      status = yaml.load(ticcmd('-d', self.ticid, '-s', '--full'))
      position = status['Current position']
      print("Current "+self.name+" position is {}.".format(position))
      return position

   def getCurrentAngle(self):
      pulse = self.getCurrentPulsePosition()
      angle = self.angle(pulse)
      print("Current "+self.name+" angle is {} deg.".format(round(angle,4)))
      return position

   def deenergize(self):
      print("Deenergizing "+self.name+" motor")
      ticcmd('-d', self.ticid, '--deenergize')

   def halt(self):
      print("Halting "+self.name+" motor")
      ticcmd('-d', self.ticid, '--halt-and-hold')


   def setTargetPulsePosition(self, targetPosition):
      print("Setting target "+self.name+" position to {}.".format(targetPosition))
      ticcmd('-d', self.ticid, '--position', str(targetPosition))

   def setTargetPulseSpeed(self, targetSpeed):
      print("Setting target "+self.name+" speed to {}.".format(targetSpeed))
      ticcmd('-d', self.ticid, '--velocity', str(targetSpeed))



##############################################33


def run():
   # motors
   ticidRa = '00315338'
   ticidDec = '00315372'
   motorRa = Motor(ticidRa, 'RA')
   motorDec = Motor(ticidDec, 'Dec')

   # test initial position
   #print motorRa.getCurrentPulsePosition()
   #print motorDec.getCurrentPulsePosition()

   # gui
   app = QtGui.QApplication(sys.argv)
   GUI = Window(motorRa, motorDec)
   sys.exit(app.exec_())


run()
