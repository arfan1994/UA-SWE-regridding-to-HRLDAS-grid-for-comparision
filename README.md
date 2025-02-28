# UA-SWE-regridding-to-HRLDAS-grid-for-comparision
# UA SWE Regridding to HRLDAS Grid

This repository contains a Python script for regridding the **UA Snow Water Equivalent (SWE) dataset** onto the **HRLDAS 601x601 grid** using **nearest-neighbor interpolation**.

## 📌 Overview
- The **UA dataset** has latitude/longitude grids, while **HRLDAS SNEQV** is on a 601x601 structured grid.
- We **regrid UA SWE** onto the HRLDAS grid using **Scipy’s `griddata` interpolation**.
- The output is stored as **NetCDF** and can be used for direct comparison with HRLDAS SNEQV.
