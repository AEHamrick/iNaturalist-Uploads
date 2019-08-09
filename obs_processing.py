from pathlib import Path
import os
from typing import Dict, Any, List
from classes import Observation
from gpx import accumulate_gps_points
from PIL import Image
from utility import get_created_date, get_lat_long, nearest_datetime, has_donefile
import config
'''
Business-rule type observation processing


'''

projects = {}

def assemble_skeleton_observations(working_dir: Path) -> List[Observation]:
    '''
    At its barest an observation is 1 or more photos, a taxon ID, and a taxon name, and some global values such as geotag accuracy and privacy;
    this method assembles these bare observations from the provided folder hierarchy and returns them for further processing.

    Each taxon_dir should be named in the form '{0}-{1}'.format(taxon id, taxon name) and should contain some
    combination of:

    :param taxon_dirs:
    :return: 'skeleton' observations created from photos found
    '''
    observations: List[Observation] = []
    taxon_dirs = []
    
    for d in [x for x in working_dir.iterdir() if x.is_dir()]:
        taxon_dirs.append(working_dir / d)
    
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
            # Requirement for use is no other files present besides observation images, so this is
            #  fine for now with no filename filtering
            if item.is_file():
                photos.append(Path(taxon_dir) / item.name)

        # If any files exist in the taxon folder itself, create an observation with them as long as no .done file exists
        if len(photos) > 0 and not has_donefile(taxon_dir):
            current_obs = Observation(photos=photos,
                                      taxon_name=taxon_name,
                                      taxon_id=taxon_id)

            current_obs.observed_on = min([get_created_date(x) for x in current_obs.photos])
            current_obs.tzone =  current_obs.observed_on.timezone_name
            observations.append(current_obs)
            photos = []

        # Iterate through the observation folders, if any; skip a folder if a .done file exists
        if len(obs_dirs) > 0:
            for obs_dir in [x for x in obs_dirs if not has_donefile(x)]:
                
                photos = [Path(obs_dir) / x.name for x in obs_dir.iterdir() if x.is_file()]
                
                current_obs = Observation(photos=photos,
                                          taxon_name=taxon_name,
                                          taxon_id=taxon_id)

                current_obs.observed_on = min([get_created_date(x) for x in current_obs.photos])
                current_obs.tzone = current_obs.observed_on.timezone_name
                observations.append(current_obs)

    return observations

def assign_coordinates_to_obs(observations: List[Observation], geotag_method:str, values:Dict):
    '''

    :param observations:
    :param gps_points:
    :param try_exif:
    :return:
    '''

    if geotag_method == 'None':
        return
        
    #Iterate over observations, never reprocess one that already has coordinates
    for obs in [x for x in observations if x.coordinates != [None,None]]:
        # Get and assign datestamp-- can't use the file attributes here because modification e.g., rotating, will
        #  overwrite created, modified, and accessed timestamps. Have to go to EXIF for this then.

        coordinates = [None, None]

        if geotag_method == 'EXIF':
            with Image.open(obs.photos[0]) as img:
                coordinates = get_lat_long(img)


        if geotag_method == 'GPX':
            gps_points = accumulate_gps_points(Path(values['path_working']) / 'gpx')
            
            coordinates = gps_points[nearest_datetime(list(gps_points.keys()), obs.observed_on)]

        obs.coordinates = coordinates
        obs.geotag_accuracy = values['geotag_acc']


def process_rules(observations: List[Observation], flags: Dict[str,bool]):
    '''
    Wrapper method for separate processing functions e.g., addition to projects, addition of tags

    :param observations:
    :param flags:
    :return:
    '''
    
    pass


def process_project_rules(observations: List[Observation], flags: Dict[str,bool]):
    '''
    Add observation to project(s) based on certain criteria

    :param obs: Observation to evaluate for project addition
    :return:
    '''
    pass