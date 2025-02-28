import numpy as np
import xarray as xr
import scipy.interpolate

# Paths to NetCDF files
ua_file = "/glade/derecho/scratch/aarshad/ReffSnowData/UA_4km_SWE_Depth_WY2018_v01_WestUS_masked.nc"
wrfinput_file = "/glade/work/aarshad/CONUS404_data/wrfinput_d01.oct011979_WUS.nc"

# Load HRLDAS grid (601x601) from WRF input file
with xr.open_dataset(wrfinput_file) as wrf_ds:
    xlat_hrldas = wrf_ds["XLAT"][0, :, :]
    xlon_hrldas = wrf_ds["XLONG"][0, :, :]

# Load UA dataset
ua_ds = xr.open_dataset(ua_file)

# Extract lat, lon, and SWE from UA dataset
ua_lat = ua_ds["lat"].values
ua_lon = ua_ds["lon"].values
ua_swe = ua_ds["SWE"]  # SWE is 3D: (time, lat, lon)

# Create 2D coordinate grids for UA dataset
X_ua, Y_ua = np.meshgrid(ua_lon, ua_lat)

# Create 2D coordinate grids for HRLDAS dataset
X_hrldas, Y_hrldas = xlon_hrldas.values, xlat_hrldas.values

# Flatten UA SWE grid for interpolation
points_ua = np.vstack((X_ua.ravel(), Y_ua.ravel())).T

# Initialize an array to store regridded SWE data
swe_remapped = np.full((ua_swe.shape[0], 601, 601), np.nan)  # (time, 601, 601)

# Loop over each time step and interpolate
for t in range(ua_swe.shape[0]):
    values_ua = ua_swe[t, :, :].values.ravel()
    UA_interpolated = scipy.interpolate.griddata(points_ua, values_ua, (X_hrldas, Y_hrldas), method="nearest")
    swe_remapped[t, :, :] = UA_interpolated  # Store interpolated SWE at this time step

# Convert back to xarray DataArray
swe_regridded_xr = xr.DataArray(
    swe_remapped,
    dims=("time", "south_north", "west_east"),
    coords={"time": ua_ds["time"], "south_north": np.arange(601), "west_east": np.arange(601)},
    name="SWE_regridded",
    attrs={"units": "mm", "description": "UA SWE regridded to HRLDAS 601x601 grid"}
)

# Save regridded SWE dataset
output_path = "/glade/derecho/scratch/aarshad/ReffSnowData/UA_SWE_Regridded_to_HRLDAS.nc"
swe_regridded_xr.to_netcdf(output_path)
print(f"Regridded UA SWE saved at: {output_path}")
