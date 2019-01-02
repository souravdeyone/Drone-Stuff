from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal
from pymavlink import mavutil
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--connect', default='127.0.0.1:14550')
args = parser.parse_args()

armAndTakeoff = False

#Connect to the vehicle
print 'Connecting to the vehicle on %s' %args.connect
vehicle = connect(args.connect, baud=57600, wait_ready=True)

def arm_and_takeoff(TargetAltitude):

    print "Basic pre-arm checks"
    #Dont let user try to arm until autopilot is ready
    while not vehicle.is_armable:
        print "Waiting for vehicle to initialize..."
        time.sleep(1)

  
    print "Arming motors"
    #Copter should now be set to guided mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:
        print "Waiting for Arming..."
        time.sleep(1)

    print "Taking off!"
    vehicle.simple_takeoff(TargetAltitude)

    while True:
        print "Altitude: ", vehicle.location.global_relative_frame.alt
        #Break and return from function just below target altitude
        if vehicle.location.global_relative_frame.alt >= TargetAltitude*0.95:
            print "Reaached target altitude"
            break
        time.sleep(1)

arm_and_takeoff(10)
print "Take off complete"

#Travel to another coordinate for 50 seconds
print "Going to another coordinate"
new_location = LocationGlobal(-34.36227, 155.1667, 40)
vehicle.simple_goto(new_location)
time.sleep(50)


#Travel to another coordinate for 50 seconds
print "Going to another coordinate"
new_location = LocationGlobal(-80.36227, 62.1667, 40)
vehicle.simple_goto(new_location)
time.sleep(50)


#Hover for 10 seconds
vehicle.mode = VehicleMode("LOITER")
print "Hovering for 10 seconds"
time.sleep(10)

#Start landing prodecure
print("Now lets land")
vehicle.mode = VehicleMode("LAND")


#Close vehicle object
vehicle.close()
