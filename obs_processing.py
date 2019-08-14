from pathlib import Path
import os
from typing import Dict, Any, List
from classes import Observation
from config import geotag_methods, flags
from gpx import accumulate_gps_points
from PIL import Image
from utility import get_created_date, get_lat_long, nearest_datetime, has_donefile
from exceptions import GeotagMatchException
from logging import getLogger

logger = getLogger()

'''
Assembly of observations from rudimentary data, "business-rule" type observation processing against criteria
'''

#TODO: toml or similar for observation rules?

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
    
    logger.debug('assemble_skeleton_observations()')
    
    logger.info('Found these top level taxon dirs in {0}'.format(working_dir))
    for d in [x for x in working_dir.iterdir() if x.is_dir() and x.name != flags['GPX_DIR_NAME']]:
        taxon_dirs.append(working_dir / d)
        logger.info('{0}'.format(d))
        
    
    # Traverse folders
    
    logger.info('Traversing taxon dirs')
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
            if item.is_file() and not item.name.endswith('.done'):
                photos.append(Path(taxon_dir) / item.name)
            
        # If any files exist in the taxon folder itself, create an observation with them as long as no .done file exists unless ignore donefiles is enabled
        if len(photos) > 0 and (not has_donefile(taxon_dir) or flags['IGNORE_DONEFILES']):
            logger.info('Creating observation for top level taxon dir')
            current_obs = Observation(photos=photos,
                                      taxon_name=taxon_name,
                                      taxon_id=taxon_id)

            logger.info('{0} photos total'.format(str(len(photos))))
            current_obs.observed_on = min([get_created_date(x) for x in current_obs.photos])
            current_obs.tzone =  current_obs.observed_on.timezone_name
            observations.append(current_obs)
            photos = []

        # Iterate through the observation folders, if any; skip a folder if a .done file exists unless ignore donefiles is enabled
        if len(obs_dirs) > 0:
            # TODO: Test ignore donefiles & add to GUI when working
            for obs_dir in [x for x in obs_dirs if (not has_donefile(x) or flags['IGNORE_DONEFILES'])]:
                logger.info('Creating observation')
                photos = [Path(obs_dir) / x.name for x in obs_dir.iterdir() if x.is_file() and not x.name.endswith('.done')]
                logger.info('{0} photos total'.format(str(len(photos))))
                
                current_obs = Observation(photos=photos,
                                          taxon_name=taxon_name,
                                          taxon_id=taxon_id)

                # Obs photos /should/ all be taken relatively close together, should be fine to take the earliest date of
                #  the set.
            
                current_obs.observed_on = min([get_created_date(x) for x in current_obs.photos])
                current_obs.tzone = current_obs.observed_on.timezone_name
                observations.append(current_obs)
    logger.info('{0} observations total'.format(str(len(observations))))
    
    return observations

def assign_coordinates_to_obs(observations: List[Observation], geotag_method:str, working_path:Path):
    '''

    :param observations:
    :param gps_points:
    :param try_exif:
    :return:
    '''

    logger.debug('assign_coordinates_to_obs')
    
    if geotag_method == geotag_methods.manual:
        raise ValueError('Shouldn\'t be in assign_coordinates_to_obs() if manual geotagging is selected')
        
    #Iterate over observations, never reprocess one that already has coordinates

    if geotag_method == geotag_methods.exif:
        for obs in [x for x in observations if not x.coordinates]:
            logger.info('Using EXIF')
            with Image.open(obs.photos[0]) as img:
                obs.coordinates = get_lat_long(img)
            obs.geotag_accuracy = flags['GEOTAG_ACCURACY']


    if geotag_method == geotag_methods.gpx:
        gps_points = accumulate_gps_points(working_path / 'gpx')
        logger.info('Using GPX')
        
        for obs in [x for x in observations if not x.coordinates]:
            try:
                obs.coordinates = gps_points[nearest_datetime(list(gps_points.keys()), obs.observed_on, flags['GEOTAG_TIMESTAMP_WINDOW'])]
            except GeotagMatchException:
                logger.warning('No gpx point can be found +-{0} of {1}'.format(str(flags['GEOTAG_TIMESTAMP_WINDOW']),obs.observed_on))
                #TODO: Perhaps find a better default
                obs.coordinates = (0,0)
            obs.geotag_accuracy = flags['GEOTAG_ACCURACY']


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