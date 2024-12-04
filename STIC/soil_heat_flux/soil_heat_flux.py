from typing import Union
import numpy as np

import rasters as rt
from rasters import Raster

from .santanello import calculate_soil_heat_flux as santanello_G
from .SEBAL import calculate_soil_heat_flux as SEBAL_G

DEFAULT_G_METHOD = "santanello"

def calculate_soil_heat_flux(
        seconds_of_day: Union[Raster, np.ndarray] = None,
        ST_C: Union[Raster, np.ndarray] = None,
        NDVI: Union[Raster, np.ndarray] = None,
        albedo: Union[Raster, np.ndarray] = None,
        Rn: Union[Raster, np.ndarray] = None, 
        SM: Union[Raster, np.ndarray] = None, 
        method: str = DEFAULT_G_METHOD) -> Union[Raster, np.ndarray]:
    """
    The method estimates soil heat flux (G) as a function of time of day, net radiation (Rn), soil moisture (SM), 
    surface temperature (ST_C), Normalized Difference Vegetation Index (NDVI), and albedo. The method used for 
    calculation can be specified.

    Parameters:
    seconds_of_day (np.ndarray): Time in seconds of the day since midnight.
    ST_C (np.ndarray): Surface temperature in Celsius.
    NDVI (np.ndarray): Normalized Difference Vegetation Index.
    albedo (np.ndarray): Albedo of the surface.
    Rn (np.ndarray): Net radiation in W/m^2.
    SM (np.ndarray): Soil moisture in m^3/m^3.
    method (str, optional): Method to be used for calculation. Defaults to "santanello".

    Returns:
    G (np.ndarray): Soil heat flux in W/m^2.
    """

    # FIXME make sure G doesn't drop to extreme negative values

    if method == "santanello":
        G = santanello_G(
            seconds_of_day=seconds_of_day,
            Rn=Rn,
            SM=SM
        )
    elif method == "SEBAL":
        G = SEBAL_G(
            Rn=Rn,
            ST_C=ST_C,
            NDVI=NDVI,
            albedo=albedo
        )
    elif method == "MOD16":
        G = (-0.276 * NDVI + 0.35) * Rn
    elif method == "PTJPL":
        G = rt.clip(Rn * (0.05 + (1 - rt.clip(NDVI, 0, 1)) * 0.265), 0, 0.35 * Rn)
    else:
        raise ValueError(f"invalid soil heat flux method: {method}")
    
    G = rt.clip(G, 0, None)

    return G
