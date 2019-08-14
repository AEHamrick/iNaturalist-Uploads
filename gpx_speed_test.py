'''
Trying to make the gpx coordinate check faster
'''
import sys, os,pendulum
from pathlib import Path
import random

from gpx import accumulate_gps_points, parse_gpx
from obs_processing import assign_coordinates_to_obs
from custom_logging import create_logger
import logging
import timeit
from bisect import bisect_left
from typing import List, Set, Union

logger = create_logger(Path(__file__).parent, 'iNat_testing')


def nearest_datetime(items: Union[Set[pendulum.datetime],List[pendulum.datetime]],
                     target: pendulum.datetime):
    '''

    :param items:  Datetimes to search through
    :param target: Datetime to match or come closest to
    :return:
    '''

    # TODO: This is way too slow with lots of GPX points
    # TODO: Build a minimum acceptable difference into this (e.g., > +- 1 hour)
    #Didn't come up with this, pretty neat
    nearest = min(items, key=lambda x: abs(x - target))
    logger.debug(nearest)
    return nearest

def nearest_slow(target, points):
    '''perform one date lookup'''
    logger.debug(target)
    needle = points[nearest_datetime(list(points.keys()), target)]
    logger.debug(needle)
    return needle

def nearest_fast(target, points):
    """
    Assumes myList is sorted. Returns closest value to myNumber.

    If two numbers are equally close, return the smallest number.
    """
    pos = bisect_left(points, target)
    if pos == 0:
        needle = points[0]
    elif pos == len(points):
        needle =  points[-1]
    else:
        before = points[pos - 1]
        after = points[pos]
        if after - target < target - before:
            needle = after
        else:
            needle = before
        
    logger.debug(needle)
    return needle

if __name__ == '__main__':
    
    
    reps = 10
    points = accumulate_gps_points(Path('D:\\Users\Sir\Pictures\iNaturalist to-upload\Batch\gpx'))
    
    # t = pendulum.duration(seconds= timeit.timeit(stmt='nearest_slow(pendulum.now(tz=\'local\'), points)',
    #                       globals=globals(),
    #                       number=reps))
    
    t = pendulum.duration(seconds= timeit.timeit(stmt='nearest_fast(pendulum.now(tz=\'local\'), sorted(list(points.keys())))',
                          globals=globals(),
                          number=reps))
    
    logger.info('{0} reps in {1}'.format(str(reps),t.in_words()))
    logger.info('Average {0}'.format(pendulum.duration(seconds=t.in_seconds()/reps)))

    
    



