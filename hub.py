import subprocess
from fabulous.color import bold, blue, green
from flask import Flask
import time
from threading import Thread
import json

import mhutils

hub_address = mhutils.get_address("keys/hub.pub")
home_address = mhutils.get_address("keys/temp.pub")

data = ""


def update_values():
    global data
    history = mhutils.get_history(hub_address)
    data = mhutils.get_last_data_from_address(history, home_address)


def background():
    while True:
        update_values()
        time.sleep(1)


Thread(target=background).start()


app = Flask(__name__, static_url_path='')
app.__static_folder = 'static'


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/get_data')
def get_data():
    return data


app.run()
