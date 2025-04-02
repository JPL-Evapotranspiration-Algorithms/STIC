from typing import Union
from os.path import join
from datetime import date
import numpy as np
import logging

import colored_logging as cl
from rasters import Raster

logger = logging.getLogger(__name__)

def diagnostic(values: Union[Raster, np.ndarray], variable: str, show_distributions: bool = True, output_directory: str = None):
    if isinstance(values, Raster) and output_directory is not None:
        filename = join(output_directory, f"{variable}.tif")
        logger.info(filename)
        values.to_geotiff(filename)

    if show_distributions:
        unique = np.unique(values)
        nan_proportion = np.count_nonzero(np.isnan(values)) / np.size(values)

        if len(unique) < 10:
            logger.info(f"variable {cl.name(variable)} ({values.dtype}) has {cl.val(unique)} unique values")

            for value in unique:
                if np.isnan(value):
                    count = np.count_nonzero(np.isnan(values))
                else:
                    count = np.count_nonzero(values == value)

                if value == 0 or np.isnan(value):
                    logger.info(f"* {cl.colored(value, 'red')}: {cl.colored(count, 'red')}")
                else:
                    logger.info(f"* {cl.val(value)}: {cl.val(count)}")
        else:
            minimum = np.nanmin(values)

            if minimum < 0:
                minimum_string = cl.colored(f"{minimum:0.3f}", "red")
            else:
                minimum_string = cl.val(f"{minimum:0.3f}")

            maximum = np.nanmax(values)

            if maximum <= 0:
                maximum_string = cl.colored(f"{maximum:0.3f}", "red")
            else:
                maximum_string = cl.val(f"{maximum:0.3f}")

            if nan_proportion > 0.5:
                nan_proportion_string = cl.colored(f"{(nan_proportion * 100):0.2f}%", "yellow")
            elif nan_proportion == 1:
                nan_proportion_string = cl.colored(f"{(nan_proportion * 100):0.2f}%", "red")
            else:
                nan_proportion_string = cl.val(f"{(nan_proportion * 100):0.2f}%")

            message = "variable " + cl.name(variable) + \
                " min: " + minimum_string + \
                " mean: " + cl.val(f"{np.nanmean(values):0.3f}") + \
                " max: " + maximum_string + \
                " nan: " + nan_proportion_string

            if np.all(values == 0):
                message += " all zeros"
                logger.warning(message)
            else:
                logger.info(message)

        if nan_proportion == 1:
            raise ValueError(f"variable {variable} is blank")
