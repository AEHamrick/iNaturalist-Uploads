'''
Helper methods to work with a GPX file in companion to the upload photo set to facilitate adding lat/long coordinates.

Modern security concerns mean that many choose not to embed GPS data in photos taken with a smartphone; too, many DSLRs
simply lack this facility. With that in mind, with either a smartphone or a dedicated GPS device, a GPX file
can be recorded during a field session and from the set of points and timestamps it contains, we can estimate
coordinates a photo was taken based on timestamp.
'''

import gpxpy
import pathlib
from pytz import timezone
from pendulum import datetime, Period, Duration, instance
import pendulum
import os
import sys
from typing import Union, List, Tuple, Dict
from logging import getLogger

logger = getLogger()

def parse_gpx(gpx_file: Union[pathlib.Path,str]) -> Dict[datetime, Tuple[str,str]]:
    '''
    Get points and their corresponding timestamp from the GPX file. The timestamp is optional according to the spec,
    but points without timestamps are useless for our purposes, so skip those points that lack it.

    GPX files use ISO8601 for timestamp

    :param gpx_file: gpx file to parse
    :return: points that meet our criteria in the form of {timestamp : (lat, long)}

    '''

    points = {}
    logger.debug('parse_gpx()')
    with open(gpx_file, 'r') as gfile:
        logger.info('Parsing {0}'.format(gpx_file))
        gpx_tree = gpxpy.parse(gfile)

    logger.debug('Accumulating gps points')
    for track in gpx_tree.tracks:
        for seg in track.segments:
            for point in seg.points:
                if point.time == None:
                    continue
                # Timestamp in the form of 2018-10-13T15:01:52Z; GPXPy already gives it to us in vanilla datetime
                # GPX seems to always record timestamps in UTC, so do a conversion
                timestamp = pendulum.instance(point.time).in_tz('local')
                
                points[timestamp] = (point.latitude,point.longitude)
    
    logger.info('Found {0} gps points with timestamp'.format(str(len(points))))
    
    return points


def accumulate_gps_points(gpx_dir: pathlib.Path) -> Dict[datetime, Tuple[str,str]]:
    '''
    Iterate over the provided GPX files and assemble points with their timestamps

    :param gpx_dir: directory where gpx files are contained; no subdirectories are inspected
    :return:
    '''
    gps_points = {}
    
    logger.debug('accumulate_gps_points()')
    
    for gpx in pathlib.Path(gpx_dir).glob('*.gpx'):
        gps_points.update(parse_gpx(gpx))

    logger.info('Found {0} gps points total'.format(str(len(gps_points))))
    
    return gps_points
