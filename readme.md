# Smart Home Control Script
This script provides a command-line interface to control Tuya smart switches and Yeelight bulb modes. It offers an easy-to-use command-line interface for toggling switches and changing light modes, now with added support for BARDI devices, which are compatible through the TUYA IoT platform.

## Features
- Control Tuya smart switches (On/Off)
- Set Yeelight bulb to predefined modes (Ivory/Warm)
- Control AC/any device that support IR (Need to Learn the base64 string remote IR signal) (On/Off)
- Command-line interface for easy interaction
- Secure credential handling using environment variables

## Prerequisites
- Python 3.8
- `tinytuya` Python package
- `yeelight` Python package
- `python-dotenv` Python package

## Installation
Clone the repository:
```bash
git clone https://github.com/satyaadhiyaksaardy/room-control.git
cd room-control
```

Install the required packages:
```bash
pip install tinytuya yeelight python-dotenv
```

## Configuration
Create a .env file in the root directory of the project with the following content:
```.env
TUYA_DEVICE_ID=your_tuya_device_id
TUYA_DEVICE_IP=your_tuya_device_ip
TUYA_DEVICE_KEY=your_tuya_device_key
YEELIGHT_IP=your_yeelight_ip_address
IR_DEVICE_ID=your_tuya_ir_device_id
IR_DEVICE_IP=your_tuya_ir_device_ip
IR_DEVICE_KEY=your_tuya_ir_device_key
IR_AC_ON_REMOTE_CODE=your_remote_on_base64_string_ir_signal
IR_AC_OFF_REMOTE_CODE=your_remote_off_base64_string_ir_signal
```
Replace the placeholders with your actual device credentials.

## BARDI Device Integration
To control BARDI devices, which are built on the TUYA IoT platform, follow these steps:
1. **Install `tinytuya`** using the command provided in the Installation section.
2. **App Transition**: If you're using the BARDI app, switch to the Smart Life or Tuya Smart App on your smartphone.
3. **Device Reset**: Follow the device's manual to reset it, then pair it with the Smart Life or Tuya Smart app.
4. **Network Scan**: Run the following command to find your device on the network:
   `python -m tinytuya scan` 
   Take note of the device ID that appears.
5. **Developer Setup**: Register for a developer account on [Tuya IoT](https://iot.tuya.com/) and follow the "Setup Wizard" for getting your local keys.
6. **Link Apps**: Connect your Smart Life or Tuya Smart App account to your Tuya Developer Account.
7. **Run the Wizard**: Execute the `tinytuya` wizard with:
   `python -m tinytuya wizard` 
   When prompted, enter the API Key, secret, and device ID obtained from the previous steps.
  
The wizard will facilitate the retrieval of local keys and save them to a JSON file, which you can then use within the script for device control.

## Usage
To control your devices, run the script with the appropriate arguments:
```bash
python control.py --tuya_switch [1/2/3] --tuya_state [on/off]
python control.py --yeelight_mode [ivory/warm]
python control.py --ac_command [on/off]
```
Examples:
```bash
# Turn on Tuya switch 1
python control.py --tuya_switch 1 --tuya_state on
# Set Yeelight bulb to warm mode
python control.py --yeelight_mode warm
# Turn on AC
python control.py --ac_command on
# Combine command
python control.py --tuya_switch 2 --tuya_state on --yeelight_mode warm --ac_command off
```
With this setup, you can seamlessly integrate your BARDI devices alongside your Yeelight bulbs for a smarter and more connected home environment.
