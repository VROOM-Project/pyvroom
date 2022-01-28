"""Assert VROOM command line interface works as upstream."""
from pathlib import Path
import json
import subprocess

import vroom

FOLDER = Path(__file__).parent.parent.resolve() / "vroom" / "docs"
COMMAND = ["vroom", "-i", str(FOLDER / "example_2.json")]


def test_command_line_example_2():
    """Assert VROOM command line interface works as upstream."""
    process = subprocess.run(COMMAND, stdout=subprocess.PIPE)
    output = json.loads(process.stdout)
    steps = [route["steps"] for route in output["routes"]]

    with (FOLDER / "example_2_sol.json").open() as src:
        reference = [route["steps"] for route in json.load(src)["routes"]]

    assert steps == reference


def test_command_line_example_2_smoke():
    """Run VROOM command line from with Python.

    Same as above, but exucuted from with Python.
    This makes stdout unavailable, but makes coverage available.
    """
    vroom.main(COMMAND)
