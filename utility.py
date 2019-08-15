""" This file includes all the functions used in the associated file
upload_folders.py. This is primarily functions associated with getting exif 
data from the photos, choosing a taxa based on the name of the folder
and uploading the files to iNaturalist."""

from typing import Union, List, Dict, Tuple
import pathlib
import shutil
import os
import pendulum
from pendulum import DateTime
import PIL
from PIL import ExifTags, Image
from bisect import bisect_left
from logging import getLogger
logger = getLogger()
from exceptions import GeotagMatchException
def nearest_datetime(items: List[DateTime], target: DateTime, window:pendulum.duration):
    '''

    :param items:  Datetimes to search through
    :param target: Datetime to match or come closest to
    :return:
    '''
    
    '''
    Didn't come up with this, pretty neat, but ultimately way too slow with lots of points to check
    return min(items, key=lambda x: abs(x - target))
    
    Instead sort the input list and use bisect for binary search
    '''
    
    pos = bisect_left(items, target)
    
    #Edge case for the bisection point being before the first element (i.e., before element 0)
    if pos == 0:
        if items[0] - target <= window:
            closest = items[0]
        else:
            raise GeotagMatchException
    # Edge case for the bisection point being after the last element (i.e., after element -1)
    elif pos == len(items):
        if target - items[-1] <= window:
            closest =  items[-1]
        else:
            raise GeotagMatchException
    else:
        before = items[pos - 1]
        after = items[pos]
        
        after_diff = after - target
        before_diff = target - before
        
        #Bisection gives a point on either side (i.e., earlier and later) of the target; need to know which one is
        # closer, temporally speaking
        
        #Later timestamp is closest
        if after_diff < before_diff:
            
            if after_diff <= window:
                closest = after
            else:
                #If closest one is outside of the window then the other one necessarily must be
                raise GeotagMatchException
        
        #Earlier timestamp is closest
        else:
            if before_diff <= window:
                closest = before
            else:
                #As above
                raise GeotagMatchException
        
    logger.debug(closest)
    
    return closest

def has_donefile(d: Union[str, pathlib.Path]) -> bool:
    '''
    Check a directory for existence of a '.done' file used as a flag to avoid duplicate observation upload

    :param d: input directory
    :return: True if any file with the string '.done' in its name exists in input dir d else False
    '''
    if type(d) == str:
        d = pathlib.Path(d)

    files: List[pathlib.Path] = [x for x in d.iterdir() if x.is_file()]

    if any(['.done' in x.name for x in files]):
        logger.info('found .done file in {0}'.format(d))
        return True
    else:
        return False


# This function returns the latitude and longitude of a .jpg image
def get_lat_long(image):
    # Gets all the exif data from the photo
    exif = {
        PIL.ExifTags.TAGS[k]: v
        for k, v in image._getexif().items()
        if k in PIL.ExifTags.TAGS
    }

    latitude = None
    longitude = None

    # From all the exif data, pulls the GPS data
    gps_info = exif.get('GPSInfo')
    # The GPS data is in a odd format, so have to dig for it a bit. This was
    # only tested on files lightroom tagged.
    # TODO: See if there's a module for this so we don't have to mess with it
    latitude_direction = str(gps_info.get(1)[0])
    latitude_degrees = float(gps_info.get(2)[0][0])
    minutes = float(gps_info.get(2)[1][0])
    multiplier = float(gps_info.get(2)[1][1])
    latitude_minutes = minutes/multiplier
    seconds = float(gps_info.get(2)[2][0])
    multiplier = float(gps_info.get(2)[2][1])
    latitude_seconds = seconds/multiplier
    
    
    # The sign is changed depending on if this is N or S
    if latitude_direction == 'N' or latitude_direction == 'n':
        latitude = latitude_degrees+latitude_minutes/60 \
                    + latitude_seconds/3600
    elif latitude_direction == 'S' or latitude_direction == 's':
        latitude = -(latitude_degrees+latitude_minutes/60
                    + latitude_seconds/3600)
        
    longitude_direction = gps_info.get(3)[0]
    longitude_degrees = gps_info.get(4)[0][0]
    minutes = float(gps_info.get(4)[1][0])
    multiplier = float(gps_info.get(4)[1][1])
    longitude_minutes = minutes/multiplier
    seconds = float(gps_info.get(4)[2][0])
    multiplier = float(gps_info.get(4)[2][1])
    longitude_seconds = seconds/multiplier
    # The sign is changed depending on if this is E or W
    if longitude_direction == 'E' or longitude_direction == 'e':
        longitude = longitude_degrees+longitude_minutes/60 \
                    + longitude_seconds/3600
    elif longitude_direction == 'W' or longitude_direction == 'w':
        longitude = -(longitude_degrees+longitude_minutes/60
                    + longitude_seconds/3600)
    
    latitude_longitude = [latitude, longitude]
    
    # Returns a list with both latitude and longitude in decimal format.
    return latitude_longitude

def get_created_date(image: str) -> DateTime:
    
    '''
    Pulls the date and time from the exif format
    
    Can't use the file attributes here because modification e.g., rotating, will overwrite created, modified,
    and accessed timestamps. Have to go to EXIF for this then.
    
    Exif.Image.DateTimeOriginal is 36867 decimal or 0x9003 hex
    %Y:%m:%d %H:%M:%S
    
    Caveat, it is timezone naive
    '''
    
    date_and_time = PIL.Image.open(image)._getexif()[36867]

    # TODO: Default to current date?
    if date_and_time is None:
        raise ValueError('No creation date in EXIF')
    dt = pendulum.parse(date_and_time, tz='local')
    
    return dt
