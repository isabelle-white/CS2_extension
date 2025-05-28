"""
coarsen the topography grid from GEBCO to match the altimetry resolution

Last modified: 16 Mar 2021
"""
import numpy as np

import xarray as xr

from scipy.interpolate import RegularGridInterpolator as rgi

import sys

# Directories
workdir = '/Users/iw2g24/PycharmProjects/CS2_extension/PhD/PhD_data/'
altdir = workdir + '/altimetry_cpom/3_grid_dot/'
lmdir = workdir + 'land_masks/'
topodir = workdir + 'topog/'

#-------------------------------------------------------------------
# bathymetry file
with xr.open_dataset(topodir + 'gebco_all.nc') as topo:
    print(topo.keys())

print("\n reading altimetry data..")
# --------------------------------------------------------
# altfile = #'insert_here_the_altimetry_file.nc'

altfile = '/dot_all_30bmedian_goco05c_sig3_1.nc'
print(altfile)

# with xr.open_dataset(altdir+altfile) as alt:
with xr.open_dataset(altdir+ altfile) as alt:
    print(alt.keys())

# topog grid only covers -50 to -78
# define the new grid within those bounds otherwise the interp fc complains
fc = rgi((topo.lon.values, topo.lat.values), topo.elevation.values.T)

# grid - lon goes from 0 to 360 in topog
alat = alt.latitude.sel(latitude=slice(topo.lat.min(), topo.lat.max())).values
alon = alt.longitude.values
alon[alon<0] = alon[alon<0] + 360

glat, glon = np.meshgrid(alat, alon)

# coarser topography
coarse_elev = fc((glon, glat))

# --------------------------------------------------------
# save coarser topog in a new file
coarse_topog = xr.Dataset({'elevation': (['lon', 'lat'], coarse_elev)},
                          coords={'lon': alon, 'lat': alat})
fname = 'coarse_gebco_p5x1_latlon_all_test_izzy.nc'
coarse_topog.to_netcdf(topodir+ fname)
print("File saved in %s as %s" % (topodir, fname))

##---------####
## THIS IS THE EDITED VERSION I CHANGED TO MAKE LAT AND LON MATCH TOPOG LIMITS - SEE WHAT OANA SAYS ABOUT WHICH ALT FILE TO USE!!!
#
# import numpy as np
# import xarray as xr
# from scipy.interpolate import RegularGridInterpolator as rgi
#
# # Directories
# workdir = '/Users/iw2g24/PycharmProjects/CS2_extension/PhD/PhD_data/'
# altdir = workdir + 'altimetry_cpom/1_raw_nc/'
# topodir = workdir + 'topog/'
#
# #-------------------------------------------------------------------
# # Load bathymetry (topography) dataset
# with xr.open_dataset(topodir + 'gebco_all.nc') as topo:
#     print(topo.keys())
#
#     # Create interpolation function for topo elevation
#     # Note topo.lon: 0 to 360; topo.lat as coords
#     fc = rgi((topo.lon.values, topo.lat.values), topo.elevation.values.T)
#
# print("\nReading altimetry data...")
# altfile = '/201012_MERGE.nc'
# with xr.open_dataset(altdir + altfile) as alt:
#     print(alt.keys())
#
#     # Extract latitude and longitude arrays from altimetry data variables (dimension: nrows)
#     lat_arr = alt['Latitude'].values
#     lon_arr = alt['Longitude'].values
#
#     # Define latitude limits from topo grid (assuming topo.lat is coordinate)
#     lat_min = topo.lat.min().values
#     lat_max = topo.lat.max().values
#
#     # Create mask to filter altimetry points within topo latitude bounds
#     mask = (lat_arr >= lat_min) & (lat_arr <= lat_max)
#
#     # Filter lat/lon arrays using mask
#     alat = lat_arr[mask]
#     alon = lon_arr[mask]
#
#     # Convert negative longitudes to 0-360 range for consistency with topo lon
#     alon = np.where(alon < 0, alon + 360, alon)
#
#     # Since altimetry points are irregularly spaced, create a regular lat/lon grid
#     # Define grid resolution (adjust these numbers as needed)
#     num_lon = 360  # e.g., 0.5 deg resolution: 360 points for 0-360
#     num_lat = 280  # e.g., covering topo lat range with ~0.25 deg spacing
#
#     glon_vals = np.linspace(topo.lon.min().values, topo.lon.max().values, num=num_lon)
#     glat_vals = np.linspace(topo.lat.min().values, topo.lat.max().values, num=num_lat)
#     glon, glat = np.meshgrid(glon_vals, glat_vals)
#
#     # Interpolate topo elevation onto this regular grid
#     coarse_elev = fc((glon, glat))
#
# # --------------------------------------------------------
# # Save coarser topography on new lat/lon grid
# coarse_topog = xr.Dataset(
#     {'elevation': (['lat', 'lon'], coarse_elev)},  # note: meshgrid defaults shape is (lat, lon)
#     coords={'lat': glat_vals, 'lon': glon_vals}
# )
# fname = 'coarse_gebco_p5x1_latlon_izzy.nc'
# coarse_topog.to_netcdf(topodir + fname)
# print(f"File saved in {topodir} as {fname}")
