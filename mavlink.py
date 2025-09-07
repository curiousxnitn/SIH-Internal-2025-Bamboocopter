from pymavlink import mavutil
import time

master = mavutil.mavlink_connection('COM3', baud=115200)
print("Waiting for heartbeat...")
master.wait_heartbeat()
print(f"Connected to system {master.target_system} component {master.target_component}")

mode = 'GUIDED'
mode_id = master.mode_mapping()[mode]
master.mav.set_mode_send(master.target_system, mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED, mode_id)

print("Arming motors...")
master.mav.command_long_send(
    master.target_system,
    master.target_component,
    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
    0, 1, 0, 0, 0, 0, 0, 0
)

msg = None
while not msg:
    msg = master.recv_match(type='HEARTBEAT', blocking=True)
    if msg.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED:
        break
    time.sleep(1)

print("Taking off to 10 meters...")
master.mav.command_long_send(
    master.target_system,
    master.target_component,
    mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
    0, 0, 0, 0, 0, 0, 0, 10
)

time.sleep(10)

print("Landing...")
master.mav.command_long_send(
    master.target_system,
    master.target_component,
    mavutil.mavlink.MAV_CMD_NAV_LAND,
    0, 0, 0, 0, 0, 0, 0, 0
)

print("Mission complete.")
