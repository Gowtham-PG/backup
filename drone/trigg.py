import time
from dronekit import connect, VehicleMode
import argparse
from pymavlink import mavutil

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
parser.add_argument('--connect', help="Vehicle connection target string. If not specified, SITL automatically started and used.")
args = parser.parse_args()

# Get the connection string from command-line arguments
connection_string = args.connect

sitl = None
vehicle = None

if not connection_string:
    import dronekit_sitl
    sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()

# Connect to the vehicle
print('Connecting to vehicle on: %s' % connection_string)
vehicle = connect(connection_string, wait_ready=True)
vehicle.mode = VehicleMode("GUIDED")

# Define the parameters for the MAV_CMD_DO_DIGICAM_CONTROL command
param1 = 0  # Shutter trigger (0: release, 1: focus and release)
param2 = 1  # Reserved (set to 0)
param3 = 0  # Reserved (set to 0)
param4 = 0  # Reserved (set to 0)
param5 = 1  # Reserved (set to 0)
param6 = 0  # Reserved (set to 0)
param7 = 0  # Reserved (set to 0)

# Send the MAV_CMD_DO_DIGICAM_CONTROL command
command = vehicle.message_factory.command_long_encode(
    0, 0,  # target_system, target_component
    mavutil.mavlink.MAV_CMD_DO_DIGICAM_CONTROL,  # command
    0,  # confirmation
    param1, param2, param3, param4, param5, param6, param7
)

# Send the command to the vehicle
vehicle.send_mavlink(command)

# Check if the command was successfully sent
if command:
    print("MAV_CMD_IMAGE_START_CAPTURE command sent successfully.")
else:
    print("Failed to send MAV_CMD_IMAGE_START_CAPTURE command.")

# Close the vehicle connection and sitl instance (if used)
if vehicle:
    vehicle.close()
if sitl:
    sitl.stop()
