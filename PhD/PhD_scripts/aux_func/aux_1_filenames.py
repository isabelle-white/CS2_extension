"""
list with filenames of .nc files
(only contains data from 07.2002-03.2012 for ENV
and from 11.2010-10.2018 for CS2 - discarded some of the early months 
from CS2 due to low spatial converage)

Last modified: 28 Jan 2025
"""

# ENVISAT
# -----------------------------------------------------------------------------
yr_list = ['03', '04', '05', '06', '07', '08', '09', '10', '11']
month_list = ['01', '02', '03', '04', '05', '06',
              '07', '08', '09', '10', '11', '12']
id_list_mid = ['month'+yr_list[i] + month_list[j] for i in range(len(yr_list))
              for j in range(len(month_list))]
id_0 = ['0207', '0208', '0209', '0210', '0211', '0212']
id_1 = ['1201', '1202', '1203']
id_list_start = ['month' + id_0[i] for i in range(len(id_0))]
id_list_end = ['month' + id_1[i] for i in range(len(id_1))]
env_id_list = id_list_start + id_list_mid + id_list_end

# CS2
# -----------------------------------------------------------------------------
#yr_list = ['2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024']
# yr_list = ['2018', '2019', '2020', '2021', '2022', '2023', '2024']
# id_list_mid = [yr_list[i] + month_list[j] for i in range(len(yr_list)) for j in
#               range(len(month_list))]
# id_list_start = ['201011', '201012']
# id_list_end = ['201801', '201802', '201803', '201804', '201805',
#                '201806', '201807', '201808', '201809', '201810']
# id_list_type = ['_MERGE']
#
# cs2_id_list = [x + '_MERGE' for x in (id_list_start + id_list_mid + id_list_end)]
# #cs2_id_list = id_list_start + id_list_mid + id_list_end

# Define the year and month ranges
year_list = ['2018', '2019', '2020', '2021', '2022', '2023', '2024']
month_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

# Create a list for the months starting from November 2018 to December 2024
id_list_mid = [year_list[i] + month_list[j] for i in range(len(year_list)) for j in range(len(month_list))]

# Filter out dates starting from November 2018 to December 2024
id_list_mid = [x for x in id_list_mid if (x >= '201812' and x <= '202412')]

# Define the start and end lists (make sure 201811 appears only in the start list)
id_list_start = ['201811']  # Start from November 2018 (this will only appear once)
id_list_end = ['202409', '202410', '202411', '202412']  # End at December 2024

# Combine all the lists and add '_MERGE' suffix, ensuring no duplication
cs2_id_list = [x + '_MERGE' for x in (id_list_start + id_list_mid + id_list_end)]

# Print the resulting list to verify
print(cs2_id_list)


