


class GeotagMatchException(Exception):
    '''
    Signals that no geotag timestamp has been found that falls within +- the specified amount of the target timestamp.
    
    E.g., if the window is +- 1 hour and the target timestamp is 2019-08-13 05:00:00-0400 and no gpx point timestamp can be
    found between 04:00:00 and 06:00:00 then this exception will raise
    '''
    # TODO: Add the closest match?