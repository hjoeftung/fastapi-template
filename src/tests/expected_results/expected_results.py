import json
import pathlib
from typing import Union

EXPECTED_RESULTS_DIR = pathlib.Path(__file__).parent.absolute()


def load(filename: str) -> Union[dict, list]:
    with open(EXPECTED_RESULTS_DIR / filename) as f:
        return json.load(f)
