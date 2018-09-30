import subprocess
import time
import random
from pprint import pprint
import mhutils
import json
import serial

hub_address = mhutils.get_address("keys/hub.pub")
home_address = mhutils.get_address("keys/temp.pub")
usb_input = serial.Serial('/dev/ttyACM0', 9600)

while True:
    usb_input.flushInput()
    data = usb_input.readline().decode('utf-8')
    try:
        pprint(json.loads(data))
        transaction_result = subprocess.check_output([
            "python3",
            "metahash.py",
            "send-tx",
            "--net=test",
            "--pubkey=keys/temp.pub",
            "--privkey=keys/temp.priv",
            "--value=1",
            "--to={}".format(hub_address),
            '--data=' + data
        ]).decode("utf-8")
        print(transaction_result)
    except:
        print(data)

    history = mhutils.get_history(home_address)
    last_command = mhutils.get_last_data_from_address(history, hub_address)
    print(last_command)
    if last_command == 'LIGHT_ON':
        usb_input.write(b'A')
    elif last_command == 'LIGHT_OFF':
        usb_input.write(b'B')
    elif last_command == 'DOOR_OPEN':
        usb_input.write(b'C')
   elif last_command == 'DOOR_CLOSE':
        usb_input.write(b'D')
     
