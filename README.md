# Surface Temperature Initiated Closure (STIC) Evapotranspiration Model Python Implementation

This repository contains the python implementation for the Surface Temperature Initiated Closure (STIC) evapotranspiration model, used by the ECOsystem Spaceborne Thermal Radiometer Experiment on Space Station (ECOSTRESS) and Surface Biology and Geology (SBG) missions.

Gregory H. Halverson (they/them)<br>
[gregory.h.halverson@jpl.nasa.gov](mailto:gregory.h.halverson@jpl.nasa.gov)<br>
Lead developer<br>
NASA Jet Propulsion Laboratory 329G

Kaniska Mallick (he/him)<br>
[kaniska.mallick@list.lu](mailto:kaniska.mallick@list.lu)<br>
Algorithm inventor<br>
Luxembourg Institute of Science and Technology

Tian Hu (he/him)<br>
[tian.hu@list.lu](mailto:tian.hu@list.lu)<br>
Algorithm developer<br>
Luxembourg Institute of Science and Technology

Madeleine Pascolini-Campbell (she/her)<br>
[madeleine.a.pascolini-campbell@jpl.nasa.gov](mailto:madeleine.a.pascolini-campbell@jpl.nasa.gov)<br>
Algorithm developer<br>
NASA Jet Propulsion Laboratory 329F

Claire Villanueva-Weeks (she/her)<br>
[claire.s.villanueva-weeks@jpl.nasa.gov](mailto:claire.s.villanueva-weeks@jpl.nasa.gov)<br>
Code maintenance<br>
NASA Jet Propulsion Laboratory 329G

### Abstract

This software package is a Python implementation of the Surface Temperature Initiated Closure (STIC) version 1.3 model designed to implement LST to solve the aerodynamic temperature, which is critical for ET modeling. The original STIC model produced by Kaniska Mallick (Mallick et al. 2015; 2018; 2022) was re-implemented from MATLAB code to Python by Gregory Halverson and Madeleine Pascolini-Campbell. The software was developed under a research grant by the NASA Research Opportunities in Space and Earth Sciences (ROSES) program. It is intended for use by the Hyperspectral Thermal Emission Spectrometer (HyTES), MODIS/ASTER (MASTER) Airborne Simulator, Ecosystem Spaceborne Thermal Radiometer Experiment on Space Station (ECOSTRESS) mission and as a precursor for the Surface Biology and Geology (SBG) mission. 

The software was developed as part of a research grant by the NASA Research Opportunities in Space and Earth Sciences (ROSES) program. It was designed for use by the Hyperspectral Thermal Emission Spectrometer (HyTES), MODIS/ASTER (MASTER) Airborne Simulator, Ecosystem Spaceborne Thermal Radiometer Experiment on Space Station (ECOSTRESS) mission as a precursor for the Surface Biology and Geology (SBG) mission. It may also be useful for general remote sensing and GIS projects in Python. This package can be utilized for remote sensing research in Jupyter notebooks and deployed for operations in data processing pipelines.
 
The software is being released according to the SPD-41 open-science requirements of NASA-funded ROSES projects.
 
Mallick, K., Boegh, E., Trebs, I., Alfieri, J. G., Kustas, W. P., Prueger, J. H., ... & Jarvis, A. J. (2015). Reintroducing radiometric surface temperature into the P enman‐M onteith formulation. Water Resources Research, 51(8), 6214-6243. https://doi.org/10.1002/2014WR016106 

Mallick, K., Toivonen, E., Trebs, I., Boegh, E., Cleverly, J., Eamus, D., ... & Garcia, M. (2018). Bridging Thermal Infrared Sensing and Physically‐Based Evapotranspiration Modeling: From Theoretical Implementation to Validation Across an Aridity Gradient in Australian Ecosystems. Water Resources Research, 54(5), 3409-3435. https://doi.org/10.1029/2017WR021357

Mallick, K., Baldocchi, D., Jarvis, A., Hu, T., Trebs, I., Sulis, M., ... & Kustas, W. P. (2022). Insights Into the Aerodynamic Versus Radiometric Surface Temperature Debate in Thermal‐Based Evaporation Modeling. Geophysical Research Letters, 49(15), e2021GL097568. https://doi.org/10.1029/2021GL097568

### This software accomplishes the following:

This software package is the python implementation of the Surface Temperature Initiated Closure (STIC) model of evapotranspiration.

### What are the unique features of the software?

- processing remote sensing data with the STIC model in python

### What improvements have been made over existing similar software application?

This python package was re-implemented in python by Gregory Halverson and Madeleine Pascolini-Campbell based on MATLAB code produced by Kaniska Mallick.

### What problems are you trying to solve in the software?

This software makes the STIC evapotranspiration model accessible for remote sensing researchers.

### Does your work relate to current or future NASA (include reimbursable) work that has value to the conduct of aeronautical and space activities?  If so, please explain:

This software package was developed as part of a research grant by the NASA Research Opportunities in Space and Earth Sciences (ROSES) program. This software was designed for use by the Hyperspectral Thermal Emission Spectrometer (HyTES),  MODIS/ASTER (MASTER) Airborne Simulator, and Ecosystem Spaceborne Thermal Radiometer Experiment on Space Station (ECOSTRESS) mission as a precursor for the Surface Biology and Geology (SBG) mission, but it may be useful generally for thermal remote sensing missions. It may also be useful generally for remote sensing and GIS projects in python.

### What advantages does this software have over existing software?

This software can be utilized for remote sensing research in Jupyter notebooks and deployed for operations in data processing pipelines.

### Are there any known commercial applications? What are they? What else is currently on the market that is similar?

This software is useful for both remote sensing data analysis and building remote sensing data pipelines.

### Is anyone interested in the software? Who? Please list organization names and contact information.

- NASA ROSES
- ECOSTRESS
- SBG

### What are the current hardware and operating system requirements to run the software? (Platform, RAM requirement, special equipment, etc.) 

This software is written entirely in python and intended to be distributed using the pip package manager.

### How has the software performed in tests? Describe further testing if planned. 

This software has been deployed for HyTES, ECOSTRESS and ET-Toolbox.

### Please identify the customer(s) and sponsors(s) outside of your section that requested and are using your software. 

This package is being released according to the SPD-41 open-science requirements of NASA-funded ROSES projects.

## Installation

Use the pip package manager to install this package

```
pip install .
```
