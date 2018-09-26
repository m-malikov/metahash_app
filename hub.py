import subprocess
from fabulous.color import bold, blue, green
from flask import Flask
import time
from threading import Thread
import json

import mhutils

hub_address = mhutils.get_address("keys/hub.pub")
temp_address = mhutils.get_address("keys/temp.pub")
co_address = mhutils.get_address("keys/co.pub")
heater_adress = mhutils.get_address("keys/heater.pub")

temp = ""
heater = ""
co = ""


def update_values():
    global temp
    global co
    global heater
    history = mhutils.get_history(hub_address)
    temp = mhutils.get_last_data_from_address(history, temp_address)
    co = mhutils.get_last_data_from_address(history, co_address)
    heater = mhutils.get_last_data_from_address(history, heater_adress)


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


@app.route('/temp')
def get_temp():
    return temp


@app.route('/heater')
def get_heater():
    return heater


@app.route('/co')
def get_co():
    return co


app.run()
