from typing import Union
import numpy as np

import rasters as rt
from rasters import Raster

def calculate_soil_heat_flux(
        seconds_of_day: Union[Raster, np.ndarray], 
        Rn: Union[Raster, np.ndarray], 
        SM: Union[Raster, np.ndarray]) -> Union[Raster, np.ndarray]:
    """
    This function calculates the soil heat flux (G) based on the method proposed by Santanello and Friedl (2003).
    The method estimates G as a function of time of day, net radiation (Rn), and soil moisture (SM).

    Parameters:
    seconds_of_day (np.ndarray): Time in seconds of the day since midnight
    Rn (np.ndarray): Net radiation in W/m^2
    SM (np.ndarray): Soil moisture in m^3/m^3

    Returns:
    G (np.ndarray): Soil heat flux in W/m^2

    Reference:
    Santanello, J. A., & Friedl, M. A. (2003). Diurnal covariation in soil heat flux and net radiation. Journal of Applied Meteorology, 42(6), 851-862.
    """

    # Constants for wet and dry surface conditions
    cgMIN = 0.05  # for wet surface
    cgMAX = 0.35  # for dry surface
    tgMIN = 74000  # for wet surface
    tgMAX = 100000  # for dry surface

    # Solar noon in seconds
    solNooN = 12 * 60 * 60
    tg0 = solNooN - seconds_of_day

    # Estimating soil heat flux (G) according to Santanello and Friedl (2003)
    cg = (1 - SM) * cgMAX + SM * cgMIN
    tg = (1 - SM) * tgMAX + SM * tgMIN

    G = Rn * cg * np.cos(2 * np.pi * (tg0 + 10800) / tg)

    # Adjusting G for negative net radiation
    G = rt.where(Rn < 0, -G, G)

    return G
