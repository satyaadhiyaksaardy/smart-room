from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import tinytuya
import json

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Initialize Tuya Cloud connection
tuya = tinytuya.Cloud(
    apiRegion=os.getenv('TUYA_API_REGION', 'us'),
    apiKey=os.getenv('TUYA_API_KEY'),
    apiSecret=os.getenv('TUYA_API_SECRET')
)

# Device IDs from .env
SWITCH_ID = os.getenv('THREE_SWITCH_ID')
AIR_CONDITIONER_ID = os.getenv('AIR_CONDITIONER_ID')
API_TOKEN = os.getenv('API_TOKEN')
ir_ac_on_remote_code = os.getenv('IR_AC_ON_REMOTE_CODE')
ir_ac_off_remote_code = os.getenv('IR_AC_OFF_REMOTE_CODE')

# Endpoint for switch control
@app.route('/switch/<int:button>', methods=['POST'])
def control_switch(button):
    if request.headers.get('Authorization') != os.getenv('API_TOKEN'):
        return jsonify({'error': 'Unauthorized', 'token': request.headers.get('Authorization'), 'expected': os.getenv('API_TOKEN')}), 401

    if button not in [1, 2, 3]:
        return jsonify({'error': 'Invalid button number'}), 400

    # Extract on/off state from request
    data = request.get_json()
    state = data.get('state', False)  # Default to False if not specified

    commands = {"commands": [{"code": f"switch_{button}", "value": state}]}

    try:
        result = tuya.sendcommand(SWITCH_ID, commands)
        return jsonify({'result': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint for air conditioner control
@app.route('/air-conditioner', methods=['POST'])
def control_air_conditioner():
    if request.headers.get('Authorization') != os.getenv('API_TOKEN'):
        return jsonify({'error': 'Unauthorized'}), 401

    # Extract on/off state from request
    data = request.get_json()
    state = data.get('state', False)  # Use "True" to turn on, "False" to turn off

    # Determine command name based on state
    command_name = "on" if state else "off"

    # Map command name to IR codes
    ir_commands = {
        "on": ir_ac_on_remote_code,
        "off": ir_ac_off_remote_code
    }

    if command_name in ir_commands:
        # Prepare the IR command payload
        ir_cmd = {
            "control": "send_ir",
            "head": "",
            "key1": ir_commands[command_name],
            "type": 0,
            "delay": 300,
        }
        # Wrap the IR command for Tuya API
        commands = {"commands": [{"code": "ir_send", "value": json.dumps(ir_cmd)}]}
    else:
        return jsonify({'error': f"Unknown IR command: {command_name}"}), 400

    try:
        # Send the IR command through Tuya Cloud
        result = tuya.sendcommand(AIR_CONDITIONER_ID, commands)
        return jsonify({'result': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)