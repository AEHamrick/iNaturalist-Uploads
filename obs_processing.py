import pathlib
from typing import Dict, Any, List
from classes import Observation

from PIL import Image
from utility import get_created_date, get_lat_long, nearest_datetime, has_donefile
import config
'''
Business-rule type observation processing


'''

projects = {}

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

            current_obs.observed_on = min([get_created_date(x) for x in current_obs.photos])
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

                    current_obs.observed_on = min([get_created_date(x) for x in current_obs.photos])
                    observations.append(current_obs)

    return observations

def assign_coordinates_to_obs(observations, gps_points, try_exif):
    '''

    :param observations:
    :param gps_points:
    :param try_exif:
    :return:
    '''

    for obs in observations:
        # Get and assign datestamp-- can't use the file attributes here because modification e.g., rotating, will
        #  overwrite created, modified, and accessed timestamps. Have to go to EXIF for this then.

        coordinates = [None, None]

        if try_exif:
            with Image.open(obs.photos[0]) as img:
                coordinates = get_lat_long(img)


        if coordinates == [None, None]:
            coordinates = gps_points[nearest_datetime(gps_points, obs.observed_on)]

        obs.coordinates = coordinates


def process_rules(observations: List[Observation], flags: Dict[str,bool]):
    '''
    Wrapper method for separate processing functions

    :param observations:
    :param flags:
    :return:
    '''

    for obs in observations:
        if flags['process_project_rules']:
            process_project_rules(obs)


def process_project_rules(obs: Observation):
    '''
    Add observation to project(s)

    :param obs: Observation to evaluate for project addition
    :return:
    '''
    pass