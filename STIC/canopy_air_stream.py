from typing import Union
import numpy as np

import rasters as rt

from rasters import Raster

from .constants import *

def calculate_canopy_air_stream_vapor_pressure(
        LE: Union[Raster, np.ndarray],  # Latent heat flux [W/m^2]
        Ea_hPa: Union[Raster, np.ndarray],  # Actual vapor pressure [hPa]
        Estar: Union[Raster, np.ndarray],  # Saturation vapor pressure [hPa]
        gB: Union[Raster, np.ndarray],  # Conductance of boundary layer [mol/m^2/s]
        gS: Union[Raster, np.ndarray],  # Conductance of stomata [mol/m^2/s]
        rho_kgm3: Union[Raster, np.ndarray, float] = RHO_KGM3,  # Air density (kg/m^3)
        Cp_Jkg: Union[Raster, np.ndarray, float] = CP_JKG,  # Specific heat at constant pressure (J/kg/K)
        gamma_hPa: Union[Raster, np.ndarray, float] = GAMMA_HPA,  # Psychrometric constant (hPa/°C)
    ) -> Union[Raster, np.ndarray]:
    """
    Calculate the canopy air stream vapor pressure.

    Parameters:
        LE (Union[Raster, np.ndarray]): Latent heat flux [W/m^2]
        Ea_hPa (Union[Raster, np.ndarray]): Actual vapor pressure [hPa]
        Estar (Union[Raster, np.ndarray]): Saturation vapor pressure [hPa]
        gB (Union[Raster, np.ndarray]): Conductance of boundary layer [mol/m^2/s]
        gS (Union[Raster, np.ndarray]): Conductance of stomata [mol/m^2/s]

    Returns:
        Union[Raster, np.ndarray]: The calculated canopy air stream vapor pressure [hPa]
    """
    e0star = Ea_hPa + (gamma_hPa * LE * (gB + gS)) / (rho_kgm3 * Cp_Jkg * gB * gS)
    e0star = rt.where(e0star < 0, Estar, e0star)
    e0star = rt.where(e0star > 250, Estar, e0star)

    return e0star
