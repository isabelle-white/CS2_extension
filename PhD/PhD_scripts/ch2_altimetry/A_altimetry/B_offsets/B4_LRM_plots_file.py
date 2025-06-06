"""
Analyse the LRM/SAR(In) offset variability

Last modified: 31 Mar 2021
"""

## Import modules
import numpy as np
from numpy import ma

import matplotlib.pyplot as plt

import xarray as xr
import pandas as pd

import sys

#-------------------------------------------------------------------
# Define directories
#-------------------------------------------------------------------
voldir = '/Users/iw2g24/PycharmProjects/CS2_extension/PhD/PhD_data/'
ncdir = voldir + 'altimetry_cpom/1_raw_nc/'
bindir = voldir + 'altimetry_cpom/2_grid_offset/'
lmdir = voldir + 'land_masks/'

scriptdir = '/Users/iw2g24/PycharmProjects/CS2_extension/PhD/PhD_scripts/'
auxscriptdir = scriptdir + 'aux_func/'

sys.path.append(auxscriptdir)
# import aux_func_trend as ft
import aux_func as ft

#-------------------------------------------------------
# bin edges
edges_lon = np.linspace(-180, 180, num=361, endpoint=True)
edges_lat = np.linspace(-82, -50, num=65, endpoint=True)
eglat, eglon = np.meshgrid(edges_lat, edges_lon)

total_area = ft.grid_area(eglon, eglat)
#-------------------------------------------------------

def mclim(statistic, n_thresh):
    print("- - - - - - - - - - - - - - ")
    print("> > bin statistic: %s" % statistic)
    print("> > bin threshold: %s" % str(n_thresh))
    print("- - - - - - - - - - - - - - \n")

    #------------------------------------------------------------------
    filename = 'b04_bin_ssha_LRM_cs2_' + statistic + '.nc'
    print("File: %s" % filename)

    with xr.open_dataset(bindir + filename) as bin0:
        print(bin0.keys)

    #------------------------------------------------------------------
    # OFFSET computation
    #------------------------------------------------------------------
    # discard bins with fewer points than a certain threshold
    bin0.ssha_lrm.values[bin0.npts_lrm<n_thresh] = np.nan
    bin0.ssha_sar.values[bin0.npts_sar<n_thresh] = np.nan

    # subtract leads from ocean
    offset = (bin0.ssha_lrm - bin0.ssha_sar).transpose('longitude', 'latitude', 'time')
    offset.values[bin0.land_mask==1] = np.nan
    offset = offset.to_dataset(name='lrm_dif')

    # create weights based on the surface area of each bin
    ones = np.ones(offset.lrm_dif.shape)
    ones[np.isnan(offset.lrm_dif.values)] = 0
    arr_area = total_area[:,:, np.newaxis]*ones

    # normalize weights
    sum_area = arr_area.sum(axis=(0,1))
    norm_area = arr_area/sum_area

    offset['weights'] = (('longitude', 'latitude', 'time'), norm_area)

    #- - - - - - - - - - - - - -
    print(offset.keys())
    #- - - - - - - - - - - - - -

    # > > a. area weighted mean and StDev for every month
    # results are the same as my implementation of the weighted avg
    weighted_obj = offset.lrm_dif.weighted(offset.weights)
    monthly_off_weighted = weighted_obj.mean(('longitude', 'latitude'))

    monthly_res_sq = (offset.lrm_dif - monthly_off_weighted)**2
    weighted_obj_res_sq = monthly_res_sq.weighted(offset.weights)
    monthly_variance_weighted = weighted_obj_res_sq.mean(('longitude', 'latitude'))
    monthly_std_weighted = np.sqrt(monthly_variance_weighted)

    # a. climatology of monthly area-weighted mean offset
    monthly_off_clim = monthly_off_weighted.groupby('time.month').mean('time')

    # TWO ways to compute StDev!!! ????
    #monthly_off_clim_std = monthly_std_weighted.groupby('time.month').mean('time')
    monthly_off_clim_std = monthly_off_weighted.groupby('time.month').std('time')

    ds = xr.Dataset({'lrm_dif' : ('month', monthly_off_clim.values),
        'lrm_std' : ('month', monthly_off_clim_std.values)},
        coords={'month' : np.arange(1,13)})

    newfile = 'b04_LRM_offset_cs2_' + str(n_thresh) + statistic +'.nc'
    file_path = bindir + newfile

    if os.path.exists(file_path):
        print("File %s already exists" % newfile)
    else:
        ds.to_netcdf(file_path)
        print("File %s created" % newfile)


    return ds

#-------------------------------------------------------
mean_lrm = mclim('mean', 30)
median_lrm = mclim('median', 30)


xtim = mean_lrm.month.values
fig, ax = plt.subplots(figsize=(7,3))

ax.plot(xtim,
        mean_lrm.lrm_dif.values*1e2,
        c='k', marker='o', markersize=4,
        label='bin mean')
ax.errorbar(xtim,
            mean_lrm.lrm_dif.values*1e2,
            yerr=mean_lrm.lrm_std.values*1e2,
            capsize=3, ecolor='k',
            color='none', lw=1.)
ax.plot(xtim,
       median_lrm.lrm_dif.values*1e2,
       c='coral', marker='o', markersize=4,
       label='bin median')
ax.errorbar(xtim,
           median_lrm.lrm_dif.values*1e2,
           yerr=median_lrm.lrm_std.values*1e2,
           capsize=3, ecolor='coral',
           color='none', lw=1.)

ax.set_xticks(xtim, minor=True)
ax.grid(True, which='major', lw=1., ls='-')
ax.grid(True, which='minor', lw=1., ls=':')
ax.set_ylabel("LRM/SAR offset CS2 (cm)")
ax.axhline(0, ls=':', c='k')
ax.legend()
plt.tight_layout()
plt.show()
