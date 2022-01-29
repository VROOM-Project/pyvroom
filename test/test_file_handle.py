"""Assert VROOM command line interface works as upstream."""
from pathlib import Path
import json

import pytest

import vroom

_FOLDER = Path(__file__).parent.parent.resolve() / "vroom" / "docs"
INPUT_FILE = _FOLDER / "example_2.json"
OUTPUT_FILE = _FOLDER / "example_2_sol.json"


def assert_equal(solution, reference):
    del solution["summary"]["computing_times"]
    assert solution == reference


@pytest.fixture
def example_2_reference():
    with OUTPUT_FILE.open() as src:
        return json.load(src)


def test_console_script(example_2_reference, capsys):
    """Run VROOM console script entrypoint."""
    vroom.main(["vroom", "-i", str(INPUT_FILE)])
    output = json.loads(capsys.readouterr().out)
    assert_equal(output, example_2_reference)


def test_loader(example_2_reference):
    input = vroom.Input.from_json(INPUT_FILE)
    solution = input.solve(exploration_level=5, nb_threads=4)
    assert_equal(solution.to_dict(), example_2_reference)
