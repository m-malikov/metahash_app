import subprocess
from fabulous.color import bold, blue, green
import time
import requests
import random

import mhutils

hub_address = mhutils.get_address("keys/hub.pub")

co = 100

while True:
    co += int((random.random() - 0.5) * 10)
    print(bold("Current CO level:"), green(str(co)))

    transaction_result = subprocess.check_output([
        "python3",
        "metahash.py",
        "send-tx",
        "--net=test",
        "--pubkey=keys/co.pub",
        "--privkey=keys/co.priv",
        "--value=1",
        "--to={}".format(hub_address),
        '--data=' + str(co)
    ]).decode("utf-8")
    print(transaction_result)
    time.sleep(5)
