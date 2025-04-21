import json
from dataclasses import asdict, is_dataclass
from json import JSONEncoder
from typing import TextIO, Any


class DataClassJSONEncoder(JSONEncoder):
    def default(self, o):
        if is_dataclass(o):
            return asdict(o)
        return super().default(o)

