#!/bin/bash

# Define geoid model name
geoid_name="eigen6s4v2_neg"

# Directories
latlon_dir="/Users/iw2g24/PycharmProjects/CS2_extension/PhD/PhD_data/altimetry_cpom/1_raw_nc_lonlat/"
geoid_grid="/Users/iw2g24/PycharmProjects/CS2_extension/PhD/PhD_data/geoid/${geoid_name}.nc"
output_dir="/Users/iw2g24/PycharmProjects/CS2_extension/PhD/PhD_data/geoid/geoid_${geoid_name}/"

echo "Starting geoid interpolation..."
echo "Reading lat/lon files from: $latlon_dir"
echo "Using geoid grid: $geoid_grid"
echo "Output directory: $output_dir"
echo "Geoid model: $geoid_name"
echo "--------------------------------------"

# Create output directory if it doesn't exist
mkdir -p "$output_dir"

# Process each lonlat text file
for file in "$latlon_dir"/*_lonlat.txt; do
    filename=$(basename "$file" _lonlat.txt)
    output_file="${output_dir}/${filename}_${geoid_name}.txt"

    echo "Processing file: $filename"
    gmt grdtrack "$file" -G"$geoid_grid" > "$output_file"

    if [ $? -eq 0 ]; then
        echo "Successfully created: $output_file"
    else
        echo "Error processing $filename"
    fi
done

echo "Geoid interpolation complete."

