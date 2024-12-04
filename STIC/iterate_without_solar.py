from typing import Union, Tuple
import numpy as np

import rasters as rt
from rasters import Raster

from .constants import *
from .canopy_air_stream import calculate_canopy_air_stream_vapor_pressure
from .root_zone_initialization import calculate_root_zone_moisture

def iterate_without_solar(
        LE: Union[Raster, np.ndarray],  # Latent heat flux (W/m^2)
        PET: Union[Raster, np.ndarray],  # Potential evapotranspiration (W/m^2)
        SM: Union[Raster, np.ndarray],
        ST_C: Union[Raster, np.ndarray],  # Surface temperature (°C)
        Ta_C: Union[Raster, np.ndarray],  # Air temperature (°C)
        dTS: Union[Raster, np.ndarray],  # Surface-air temperature difference (°C)
        T0: Union[Raster, np.ndarray],  # Reference temperature (°C)
        gB: Union[Raster, np.ndarray],  # Boundary layer conductance (m/s)
        gS: Union[Raster, np.ndarray],  # Stomatal conductance (m/s)
        Ea_hPa: Union[Raster, np.ndarray],  # Actual vapor pressure (hPa)
        Td_C: Union[Raster, np.ndarray],  # Dew point temperature (°C)
        VPD_hPa: Union[Raster, np.ndarray],  # Vapor pressure deficit (hPa)
        Estar: Union[Raster, np.ndarray],  # Saturation vapor pressure at surface temperature (hPa)
        delta: Union[Raster, np.ndarray],  # Slope of the saturation vapor pressure-temperature curve (hPa/°C)
        phi: Union[Raster, np.ndarray],  # available energy (W/m^2)
        Ds: Union[Raster, np.ndarray],  # Vapor pressure deficit at source (hPa)
        Es: Union[Raster, np.ndarray],  # Saturation vapor pressure (hPa)
        s3: Union[Raster, np.ndarray],  # Slope of the saturation vapor pressure and temperature 
        s4: Union[Raster, np.ndarray],  # Slope of the saturation vapor pressure and temperature 
        gB_by_gS: Union[Raster, np.ndarray],  # Ratio of boundary layer conductance to stomatal conductance
        gamma_hPa: Union[Raster, np.ndarray] = GAMMA_HPA,  # Psychrometric constant (hPa/°C)
        rho_kgm3: Union[Raster, np.ndarray] = RHO_KGM3,  # Air density (kg/m^3)
        Cp_Jkg: Union[Raster, np.ndarray] = CP_JKG,  # Specific heat at constant pressure (J/kg/K)
    ) -> Tuple[Union[Raster, np.ndarray]]:
    """
    Iterate STIC model without knowing solar radiation.

    Parameters:
    LE (np.ndarray): Latent heat flux (W/m^2)
    PET (np.ndarray): Potential evapotranspiration (W/m^2)
    ST_C (np.ndarray): Surface temperature (°C)
    Ta_C (np.ndarray): Air temperature (°C)
    dTS (np.ndarray): Surface-air temperature difference (°C)
    T0 (np.ndarray): Reference temperature (°C)
    gB (np.ndarray): Boundary layer conductance (m/s)
    gS (np.ndarray): Stomatal conductance (m/s)
    Ea_hPa (np.ndarray): Actual vapor pressure (hPa)
    Td_C (np.ndarray): Dew point temperature (°C)
    VPD_hPa (np.ndarray): Vapor pressure deficit (hPa)
    Estar (np.ndarray): Saturation vapor pressure at surface temperature (hPa)
    delta (np.ndarray): Slope of the saturation vapor pressure-temperature curve (hPa/°C)
    phi (np.ndarray): available energy (W/m^2)
    Ds (np.ndarray): Vapor pressure deficit at source (hPa)
    Es (np.ndarray): Saturation vapor pressure (hPa)
    s3 (np.ndarray): Slope of the saturation vapor pressure and temperature 
    s4 (np.ndarray): Soil moisture parameter
    gB_by_gS (np.ndarray): Ratio of boundary layer conductance to stomatal conductance
    gamma (np.ndarray): Psychrometric constant (hPa/°C)
    rho (np.ndarray): Air density (kg/m^3)
    cp (np.ndarray): Specific heat at constant pressure (J/kg/K)
    
    Returns:
    SM (np.ndarray): soil moisture (m³/m³)
    SMrz (np.ndarray): Root zone moisture (m³/m³)
    Ms (np.ndarray): Surface Moisture
    s1 (np.ndarray): lope of the saturation vapor pressure and temperature
    e0 (np.ndarray): Vapor pressure at the reference height (hPa)
    e0star (np.ndarray): Canopy air stream vapor pressures (hPa)
    Tsd_C (np.ndarray): Soil dew point temperature (°C)
    D0 (np.ndarray): Vapor pressure deficit at source (hPa)
    alphaN (np.ndarray): Alpha parameter
    """

    # canopy air stream vapor pressures
    e0star = calculate_canopy_air_stream_vapor_pressure(
        LE=LE, # latent heat flux (W/m^2)
        Ea_hPa=Ea_hPa, # actual vapor pressure (hPa)
        Estar=Estar, # saturation vapor pressure at surface temperature (hPa)
        gB=gB, # boundary layer conductance (m/s)
        gS=gS # stomatal conductance (m/s),
        
    )

    # vapor pressure deficit at source
    D0 = VPD_hPa + (delta * phi - (delta + gamma_hPa) * LE) / (rho_kgm3 * Cp_Jkg * gB)  
    D0 = rt.where(D0 < 0, Ds, D0)

    # Vapor pressure at the reference height (hPa)
    e0 = rt.clip(e0star - D0, Es, e0star)

    # re-estimating M (direct LST feedback into M computation)
    s1 = (45.03 + 3.014 * Td_C + 0.05345 * Td_C ** 2 + 0.00224 * Td_C ** 3) * 1e-2  # Soil moisture parameter
    Tsd_C = Td_C + (gamma_hPa * LE) / (rho_kgm3 * Cp_Jkg * gB * s1)  # Soil dew point temperature (°C)

    # Surface Moisture Ms
    Ms = rt.clip(s1 * (Tsd_C - Td_C) / (s3 * (ST_C - Td_C)), 0, 1)

    # Root zone moisture Mrz
    SMrz = calculate_root_zone_moisture(
        delta_hPa=delta,  # Slope of the saturation vapor pressure-temperature curve (hPa/°C)
        ST_C=ST_C,  # Surface temperature (°C)
        Ta_C=Ta_C,  # Air temperature (°C)
        Td_C=Td_C,  # Dew point temperature (°C)
        s11=s1,  # Soil moisture parameter
        s33=s3,  # Soil moisture parameter
        s44=s4,  # Soil moisture parameter
        Tsd_C=Tsd_C  # Soil dew point temperature (°C)
    )

    # combining hysteresis logic to differentiate surface vs. rootzone water control
    SM = rt.where((D0 > VPD_hPa) & (PET > phi) & (dTS > 0), SMrz, SM)
    SM = rt.where((phi > 0) & (dTS > 0) & (Td_C <= 0), SMrz, SM)
    SM = rt.clip(SM, 0, 1)

    # checking convergence
    # re-estimating alpha
    alphaN = ((gS * (e0star - Ea_hPa) * (2 * delta + 2 * gamma_hPa + gamma_hPa * gB_by_gS * (1 + SM))) / (
            2 * delta * (gamma_hPa * (T0 - Ta_C) * (gB + gS) + gS * (e0star - Ea_hPa))))

    return SM, SMrz, Ms, s1, e0, e0star, Tsd_C, D0, alphaN
