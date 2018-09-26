import subprocess
from fabulous.color import bold, blue, green
import time
import random

import mhutils

hub_address = mhutils.get_address("keys/hub.pub")

temp = 20

while True:
    temp += (random.random() - 0.5)
    print(bold("Current temperature:"), green("{:.1f}".format(temp)))

    transaction_result = subprocess.check_output([
        "python3",
        "metahash.py",
        "send-tx",
        "--net=test",
        "--pubkey=keys/temp.pub",
        "--privkey=keys/temp.priv",
        "--value=1",
        "--to={}".format(hub_address),
        '--data=' + "{:.1f}".format(temp)
    ]).decode("utf-8")
    print(transaction_result)
    time.sleep(5)
