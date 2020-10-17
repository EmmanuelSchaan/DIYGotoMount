import subprocess
import yaml


# my tic device number
tic1_id = '00315372'
#tic_ra = '00315372'
#tic_dec = '00315338'

def ticcmd(*args):
   return subprocess.check_output(['ticcmd'] + list(args))

status = yaml.load(ticcmd('-s', '--full'))

position = status['Current position']
print("Current position is {}.".format(position))


# energize the motor
ticcmd('-d', tic1_id, '--energize')
# disable safe start
ticcmd('-d', tic1_id, '--exit-safe-start')

# 1/16 microstepping
ticcmd('-d', tic1_id, '--step-mode', '16')
# set max speed, acceleration, decay mode
ticcmd('-d', tic1_id, '--max-speed', '400000000')
ticcmd('-d', tic1_id, '--max-accel', '4000000')
ticcmd('-d', tic1_id, '--max-decel', '4000000')
ticcmd('-d', tic1_id, '--decay', 'mixed50')




new_target = position + 50000
print("Setting target position to {}.".format(new_target))
#ticcmd('-d', tic1_id, '--exit-safe-start', '--position', str(new_target))
ticcmd('-d', tic1_id, '--position', str(new_target))





# deenergize the motor
#ticcmd('-d', tic1_id, '--deenergize')

