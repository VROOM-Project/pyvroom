"""Assert VROOM command line interface works as upstream."""
from pathlib import Path
import json
import subprocess

FOLDER = Path(__file__).parent.parent.resolve() / "vroom" / "docs"


def test_command_line_example_2():
    """Assert VROOM command line interface works as upstream."""

    process = subprocess.run(["vroom", "-i", FOLDER / "example_2.json"], stdout=subprocess.PIPE)
    output = json.loads(process.stdout)
    steps = [route["steps"] for route in output["routes"]]

    with (FOLDER / "example_2_sol.json").open() as src:
        reference = [route["steps"] for route in json.load(src)["routes"]]

    assert steps == reference
