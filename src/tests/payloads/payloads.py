import json
import pathlib
from typing import Union

PAYLOADS_DIR = pathlib.Path(__file__).parent.absolute()


def load(filename: str) -> Union[dict, list]:
    with open(PAYLOADS_DIR / filename) as f:
        return json.load(f)
