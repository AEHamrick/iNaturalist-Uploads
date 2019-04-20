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
# TODO: Expand documentation and docstrings
# TODO: oAuth/API access method
# TODO: Logging
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
from import_functions import upload_folder_single, upload_folder_multiple, \
                             has_donefile, nearest_datetime, get_date
from classes import Observation
from import_gui import input_data
from gpx import parse_gpx
from obs_processing import process_rules, assign_coordinates_to_obs
import config


def assemble_skeleton_observations(taxon_dirs: List[pathlib.Path]) -> List[Observation]:
    '''
    At its barest an observation is 1 or more photos, a taxon ID, and a taxon name; this method assembles these bare
    observations from the provided folder hierarchy and returns them for further processing.

    Each taxon_dir should be named in the form '{0}-{1}'.format(taxon id, taxon name) and should contain some
    combination of:

    :param taxon_dirs:
    :return: 'skeleton' observations created from photos found
    '''
    observations: List[Observation] = []
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

            current_obs.observed_on = min([get_date(x) for x in current_obs.photos])
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

                    current_obs.observed_on = min([get_date(x) for x in current_obs.photos])
                    observations.append(current_obs)

    return observations


def accumulate_gps_points(gpx_dir: pathlib.Path) -> Dict[datetime, Tuple[str,str]]:
    '''
    Iterate over the provided GPX files and assemble points with their timestamps

    :param gpx_dir: directory where gpx files are contained; no subdirectories are inspected
    :return:
    '''
    gps_points = {}

    for gpx in pathlib.Path(gpx_dir).glob('*.gpx'):
        gps_points.update(parse_gpx(gpx))

    return gps_points


if __name__ == '__main__':
    print("Running")

    # Pulls the data from the gui when the script is run.
    [user, passw, app, secret,
     base_dir, time_zone, accuracy] = input_data()

    print('Uploading all photos in folders contained in ' + base_dir)

    directories = []

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

