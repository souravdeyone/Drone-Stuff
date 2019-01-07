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
    vehicle.flush()

    while True:
        print "Altitude: ", vehicle.location.global_relative_frame.alt

        #Break and return from function just below target altitude
        if vehicle.location.global_relative_frame.alt >= TargetAltitude*0.95:
            print "Reaached target altitude"
            break
        time.sleep(1)

##arm_and_takeoff(40)
##print "Take off complete"
##
###Travel to another coordinate for 50 seconds
##print "Going to 1st coordinate"
##vehicle.airspeed=3
##new_location = LocationGlobalRelative(-34.36227, 155.1667, 40)
##vehicle.simple_goto(new_location)
##time.sleep(20)
##print "Completed 1st coordinate"
##
###Travel to another coordinate for 50 seconds
##print "Going to 2nd coordinate"
##vehicle.airspeed=5
##new_location2 = LocationGlobalRelative(80.36227, 2.1667, 40)
##vehicle.simple_goto(new_location2)
##vehicle.flush()
##time.sleep(30)
##print "Completed 2nd coordinate"
##
###Travel to another coordinate for 50 seconds
##print "Going to 3rd coordinate"
##vehicle.airspeed=3
##new_location2 = LocationGlobalRelative(-80.36227, 62.1667, 40)
##vehicle.simple_goto(new_location2)
##vehicle.flush()
##time.sleep(30)
##print "Completed 3nd coordinate"
##
###Hover for 10 seconds
##print "Go into RTL"
##vehicle.mode = VehicleMode("RTL")
##vehicle.flush()
##
##print "RTL Complete"



arm_and_takeoff(10)

start = time.time()

print "Set default/target airspeed to 3"
vehicle.airspeed = 3

print "Going towards first point for 30 seconds ..."
point1 = LocationGlobalRelative(-35.361354, 149.165218, 20)
vehicle.simple_goto(point1)

# sleep so we can see the change in map
time.sleep(30)
first_time = time.time()-start
print(first_time)

print "Going towards second point for 30 seconds (groundspeed set to 10 m/s) ..."
point2 = LocationGlobalRelative(-35.363244, 149.168801, 20)
vehicle.simple_goto(point2, groundspeed=10)

# sleep so we can see the change in map
time.sleep(30)
second_time = time.time()-first_time-start
print(second_time)

print "Going towards third point for 30 seconds (groundspeed set to 2 m/s) ..."
point2 = LocationGlobalRelative(35.363244, 90.168801, 20)
vehicle.simple_goto(point2, groundspeed=2)

# sleep so we can see the change in map
time.sleep(30)
third_time = time.time()-second_time-first_time-start
print third_time


print "Returning to Launch"
vehicle.mode = VehicleMode("RTL")

#Close vehicle object before exiting script
print "Close vehicle object"
vehicle.close()


#Close vehicle object
vehicle.close()
