import numpy
import pandas

from .. import _vroom


class Solution(_vroom.Solution):

    @property
    def routes(self) -> pandas.DataFrame:
        array = numpy.asarray(self._routes_numpy())
        frame = pandas.DataFrame({
            "vehicle_id": array["vehicle_id"],
            "job_id": array["job_id"],
            "task": array["task"].astype("U9"),
            "arrival": array["arrival"],
            "loc_index": array["loc_index"],
        })
        return frame
