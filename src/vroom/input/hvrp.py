from typing import Any, Dict, Union
from pathlib import Path
import os
import json
import sys

from .benchmark import get_matrix

# Generate a json-formatted problem from a HVRP file.

# Those benchmarks use double precision for matrix costs and results
# are usually reported with 2 decimal places. As a workaround, we
# multiply all costs by CUSTOM_PRECISION before performing the usual
# integer rounding. Comparisons in benchmarks/compare_to_BKS.py are
# adjusted accordingly.
CUSTOM_PRECISION = 1000

FIRST_LINE = 5


def parse_hvrp(input: Union[str, Path]) -> Dict[str, Any]:
    if os.path.isfile(input):
        with open(input_file, "r") as f:
            input = f.read()
    lines = str(input).split()

    jobs, vehicle_types, _, _, lower_bound, bks = lines[FIRST_LINE].split()
    meta = {
        "JOBS": int(jobs),
        "VEHICLE_TYPES": int(vehicle_types),
        "LOWER_BOUND": float(lower_bound),
        "BKS": float(bks),
    }

    coords = []

    # # Useful to generate first draft for BKS file.
    # BKS = {
    #   input_file: {
    #     "class": "vfmp_v",
    #     "best_known_cost": meta['BKS'],
    #     "jobs": meta['JOBS'],
    #     "total_amount": 0,
    #     "total_capacity": 0,
    #     "vehicles": 0
    #   }
    # }

    # Handle depot and vehicles.
    depot_line = lines[FIRST_LINE + 1 + meta["VEHICLE_TYPES"]]
    coords.append([int(x) for x in depot_line.split()])

    vehicles = []

    for v_type in range(1, meta["VEHICLE_TYPES"] + 1):
        line = lines[FIRST_LINE + v_type]
        vehicle = line.split()

        v_number = int(vehicle[0])
        v_capacity = int(vehicle[1])
        v_fixed_cost = int(vehicle[2])
        v_du_cost = float(vehicle[3])

        # BKS[input_file]['vehicles'] += v_number
        # BKS[input_file]['total_capacity'] += v_number * v_capacity

        if v_fixed_cost != 0:
            # Not handled yet!
            print("Non-fixed cost!")
            exit(1)

        for n in range(v_number):
            vehicles.append(
                {
                    "id": v_type * 1000 + n,
                    "profile": "euc_2D",
                    "start": coords[0],
                    "start_index": 0,
                    "end": coords[0],
                    "end_index": 0,
                    "capacity": [v_capacity],
                    "speed_factor": 1 / v_du_cost,
                }
            )

    jobs = []

    jobs_start = FIRST_LINE + meta["VEHICLE_TYPES"] + 2

    for i, line in enumerate(lines[jobs_start : jobs_start + meta["JOBS"]]):

        customer = line.split()
        if len(customer) < 3:
            print("Too few columns in customer line.")
            exit(2)

        current_coords = [int(customer[0]), int(customer[1])]
        jobs.append(
            {
                "id": i,
                "location": current_coords,
                "location_index": len(coords),
                "delivery": [int(customer[2])],
            }
        )
        coords.append(current_coords)

    matrix = get_matrix(coords, CUSTOM_PRECISION)

    meta["VEHICLES"] = len(vehicles)

    # for n in range(len(jobs)):
    #   BKS[input_file]['total_amount'] += jobs[n]['delivery'][0]

    # # Uncomment to generate BKS file.
    # print(json.dumps(BKS))
    # exit(0)

    return {
        "meta": meta,
        "vehicles": vehicles,
        "jobs": jobs,
        "matrices": {"euc_2D": {"durations": matrix}},
    }


if __name__ == "__main__":
    input_file = sys.argv[1]
    instance_name = input_file[: input_file.rfind(".txt")]
    output_name = instance_name + ".json"

    print("- Writing problem " + input_file + " to " + output_name)
    json_input = parse_hvrp(input_file)

    json_input["meta"]["NAME"] = instance_name

    with open(output_name, "w") as out:
        json.dump(json_input, out)
