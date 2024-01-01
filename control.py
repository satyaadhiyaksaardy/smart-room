import argparse
import tinytuya
from yeelight import Bulb
from dotenv import load_dotenv
import os
import json

load_dotenv()

# Initialize the Tuya device
id = os.getenv('TUYA_DEVICE_ID')
ip = os.getenv('TUYA_DEVICE_IP')
key = os.getenv('TUYA_DEVICE_KEY')
threeSwitch = tinytuya.OutletDevice(id, ip, key)
threeSwitch.set_version(3.3)

# Initialize the IR Blaster device (for AC control)
ir_id = os.getenv('IR_DEVICE_ID')
ir_ip = os.getenv('IR_DEVICE_IP')
ir_key = os.getenv('IR_DEVICE_KEY')
ir_ac_on_remote_code = os.getenv('IR_AC_ON_REMOTE_CODE')
ir_ac_off_remote_code = os.getenv('IR_AC_OFF_REMOTE_CODE')
ir_blaster = tinytuya.OutletDevice(ir_id, ir_ip, ir_key)
ir_blaster.set_version(3.3)

# Initialize the Yeelight bulb
yeelight_ip = os.getenv('YEELIGHT_IP')
bulb = Bulb(yeelight_ip)

# Tuya switch control function
def switch_tuya(switch_number, state):
    if state == 'on':
        threeSwitch.set_value(switch_number, True)
    elif state == 'off':
        threeSwitch.set_value(switch_number, False)

# Yeelight mode functions
def ivory_mode():
    bulb.set_brightness(100)
    bulb.set_rgb(255, 255, 255)
    bulb.set_hsv(0, 0)
    bulb.set_color_temp(6500)

def warm_mode():
    bulb.set_brightness(71)
    bulb.set_rgb(255, 255, 255)
    bulb.set_hsv(0, 0)
    bulb.set_color_temp(2017)

# Function to switch Yeelight modes
def switch_yeelight(mode):
    if mode == "ivory":
        ivory_mode()
    elif mode == "warm":
        warm_mode()
    else:
        print("Unknown mode")

# Function to send IR command
def send_ir_command(command_name):
    # Define your IR command mappings
    ir_commands = {
        "on": ir_ac_on_remote_code,
        "off": ir_ac_off_remote_code
    }

    if command_name in ir_commands:
        command = {
            "control": "send_ir",
            "head": "",
            "key1": ir_commands[command_name],
            "type": 0,
            "delay": 300,
        }
        payload = ir_blaster.generate_payload(tinytuya.CONTROL, {"201": json.dumps(command)})
        ir_blaster.send(payload)
    else:
        print(f"Unknown IR command: {command_name}")

# Set up command line argument parsing
parser = argparse.ArgumentParser(description='Control Tuya switches and Yeelight bulb modes.')
parser.add_argument('--tuya_switch', type=int, choices=[1, 2, 3],
                    help='Tuya switch number to control (1, 2, or 3)')
parser.add_argument('--tuya_state', type=str, choices=['on', 'off'],
                    help='State to set the Tuya switch to (on or off)')
parser.add_argument('--yeelight_mode', type=str, choices=['ivory', 'warm'],
                    help='Yeelight mode to set (ivory or warm)')
parser.add_argument('--ac_command', type=str, choices=['on', 'off'],
                    help='AC command to send (on or off)')

# Parse the command line arguments
args = parser.parse_args()

# Execute based on provided arguments
if args.tuya_switch and args.tuya_state:
    switch_tuya(args.tuya_switch, args.tuya_state)
if args.yeelight_mode:
    switch_yeelight(args.yeelight_mode)
if args.ac_command:
    send_ir_command(args.ac_command)