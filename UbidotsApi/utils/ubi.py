import time
import requests
import math
import random

TOKEN = "BBFF-b8rGQmXyxLHG0PtQkmCXPsFq9CdxcD"  # Put your TOKEN here
DEVICE_LABEL = "demo"  # Put your device label here 
#VARIABLE_LABEL_1 = "objects"  # Put your first variable label here

def build_payload(variable_1, clases, fecha, ubicacion):
    texto = "Se detectaron: "
    texto += "" + clases[0] + " Cascos,"
    texto += " " + clases[1] + " Guantes,"
    texto += " " + clases[2] + " Chalecos,"
    texto += " " + clases[3] + " Gafas. Entre " + fecha[0] + " y " + fecha[1] + ". Ubicada en: " + ubicacion
    payload = {variable_1: {"value": 1, "context": {"":texto}}}

    return payload


def post_request(payload):
    # Creates the headers for the HTTP requests
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1

    # Processes results
    if status >= 400:
        #print("[ERROR] Could not send data after 5 attempts, please check \
        #    your token credentials and internet connection")
        return False

    print("[INFO] request made properly, your device is updated")
    return True


def start(VARIABLE_LABEL_1, clases, fecha, ubicacion):
    payload = build_payload(
        VARIABLE_LABEL_1, clases, fecha, ubicacion)

    print("[INFO] Attemping to send data")
    post_request(payload)
    print("[INFO] finished")