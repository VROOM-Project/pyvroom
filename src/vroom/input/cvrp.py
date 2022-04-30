from typing import Any, Dict, Union
from pathlib import Path
import os
import re

from .benchmark import parse_node_coords, get_matrix

CVRP_FIELDS = [
    "NAME",
    "TYPE",
    "COMMENT",
    "DIMENSION",
    "EDGE_WEIGHT_TYPE",
    "CAPACITY",
    "VEHICLES",
]


def parse_cvrp(input: Union[str, Path]) -> Dict[str, Any]:
    """
    Read CVRP files.

    Args:
        input:

    Returns:

    Example:
        >>> content = '''NAME : A-n32-k5-demo
        ... COMMENT : (Augerat et al, No of trucks: 5, Optimal value: 784)
        ... TYPE : CVRP
        ... DIMENSION : 6
        ... EDGE_WEIGHT_TYPE : EUC_2D
        ... CAPACITY: 100
        ... NODE_COORD_SECTION
        ...  1 82 76
        ...  2 96 44
        ...  3 50 5
        ...  4 49 8
        ...  5 13 7
        ...  6 29 89
        ... DEMAND_SECTION
        ... 1 0
        ... 2 19
        ... 3 21
        ... 4 6
        ... 5 19
        ... 6 7
        ... DEPOT_SECTION
        ...  1
        ...  -1
        ... EOF'''
        >>> print(parse_cvrp(content))  # doctest: +NORMALIZE_WHITESPACE
        {'meta': {'NAME': 'A-n32-k5-demo',
                  'COMMENT': '(Augerat et al, No of trucks: 5, Optimal value: 784)',
                  'TYPE': 'CVRP',
                  'DIMENSION': 6,
                  'EDGE_WEIGHT_TYPE': 'EUC_2D',
                  'CAPACITY': 100},
         'vehicles': [{'id': 0, 'start': [82.0, 76.0], 'start_index': 0,
                       'end': [82.0, 76.0], 'end_index': 0, 'capacity': [100]}],
         'jobs': [{'id': 2, 'location': [96.0, 44.0], 'location_index': 1, 'amount': [19]},
                  {'id': 3, 'location': [50.0, 5.0], 'location_index': 2, 'amount': [21]},
                  {'id': 4, 'location': [49.0, 8.0], 'location_index': 3, 'amount': [6]},
                  {'id': 5, 'location': [13.0, 7.0], 'location_index': 4, 'amount': [19]},
                  {'id': 6, 'location': [29.0, 89.0], 'location_index': 5, 'amount': [7]}],
         'matrix': [[0, 35, 78, 76, 98, 55],
                    [35, 0, 60, 59, 91, 81],
                    [78, 60, 0, 3, 37, 87],
                    [76, 59, 3, 0, 36, 83],
                    [98, 91, 37, 36, 0, 84],
                    [55, 81, 87, 83, 84, 0]]}

    """
    if os.path.isfile(input):
        with open(input) as handle:
            input = handle.read()
    else:
        input = str(input)
    lines = input.split("\n")
    regex = rf"^\s*({'|'.join(CVRP_FIELDS)})\s*:\s*(.*?)\s*$"
    meta = {name: value for name, value in re.findall(regex, input, flags=re.M)}
    meta["DIMENSION"] = int(meta["DIMENSION"])
    meta["CAPACITY"] = int(meta["CAPACITY"])

    # Only support EUC_2D for now.
    if meta.get("EDGE_WEIGHT_TYPE", None) != "EUC_2D":
        raise ValueError("Unsupported EDGE_WEIGHT_TYPE; EUC_2D required.")

    # Find start of nodes descriptions.
    node_start = next((i for i, s in enumerate(lines) if s.startswith("NODE_COORD_SECTION")))

    # Defining all jobs.
    jobs = []
    coords = []

    for i in range(node_start + 1, node_start + 1 + meta["DIMENSION"]):
        coord_line = parse_node_coords(lines[i])

        if len(coord_line) < 3:
            # Reaching another section (like DEMAND_SECTION), happens when
            # only jobs are listed in NODE_COORD_SECTION but DIMENSION count
            # include jobs + depot.
            break

        coords.append([float(coord_line[1]), float(coord_line[2])])
        jobs.append(
            {
                "id": int(coord_line[0]),
                "location": [float(coord_line[1]), float(coord_line[2])],
                "location_index": i - node_start - 1,
            }
        )

    # Add all job demands.
    total_demand = 0
    demand_start = next((i for i, s in enumerate(lines) if s.startswith("DEMAND_SECTION")))
    for i in range(demand_start + 1, demand_start + 1 + meta["DIMENSION"]):
        demand_line = parse_node_coords(lines[i])

        if len(demand_line) < 2:
            # Same as above in job parsing.
            break

        job_id = int(demand_line[0])
        current_demand = int(demand_line[1])

        for j in jobs:
            # Add demand to relevant job.
            if j["id"] == job_id:
                j["amount"] = [current_demand]
                total_demand += current_demand
                break

    # Find depot description.
    depot_start = next((i for i, s in enumerate(lines) if s.startswith("DEPOT_SECTION")))

    depot_def = lines[depot_start + 1].strip().split(" ")
    if len(depot_def) == 2:
        # Depot coordinates are provided, we add them at the end of coords
        # list and remember their index.
        depot_loc = [float(depot_def[0]), float(depot_def[1])]
        depot_index = len(coords)
        coords.append(depot_loc)
    else:
        # Depot is one of the existing jobs, we retrieve loc and index in
        # coords, then remove the job.
        depot_id = int(depot_def[0])
        job_index = next((i for i, j in enumerate(jobs) if j["id"] == depot_id))
        depot_loc = jobs[job_index]["location"]
        depot_index = jobs[job_index]["location_index"]
        jobs.pop(job_index)

    matrix = get_matrix(coords)

    if "VEHICLES" in meta:
        meta["VEHICLES"] = int(meta["VEHICLES"])
        nb_vehicles = meta["VEHICLES"]
    else:
        nb_vehicles = int(1 + (total_demand / meta["CAPACITY"]))

    vehicles = []

    for i in range(nb_vehicles):
        vehicles.append(
            {
                "id": i,
                "start": depot_loc,
                "start_index": depot_index,
                "end": depot_loc,
                "end_index": depot_index,
                "capacity": [meta["CAPACITY"]],
            }
        )

    return {"meta": meta, "vehicles": vehicles, "jobs": jobs, "matrix": matrix}
