import datetime
import time

DUMP_DIR = "dumps"


def dump(dump_type, dump_name, dump_data):

    if dump_type not in ["plaintext", "json", "file"]:
        return "error"

    file_ext = ""
    if dump_type == "plaintext":
        file_ext = "txt"
    elif dump_type == "json":
        file_ext = "json"
    elif dump_type == "file":
        file_ext = "file"

    if not dump_name:
        dump_name = "unnamed_dump"
    dump_name += f"_{datetime.date.today().isoformat()}_{time.time()}"

    dump_file = open(f"{DUMP_DIR}/{dump_name}.{file_ext}", "w")
    dump_file.write(dump_data)
    dump_file.flush()
    dump_file.close()

    del dump_file

    return "ok"
