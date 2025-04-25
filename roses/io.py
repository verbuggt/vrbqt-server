import json
import time

from roses.schemas import RoseOut

max_roses_perry = 100
max_roses_zoe = 150

max_age = 7 * 24 * 60 * 60  # 7 days in seconds


def open_file():
    return open("./.data/roses/roses.json", "r+")


def remove_old_roses(rose_list):
    now = time.time()
    for rose in rose_list:
        if now - rose['timestamp'] > max_age:
            rose_list.remove(rose)


def get_roses():
    file = open_file()
    rose_list = json.loads(file.read())["roses"]
    remove_old_roses(rose_list)

    write_file(file, rose_list)
    del file

    roses: list = []
    for json_rose in rose_list:
        roses.append(
            RoseOut(cat=json_rose["cat"],
                    timestamp=json_rose["timestamp"],
                    position=json_rose["position"],
                    size=json_rose["size"]))

    return roses


def write_file(file, rose_list: list):
    file.seek(0)
    file.truncate()
    file.write(json.dumps({"roses": rose_list}, indent=2))
    file.flush()
    file.close()


def add_rose(ip: str, timestamp: float, cat_name: str, rose_position: float, size: float):
    file = open_file()
    rose_list: list = json.loads(file.read())["roses"]
    remove_old_roses(rose_list)

    if len(rose_list) > (max_roses_perry if cat_name == "perry" else max_roses_zoe):
        return {"error": "total rose limit reached"}

    rose = RoseOut(cat=cat_name, timestamp=timestamp, position=rose_position, size=size)
    rose_list.append(rose.dict())

    write_file(file, rose_list)
    del file

    return rose
