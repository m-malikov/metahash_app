import subprocess
import time
import random
from pprint import pprint
import mhutils
import json
import serial

hub_address = mhutils.get_address("keys/hub.pub")
usb_input = serial.Serial('???', 9600)

while True:
    # data = json.dumps(
    #    {"temp": "22.5", "humidity": "100", "soil": "50"})
    data = usb_input.readline().decode('utf-8')
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
    time.sleep(5)
