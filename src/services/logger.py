import sys
import json
from loguru import logger as log


def serialize(record):
    try:
        subset = {
            "timestamp": record["time"].isoformat(),
            "level": record["level"].name,
            "message": record["message"],
            "source": f"{record['file']}:{record['function']}:{record['line']}",
        }
        if record["extra"]:
            subset["error"] = str(record["extra"]["extra"])

        return json.dumps(subset)
    except Exception as e:
        print(e)


def patching(record):
    try:
        record["extra"]["serialized"] = serialize(record)
    except Exception as e:
        pass


log.remove()
logger = log.patch(patching)
log.add(sys.stdout, backtrace=False, format="{extra[serialized]}", catch=False)
