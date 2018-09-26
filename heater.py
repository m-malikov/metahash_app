import subprocess
from fabulous.color import bold, blue, green
import time
import random

import mhutils

hub_address = mhutils.get_address("keys/hub.pub")
temp_address = mhutils.get_address("keys/temp.pub")

heater_is_on = False

while True:
    last_temp = mhutils.get_last_data_from_address(
        mhutils.get_history(hub_address), temp_address)
    print(bold("Current temperature:"), green(
        bold(last_temp)))

    if heater_is_on != (float(last_temp) < 20):
        heater_is_on = float(last_temp) < 20
        print(heater_is_on)

        transaction_result = subprocess.check_output([
            "python3",
            "metahash.py",
            "send-tx",
            "--net=test",
            "--pubkey=keys/heater.pub",
            "--privkey=keys/heater.priv",
            "--value=1",
            "--to={}".format(hub_address),
            '--data=' + str(heater_is_on)
        ]).decode("utf-8")
        print(transaction_result)
    time.sleep(5)
