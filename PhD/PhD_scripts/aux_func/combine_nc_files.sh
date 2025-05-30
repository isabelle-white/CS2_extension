#!/bin/bash

dir="/Users/iw2g24/PycharmProjects/CS2_extension/PhD/PhD_data/glo_L4_MY/5_year_blocks"
output="sla_1993_2024_glo.nc"

echo "Finding NetCDF files in $dir"
files=($(ls "$dir"/*.nc | sort))

echo "Preparing to concatenate ${#files[@]} files:"

# Echo each file before concatenation
for i in "${!files[@]}"; do
  echo "[$((i+1))/${#files[@]}] Adding file: ${files[$i]}"
done

echo "Concatenating files into $output..."

# Run ncrcat on all files
ncrcat "${files[@]}" "$output"

echo "Concatenation complete. Output saved to $output"

