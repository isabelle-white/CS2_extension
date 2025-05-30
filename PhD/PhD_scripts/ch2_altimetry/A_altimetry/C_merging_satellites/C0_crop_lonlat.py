#c0
"""
Crop lon and lat from along-track altimetry and save coordinates in text files.
Then use GMT to interpolate the geoid at the along-track lon/lat.

Last modified: 31 March 2021
"""

import numpy as np
import xarray as xr

import sys

# Directories
workdir = '/Users/iw2g24/PycharmProjects/CS2_extension/PhD/PhD_data/'

altdir = workdir + 'altimetry_cpom/1_raw_nc/'
latlondir = workdir + 'altimetry_cpom/1_raw_nc_lonlat/'

scriptdir = '/Users/iw2g24/PycharmProjects/CS2_extension/PhD/PhD_scripts/'
auxscriptdir = scriptdir + 'scripts/aux_func/'

sys.path.append(auxscriptdir)
from aux_1_filenames import cs2_id_list, env_id_list


# Which satellite to process?
satellite = input("Which satellite? (env or cs2) ")
if satellite == 'env':
    id_list = env_id_list
elif satellite == 'cs2':
    id_list = cs2_id_list
else:
    print("Typo! Try again.")

itt = len(id_list)
print("Number of files: %s" % itt)

# for ii, suffix in zip(range(itt), id_list):
#     print("Extracting lat/lon from " + suffix + '.nc')
#     print('filenumber ', ii)
#     alt = xr.open_dataset(altdir+suffix+'.nc')
#     alt_lon = alt.Longitude.values
#     alt_lat = alt.Latitude.values
#
#     # save coordinates in a text file
#     data = np.vstack((alt_lon, alt_lat)).T
#
#     latlonfile = latlondir + suffix + '_lonlat.txt'
#     with open(latlonfile, 'w+') as output:
#         np.savetxt(output, data, fmt=['%.2f', '%.2f'])

for ii, suffix in zip(range(itt), id_list):
    print("Extracting lat/lon from " + suffix + '.nc')
    print('filenumber ', ii)

    filepath = altdir + suffix + '.nc'

    try:
        ds = xr.open_dataset(filepath)

        required_vars = ['Latitude', 'Longitude']
        if not all(var in ds.variables for var in required_vars) or ds.sizes == {}:
            print(f"{suffix}.nc is empty or missing required variables.")
            continue

        alt_lon = ds.Longitude.values
        alt_lat = ds.Latitude.values

    except FileNotFoundError:
        print(f"{suffix}.nc not found.")
        continue

    except Exception as e:
        print(f"Error reading {suffix}.nc: {e}")
        continue

    # Save coordinates in a text file
    data = np.vstack((alt_lon, alt_lat)).T
    latlonfile = latlondir + suffix + '_lonlat.txt'

    with open(latlonfile, 'w+') as output:
        np.savetxt(output, data, fmt=['%.2f', '%.2f'])

sys.exit()

# # BELOW: Too many points to use interpolation functions in python - use GMT instead

# from scipy import interpolate
# from netCDF4 import Dataset, num2date

# # GEOID
# geoiddir = workdir + 'geoid/'
# #geoidfile = 'egm2008.nc'
# geoidfile = 'goco05c.nc'

# gd = Dataset(geoiddir + geoidfile, 'r+')
# gd_lat = gd.variables['lat'][:]
# gd_lon = gd.variables['lon'][:]
# gd_height = gd.variables['geoid'][:]
# gd.close()

# gd_lon_grid, gd_lat_grid = np.meshgrid(gd_lon, gd_lat)
# alt_lon_grid, alt_lat_grid = np.meshgrid(alt_lon, alt_lat)
# # GEOID
# # interpolate the geoid to the SSH lat/lon
# gd_height_interp = interpolate.griddata((gd_lat, gd_lon_grid.flatten()),
#                                         gd_height.flatten(),
#                                         (alt_lat_grid.flatten(),
#                                          alt_lon_grid.flatten()))
