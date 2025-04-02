from typing import Union
import numpy as np

import rasters as rt

from rasters import Raster

from .constants import GAMMA_HPA

def calculate_rootzone_moisture(
        delta_hPa: Union[Raster, np.ndarray], # Rate of change of saturation vapor pressure with temperature (hPa/°C)
        s1_hPa: Union[Raster, np.ndarray], # The slope of SVP at surface temperature (hPa/K)
        s3_hPa: Union[Raster, np.ndarray], # The slope of SVP at dewpoint temperature (hPa/K)
        ST_C: Union[Raster, np.ndarray], # surface temperature (°C)
        Ta_C: Union[Raster, np.ndarray], # air temperature (°C)
        dTS_C: Union[Raster, np.ndarray], # difference between surface and air temperature (°C)
        Td_C: Union[Raster, np.ndarray], # dewpoint temperature (°C)
        Tsd_C: Union[Raster, np.ndarray], # surface dewpoint temperature (°C)
        Rg_Wm2: Union[Raster, np.ndarray], # Incoming solar radiation (W/m^2)
        Rn_Wm2: Union[Raster, np.ndarray], # Net radiation (W/m^2)
        LWnet_Wm2: Union[Raster, np.ndarray], # Net longwave radiation (W/m^2)
        FVC: Union[Raster, np.ndarray], # Fractional vegetation cover (unitless)
        VPD_hPa: Union[Raster, np.ndarray], # Vapor pressure deficit (hPa)
        D0_hPa: Union[Raster, np.ndarray], # Vapor pressure deficit at source (hPa)
        SVP_hPa: Union[Raster, np.ndarray], # Saturation vapor pressure (hPa)
        Ea_hPa: Union[Raster, np.ndarray], # Actual vapor pressure (hPa)
        gamma_hPa: Union[Raster, np.ndarray, float] = GAMMA_HPA # Psychrometric constant (hPa/°C)
    ) -> Union[Raster, np.ndarray]:
    """
    Calculates the root zone moisture (Mrz) based on thermal IR and meteorological information.

    Args:
        delta (np.ndarray): Rate of change of saturation vapor pressure with temperature (kPa/°C).
        s1 (np.ndarray): The slope of saturation vapor pressure at surface temperature (hPa/K).
        s3 (np.ndarray): The slope of saturation vapor pressure at dewpoint temperature (hPa/K).
        ST_C (np.ndarray): Surface temperature in degrees Celsius.
        Ta_C (np.ndarray): Air temperature in degrees Celsius.
        dTS (np.ndarray): Difference between surface and air temperature in degrees Celsius.
        Td_C (np.ndarray): Dewpoint temperature in degrees Celsius.
        Tsd_C (np.ndarray): Surface dewpoint temperature in degrees Celsius.
        Rg (np.ndarray): Incoming solar radiation in W/m^2.
        Rn (np.ndarray): Net radiation in W/m^2.
        Lnet (np.ndarray): Net longwave radiation in W/m^2.
        fc (np.ndarray): Fractional vegetation cover (unitless).
        VPD_hPa (np.ndarray): Vapor pressure deficit in hPa.
        D0 (np.ndarray): Vapor pressure deficit at source in hPa.
        SVP_hPa (np.ndarray): Saturation vapor pressure in hPa.
        Ea_hPa (np.ndarray): Actual vapor pressure in hPa.

    Returns:
        np.ndarray: Root zone moisture (Mrz) (value 0 to 1).
    """
    s44 = (SVP_hPa - Ea_hPa) / (Ta_C - Td_C)
    kTSTD = (ST_C - Tsd_C) / (Ta_C - Td_C)
    Mrz = (gamma_hPa * s1_hPa * (Tsd_C - Td_C)) / (delta_hPa * s3_hPa * kTSTD * (ST_C - Td_C) + gamma_hPa * s44 * (Ta_C - Td_C) - delta_hPa * s1_hPa * (Tsd_C - Td_C))
    Mrz = rt.where((Rn_Wm2 < 0) & (dTS_C < 0) & (Mrz < 0), np.abs(Mrz), Mrz)
    Mrz = rt.where((Rn_Wm2 < 0) & (dTS_C > 0) & (Mrz < 0), np.abs(Mrz), Mrz)
    Mrz = rt.where((Rn_Wm2 > 0) & (dTS_C < 0) & (Mrz < 0), np.abs(Mrz), Mrz)
    Mrz = rt.where((Rn_Wm2 > 0) & (dTS_C > 0) & (Mrz < 0), np.abs(Mrz), Mrz)
    Mrz = rt.where((Rg_Wm2 > 0) & (Mrz < 0), np.abs(Mrz), Mrz)
    Mrz = rt.where((Rg_Wm2 < 0) & (Mrz < 0), np.abs(Mrz), Mrz)
    Mrz = rt.where((Td_C < 0) & (Mrz < 0), np.abs(Mrz), Mrz)
    Mrz = rt.where(Mrz > 1, 1, Mrz)
    Mrz = rt.where(Mrz < 0, 0.0001, Mrz)
    
    return Mrz