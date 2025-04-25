import json

import requests


data = {
    "dump_name": "ip",
    "dump_type": "plaintext",
    "dump_data": "",
}


def get_ip(v: int):
    if v not in [4, 6]:
        raise Exception("no.")

    url = f"https://ip{v}.me/api/"

    return ",".join(requests.get(url).text.split(",")[:2])


data['dump_data'] = "\n".join([get_ip(4), get_ip(6)])
print(requests.post("http://127.0.0.1:8000/api/dump/dump", data=json.dumps(data)).json())
