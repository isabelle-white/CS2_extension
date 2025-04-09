import os
import shutil

# Define the base iCloud Drive path
icloud_path = "/Users/iw2g24/Library/Mobile Documents/com~apple~CloudDocs/Orchestra-CryData"

# Define subdirectories based on naming roots
categories = ["LRM", "SAR", "SARIN", "MERGE"]

# Ensure subdirectories exist
for category in categories:
    os.makedirs(os.path.join(icloud_path, category), exist_ok=True)

# Loop through files in Orchestra-CryData
for root, dirs, files in os.walk(icloud_path):
    for file in files:
        # Only process files that contain ".elev" (including .elev.Z, etc.)
        if ".elev" in file:
            # Determine the category based on file name
            if "SARIN" in file:
                category = "SARIN"
            elif "SAR" in file:  # Ensures SARIN files do not go here
                category = "SAR"
            elif "LRM" in file:
                category = "LRM"
            elif "MERGE" in file:
                category = "MERGE"
            else:
                continue  # Skip files that do not match any category

            # Define source and destination paths
            file_path = os.path.join(root, file)
            dest_path = os.path.join(icloud_path, category, file)

            # Move the file to the correct subdirectory
            if os.path.isfile(file_path):
                shutil.move(file_path, dest_path)
                print(f"Moved {file} to {category}/")


