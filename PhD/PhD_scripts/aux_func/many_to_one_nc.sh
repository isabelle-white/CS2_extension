#!/bin/bash

echo "Starting NetCDF concatenation process..."

python3 <<EOF
import xarray as xr
import os

dir_name = "/Users/iw2g24/PycharmProjects/CS2_extension/PhD/PhD_data/glo_L4_MY/5_year_blocks"
print(f"Looking for NetCDF files in: {dir_name}")

# List and sort NetCDF files
nc_files = sorted([os.path.join(dir_name, f) for f in os.listdir(dir_name) if f.endswith(".nc")])

print(f"Found {len(nc_files)} files:")
for i, f in enumerate(nc_files, start=1):
    print(f"  [{i}/{len(nc_files)}] Loading file: {f}")

# Open datasets
datasets = [xr.open_dataset(f) for f in nc_files]

print("Concatenating datasets along 'time' dimension...")
combined = xr.concat(datasets, dim="time")

output_file = "sla_1993_2024_glo.nc"
combined.to_netcdf(output_file)
print(f"Concatenated dataset saved to {output_file}")
EOF

echo "Process completed."

