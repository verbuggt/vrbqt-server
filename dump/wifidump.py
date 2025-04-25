import json
import os
import time

import requests

scan_result = ""
scans_run = 0
max_scans = 3
data = {
    "dump_name": "wifi",
    "dump_type": "plaintext",
    "dump_data": "",
}


def scan_wifi_list():
    global scan_result, scans_run
    scan_result = os.popen("nmcli device wifi rescan && nmcli device wifi list").read()
    scans_run += 1


def check_wifi():
    if max_scans <= scans_run:
        return

    scan_wifi_list()

    if "StrahlungToGo" not in scan_result:
        data['dump_data'] = scan_result
        print(requests.post("http://127.0.0.1:8000/api/dump/dump", data=json.dumps(data)).text)
        time.sleep(4)
        check_wifi()
    else:
        print(scan_result)
        print("at home, all good :)")


check_wifi()
