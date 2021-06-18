import numpy as np

import subprocess
import yaml
from time import sleep

import sys
import os
from PyQt4 import QtGui, QtCore



##############################################33
# Camera settings: Canon EOS 550D (=T2i)

dictIso = {
   0: 'Auto',
   1: '100',
   2: '200',
   3: '400',
   4: '800',
   5: '1600',
   6: '3200',
   7: '6400',
   }

dictExposure = {
   0: 'bulb',
   1: '30',
   2: '25',
   3: '20',
   4: '15',
   5: '13',
   6: '10',
   7: '8',
   8: '6',
   9: '5',
   10: '4',
   11: '3.2',
   12: '2.5',
   13: '2',
   14: '1.6',
   15: '1.3',
   16: '1',
   17: '0.8',
   18: '0.6',
   19: '0.5',
   20: '0.4',
   21: '0.3',
   22: '1/4',
   23: '1/5',
   24: '1/6',
   25: '1/8',
   26: '1/10',
   27: '1/13',
   28: '1/15',
   29: '1/20',
   30: '1/25',
   31: '1/30',
   32: '1/40',
   33: '1/50',
   34: '1/60',
   35: '1/80',
   36: '1/100',
   37: '1/125',
   38: '1/160',
   39: '1/200',
   40: '1/250',
   41: '1/320',
   42: '1/400',
   43: '1/500',
   44: '1/640',
   45: '1/800',
   46: '1/1000',
   47: '1/1250',
   48: '1/1600',
   49: '1/2000',
   50: '1/2500',
   51: '1/3200',
   52: '1/4000',
}






##############################################33
# GUI


class Window(QtGui.QMainWindow):

   def __init__(self, motorRa, motorDec):
      
      # First, disable the two-finger right click daemon,
      # it messes up with the python gui
      os.system('killall twofing')

      super(Window, self).__init__()
      self.setGeometry(0, 66, 520, 400)
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

      # Initialize camera settings
      # set ISO and shutter speed
      self.iso()
      self.exposure()
      # make sure the photos are saved to the camera SD card, not just to its RAM
      os.system('gphoto2 --set-config /main/settings/capturetarget=1')


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
      self.btnRaMinus.move(125,50)

      # RA plus
      self.btnRaPlus = QtGui.QPushButton("RA+", self)
      #self.btnRaPlus.clicked.connect(self.increaseRa)
      self.btnRaPlus.pressed.connect(lambda : self.slewBtnPressed('raPlus'))
      self.btnRaPlus.released.connect(lambda : self.slewBtnReleased('raPlus'))
      self.btnRaPlus.resize(50,50)
      self.btnRaPlus.move(225,50)

      # Dec minus
      self.btnDecMinus = QtGui.QPushButton("Dec-", self)
      #self.btnDecMinus.clicked.connect(self.decreaseDec)
      self.btnDecMinus.pressed.connect(lambda : self.slewBtnPressed('decMinus'))
      self.btnDecMinus.released.connect(lambda : self.slewBtnReleased('decMinus'))
      self.btnDecMinus.resize(50,50)
      self.btnDecMinus.move(175,100)

      # Dec plus
      self.btnDecPlus = QtGui.QPushButton("Dec+", self)
      #self.btnDecPlus.clicked.connect(self.increaseDec)
      self.btnDecPlus.pressed.connect(lambda : self.slewBtnPressed('decPlus'))
      self.btnDecPlus.released.connect(lambda : self.slewBtnReleased('decPlus'))
      self.btnDecPlus.resize(50,50)
      self.btnDecPlus.move(175,0)

      # Stop
      self.btnStop = QtGui.QPushButton("Stop", self)
      self.btnStop.clicked.connect(self.stop)
      self.btnStop.resize(50,50)
      self.btnStop.move(175,50)

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
      self.btnShutter.move(300,0)

      # Test shot
      self.btnTestShot = QtGui.QPushButton("Test shot", self)
      self.btnTestShot.clicked.connect(self.testShot)
      self.btnTestShot.resize(100,50)
      self.btnTestShot.move(300,50)

      # Camera start/stop
      self.btnCameraStartStop = QtGui.QPushButton("Start", self)
      self.btnCameraStartStop.setCheckable(True)
      self.btnCameraStartStop.setStyleSheet("background-color : lightgreen")
      self.btnCameraStartStop.clicked.connect(self.cameraStartStop)
      self.btnCameraStartStop.resize(100,50)
      self.btnCameraStartStop.move(300,300)
      
      # ISO
      self.cbbxIso = QtGui.QComboBox(self)
      for i in range(len(dictIso.keys())):
         self.cbbxIso.addItem(dictIso[i])
      self.cbbxIso.currentIndexChanged.connect(self.iso)
      self.cbbxIso.resize(100,50)
      self.cbbxIso.move(300,100)
      # label
      self.labelIso = QtGui.QLabel("ISO", self)
      self.labelIso.resize(50,50)
      self.labelIso.move(250,100)


      # Exposure in sec
      self.cbbxExposure = QtGui.QComboBox(self)
      for i in range(len(dictExposure.keys())):
         self.cbbxExposure.addItem(dictExposure[i])
      self.cbbxExposure.currentIndexChanged.connect(self.exposure)
      self.cbbxExposure.resize(100,50)
      self.cbbxExposure.move(300,150)
      # label
      self.labelExposure = QtGui.QLabel("Exp (s)", self)
      self.labelExposure.resize(50,50)
      self.labelExposure.move(250,150)

      # Long exposure in sec, if bulb mode 
      self.spbxBulbExposure = QtGui.QSpinBox(self)
      self.spbxBulbExposure.setRange(30, 3600)
      self.spbxBulbExposure.setSingleStep(10)
      self.spbxBulbExposure.resize(65,50)
      self.spbxBulbExposure.move(335,200)
      # label
      self.labelInterval = QtGui.QLabel("Bulb Exp (s)", self)
      self.labelInterval.resize(85,50)
      self.labelInterval.move(250,200)


      # Interval for timelapse in sec
      self.spbxInterval = QtGui.QSpinBox(self)
      #self.spbxInterval.setMinimum(0)
      #self.spbxInterval.setMaximum(10000)
      #self.spbxInterval.valueChanged.connect(self.interval)
      self.spbxInterval.resize(100,50)
      self.spbxInterval.move(300,250)
      # label
      self.labelInterval = QtGui.QLabel("Int (s)", self)
      self.labelInterval.resize(50,50)
      self.labelInterval.move(250,250)

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
      # if not in bulb mode
      if self.cbbxExposure.currentIndex()<>0:
         # Take a photo
         os.system('gphoto2 --capture-image')
      # else in bulb mode
      else:
         # read the long exposure time
         exposure = self.spbxBulbExposure.value()
         # Hold the shutter down for the requested amount of time
         os.system("gphoto2 --set-config /main/actions/eosremoterelease=2 --wait-event="+str(exposure)+"s")


   def testShot(self):
      '''Capture test photo and save it to raspberry pi
      to review it
      '''
      # if not in bulb mode
      if self.cbbxExposure.currentIndex()<>0:
         # Take a photo and save it to the Pi
         os.system('gphoto2 --capture-image-and-download --keep --force-overwrite --filename '+self.pathTestShots+'test.jpg')
      # else in bulb mode
      else:
         # read the long exposure time
         exposure = self.spbxBulbExposure.value()
         # Hold the shutter down for the requested amount of time
         os.system("gphoto2 --set-config /main/actions/eosremoterelease=2 --wait-event="+str(exposure)+"s")
         # Once the exposure is written on camera, download to Pi
         os.system("gphoto2 --keep --wait-event-and-download=FILEADDED --force-overwrite --filename "+self.pathTestShots+"test.jpg")
      # Show the image, so it can be reviewed
      os.system('feh --scale-down --image-bg "black" '+self.pathTestShots+'test.jpg')


   def cameraStartStop(self):
      '''Start/stop the timelapse,
      saving images to the camera
      '''
      if self.btnCameraStartStop.isChecked(): 
         self.btnCameraStartStop.setStyleSheet("background-color : red") 
         self.btnCameraStartStop.setText("Stop")

         # read the timelapse interval in sec
         interval = self.spbxInterval.value()
         print("Starting timelapse: interval = "+str(interval)+" sec")
         # Start the timelapse

         # if not in bulb mode
         if self.cbbxExposure.currentIndex()<>0:
            # use timelapse function of gphoto2
            self.subprocTimelapse = subprocess.Popen('gphoto2 --capture-image --interval '+str(interval), shell=True)

         # else in bulb mode
         else:
            # read the long exposure time
            exposure = self.spbxBulbExposure.value()
            # do a manual loop for the timelapse
            self.subprocTimelapse = subprocess.Popen("""while :
                  do
                  gphoto2 --set-config /main/actions/eosremoterelease=2 --wait-event="""+str(exposure)+"""s
                  sleep """+str(max(0, interval-exposure))+"""
                  done""", shell=True)

      else: 
         self.btnCameraStartStop.setStyleSheet("background-color : lightgreen")
         self.btnCameraStartStop.setText("Start")
         # kill the timelapse, if it was started
         print("Stopping timelapse")
         # kill the exposure if it's in progress
         os.system('killall gphoto2')
         # stop the manual loop, if in bulb mode, so we don't start another exposure
         if hasattr(self,'subprocTimelapse'):
            self.subprocTimelapse.kill()


   def iso(self):
      '''Set the ISO on the camera
      '''
      isoIndex = self.cbbxIso.currentIndex()
      print("Setting ISO to "+dictIso[isoIndex]+" (choice "+str(isoIndex)+")")
      os.system('gphoto2 --set-config /main/imgsettings/iso='+str(isoIndex))
#      subprocess.Popen('gphoto2 --set-config /main/imgsettings/iso='+str(isoIndex), shell=True)


   def exposure(self):
      '''Set the Shutter speed on the camera
      '''
      exposureIndex = self.cbbxExposure.currentIndex()
      print("Setting Shutter to "+dictExposure[exposureIndex]+" (choice "+str(exposureIndex)+")")
      os.system('gphoto2 --set-config /main/capturesettings/shutterspeed='+str(exposureIndex))
#      subprocess.Popen('gphoto2 --set-config /main/capturesettings/shutterspeed='+str(exposureIndex), shell=True)


   def interval(self):
      pass

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
