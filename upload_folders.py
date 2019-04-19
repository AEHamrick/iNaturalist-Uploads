# -*- coding: utf-8 -*-
"""
This script uploads all photos in a folder to iNaturalist. It requires that
all photos are in a subfolder with the common or scientific name and/or the 
taxon number. 

Examples of acceptable folders to hold the individual photos in are:

.../main_folder/52381-Aphididae
.../main_folder/52381
.../main_folder/Aphididae 52381
.../main_folder/Aphids

All photos in any of those folders would be uploaded to a separate observation.

To upload multiple photos to an individual observation put those photos in a
subfolder. For example all photos in:

.../main_folder/52381/New Folder
would be uploaded to a single observation.

Dates, times, gps coordinates are taken from exif data. 

After upload the photos are moved to a folder 'Uploaded' in the same directory
as the main photo. The folder remains in place in case it will be used in 
future observations.
"""
# TODO: Break these elements out into functions and add a __main__
# TODO: Move the above explanation out of docstring and into readme
# TODO: Expand documentation and docstrings
# TODO: oAuth/API access method
# TODO: Logging
# TODO: Consistent-ize use of pathlib.Path over string paths
# TODO: Pick lat/long from Exif or GPX based on parameter or GUI checkbox
# TODO: Implement docopt and map out what things we want to be args and options
# TODO: Figure out how to run from either GUI or command line

# os used to get a folder name
import os
import pathlib
# This requires the file import_function.py to be in the same folder as this
# script
from import_functions import upload_folder_single, upload_folder_multiple, \
                             has_donefile, nearest_datetime, get_date
from classes import Observation
# This requires the file import_gui.py to be in the same folder as this
# script.
from import_gui import input_data
from gpx import parse_gpx
print("Running")

# Pulls the data from the gui when the script is run. 
[user, passw, app, secret, 
 folder_name, time_zone, accuracy] = input_data()


print('Uploading all photos in folders contained in ' + folder_name )

directories = []
observations = []
'''Expected structure
Base dir
 |
 - GPX companion file dir
 |
 - Taxon dir 1
   |
   - Photo 1
   - Photo 2
   - ...
   - Photo n
 |  
 - Taxon dir 2
   |
   - Obs dir 1
     |
     - Photo 1
     - Photo 2
     - ...
     - Photo n
   - Obs dir 2

'''

base_dir = folder_name
taxon_dirs = [pathlib.Path(x) for x in os.listdir(base_dir) if os.path.isdir(x)]

# Traverse folders
for taxon_dir in taxon_dirs:

    # Elements are always in this order when copied from the iNat URL
    taxon_id, taxon_name = taxon_dir.name.split('-')

    obs_dirs = []
    photos = []
    for item in taxon_dir.iterdir():
        # Each subdir of a taxon level dir will be 1 observation
        if item.is_dir():
            obs_dirs.append(item)
        # Requirement for use is no other files pesent besides observation images, so this is
        #  fine for now with no filename filtering
        if item.is_file():
            photos.append(item.name)

    # If any files exist in the taxon folder itself, create an observation with them as long as no .done file exists
    if len(photos) > 0 and has_donefile(taxon_dir):
        current_obs = Observation(photos=photos,
                                  taxon_name=taxon_name,
                                  taxon_id=taxon_id)

        observations.append(current_obs)
        photos = []

    # Iterate through the observation folders, if any
    if len(obs_dirs) > 0:
        for obs_dir in obs_dirs:
            #Skip if a .done file exists, otherwise make a new observation
            if not has_donefile(obs_dir):
                photos = [x.name for x in obs_dir.iterdir() if x.is_file()]
                current_obs = Observation(photos=photos,
                                          taxon_name=taxon_name,
                                          taxon_id=taxon_id)
                observations.append(current_obs)

# Now we have a list of observations, each with a list of photos, a taxon id, and a taxon name

#Deal with the GPX files
gps_points = []
for gpx in pathlib.Path(base_dir).glob('*.gpx'):
    gps_points.extend(parse_gpx(gpx))

for obs in observations:
    # Get and assign datestamp-- can't use the file attributes here because modification e.g., rotating, will
    #  overwrite created, modified, and accessed timestamps. Have to go to EXIF for this then.

    # TODO: Find the earliest date in the observations' photos to use for this to avoid issues with edited photos having
    #  the wrong date
    obs.observed_on = get_date(obs.photos[0])

    obs.coordinates = gps_points[nearest_datetime(gps_points, obs.observed_on)]

#At this point we could write out some kind of keyfile to which metadata could be added to, e.g., tags or project IDs,
# and then re-ingested and associated with the observations before submission to the API.

#Business rule type methods could also come here if we want to add information programmatically, e.g., add certain taxa
# to certain projects, invasive tag, personal collection UID, or even geotagging.
    
#Uploads all photos in folders contained in uploaded_folder
for folder in directories:
    subfolder = folder_name +'/' + folder + '/'
#    print(subfolder)
    upload_folder_single(subfolder, uploaded_folder, time_zone, accuracy,
                         user, passw, app, secret)

# Uploads photos in sub folders contained in species folders. These upload all
# Photos as a single observation.


for folder in directories:
        subfolder = folder_name +'/' + folder + '/'
        try: 
            for root, dirs, files in os.walk(subfolder):
                print('dirs' + dirs[0])
                for directory in dirs:
                    subsubfolder = subfolder + directory + '/'
                    upload_folder_multiple(subfolder, subsubfolder,
                                           uploaded_folder, time_zone, 
                                           accuracy, user, passw, app, secret)
        except:
            pass



        

print("Program complete")
