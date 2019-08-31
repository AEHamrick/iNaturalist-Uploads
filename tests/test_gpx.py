import pytest

from gpx import accumulate_gps_points, parse_gpx



def test_accumulate_gps_points():
    '''
    Test cases:
    1 input file
    >1 input files
    invalid file - check for exception
    0 input files (empty list)
    
    
    :return:
    '''
    
    pass


def test_parse_gpx():
    '''
    Test cases:
    valid gpx with timestamps
    valid gpx without timestamps
    truncated file
    empty file
    
    n.b.,  testing against files that don't match the gpx schema out of scope for now
    
    :return:
    '''
    
    pass