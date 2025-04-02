from typing import Union
import numpy as np

import rasters as rt
from rasters import Raster

from .constants import GAMMA_HPA

def calculate_root_zone_moisture(
        delta_hPa: Union[Raster, np.ndarray],
        ST_C: Union[Raster, np.ndarray], 
        Ta_C: Union[Raster, np.ndarray], 
        Td_C: Union[Raster, np.ndarray], 
        s11: Union[Raster, np.ndarray], 
        s33: Union[Raster, np.ndarray], 
        s44: Union[Raster, np.ndarray], 
        Tsd_C: Union[Raster, np.ndarray],
        gamma_hPa: Union[Raster, np.ndarray, float] = GAMMA_HPA) -> Union[Raster, np.ndarray]:
    """
    This function calculates the rootzone moisture (Mrz) using various parameters.

    Parameters:
    delta (np.ndarray): Rate of change of saturation vapor pressure with temperature (hPa/°C)
    ST_C (np.ndarray): Surface temperature (°C)
    Ta_C (np.ndarray): Air temperature (°C)
    Td_C (np.ndarray): Dewpoint temperature (°C)
    s11 (np.ndarray): The slope of SVP at dewpoint temperature (hPa/K)
    s33 (np.ndarray): The slope of SVP at surface temperature (hPa/K)
    s44 (np.ndarray): The difference between saturation vapor pressure and actual vapor pressure divided by the difference between air temperature and dewpoint temperature (hPa/K)
    Tsd_C (np.ndarray): The surface dewpoint temperature (°C)

    Returns:
    SMrz (np.ndarray): The rootzone moisture (m³/m³)
    """
    return rt.clip((gamma_hPa * s11 * (Tsd_C - Td_C)) / (delta_hPa * s33 * (ST_C - Td_C) + gamma_hPa * s44 * (Ta_C - Td_C) - delta_hPa * s11 * (Tsd_C - Td_C)), 0.0001, 0.999)
    