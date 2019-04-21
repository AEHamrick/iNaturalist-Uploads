# -*- coding: utf-8 -*-
"""
Expected structure
Base dir
 |
 - GPX file 1
 - GPX file 2
 - ...
 - GPX file n
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
   |
   - Obs dir 2



"""
# TODO: PySimpleGUI
# TODO: Expand documentation and docstrings
# TODO: Logging
# TODO: Override keyring with credentials from GUI
# TODO: Consistent-ize use of pathlib.Path over string pathsx
# TODO: Implement docopt and map out what things we want to be args and options
# TODO: Figure out how to run from either GUI or command line
# TODO: Processing rules
# TODO: Keyfile process and contents
# TODO: Consider multiple formats for taxon level folder names
# TODO: Consolidate creation of and addition of photos to a new obs?

import os
import pathlib
from typing import List, Dict, Tuple
from datetime import datetime


#Project imports
from utility import has_donefile, get_created_date
from classes import Observation
from gui import input_data
from gpx import parse_gpx, accumulate_gps_points
from obs_processing import process_rules, assign_coordinates_to_obs, assemble_skeleton_observations
from api_interactions import upload_obs
import config


if __name__ == '__main__':
    print("Running")

    # Pulls the data from the gui when the script is run.
    [user, passw, app, secret,
     base_dir, time_zone, accuracy] = input_data()

    print('Uploading all photos in folders contained in ' + base_dir)

    taxon_dirs = [pathlib.Path(x) for x in os.listdir(base_dir) if os.path.isdir(x)]

    observations = assemble_skeleton_observations(taxon_dirs)
    # Now we have a list of observations, each with a list of photos, a taxon id, and a taxon name

    coordinates = accumulate_gps_points(base_dir)

    assign_coordinates_to_obs(observations,coordinates,config.flags['TRY_EXIF'])

    # At this point we could write out some kind of keyfile to which metadata could be added to, e.g., tags
    # or project IDs, and then re-ingested and associated with the observations before submission to the API.

    # Business rule type methods could also come here if we want to add information programmatically, e.g.,
    # add certain taxa to certain projects, invasive tag, personal collection UID, or even geotagging.

    process_rules(observations,{}) #placeholder

    for obs in observations:
        upload_obs(obs)
        

