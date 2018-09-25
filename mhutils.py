import subprocess
import json


def get_address(pubkey):
    return subprocess.check_output([
        "bash",
        "metahash.sh",
        "get-address",
        "--net=test",
        "--pubkey=" + pubkey,
    ]).decode("utf-8").split()[-1]


def get_history(address):
    return json.loads(
        subprocess.check_output([
            "python3",
            "metahash.py",
            "fetch-history",
            "--net=test",
            "--address=" + address
        ]).decode("utf-8")
    )["result"]


def get_last_data_from_address(history, address):
    transactions = filter(lambda x: x["from"] == address, history)
    last_transaction = max(transactions, key=lambda x: x["timestamp"])
    return bytes.fromhex(last_transaction["data"]).decode('utf-8')
