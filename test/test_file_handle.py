"""Assert VROOM command line interface works as upstream."""
from pathlib import Path
import json

import pytest

import vroom

FOLDER = Path(__file__).parent.parent.resolve() / "vroom" / "docs"
COMMAND = ["vroom", "-i", str(FOLDER / "example_2.json")]


@pytest.fixture
def example_2_reference():
    with (FOLDER / "example_2_sol.json").open() as src:
        return [route["steps"] for route in json.load(src)["routes"]]


def test_console_script(example_2_reference, capsys):
    """Run VROOM console script entrypoint."""
    vroom.main(COMMAND)
    output = json.loads(capsys.readouterr().out)
    assert [route["steps"] for route in output["routes"]] == example_2_reference
