from typing import Union
import numpy as np

from rasters import Raster

from .constants import SB_SIGMA

def calculate_net_longwave_radiation(
        Ta_C: Union[Raster, np.ndarray], 
        Ea_hPa: Union[Raster, np.ndarray], 
        ST_C: Union[Raster, np.ndarray], 
        emissivity: Union[Raster, np.ndarray], 
        albedo: Union[Raster, np.ndarray],
        sigma: float = SB_SIGMA) -> Union[Raster, np.ndarray]:
    """
    Calculate the net radiation.

    Parameters:
    Ta_C (np.ndarray): Air temperature in Celsius
    Ea_hPa (np.ndarray): Actual vapor pressure at air temperature in hPa
    ST_C (np.ndarray): Surface temperature in Celsius
    emissivity (np.ndarray): Emissivity of the surface
    RG (np.ndarray): Global radiation
    albedo (np.ndarray): Albedo of the surface

    Returns:
    Lnet (np.ndarray): Net longwave radiation
    """
    etaa = 1.24 * (Ea_hPa / (Ta_C + 273.15)) ** (1.0 / 7.0)  # air emissivity
    LWin = sigma * etaa * (Ta_C + 273.15) ** 4
    LWout = sigma * emissivity * (ST_C + 273.15) ** 4
    
    # emissivity was being applied twice here
    # LWnet = emissivity * LWin - LWout
    
    LWnet = LWin - LWout

    return LWnet
