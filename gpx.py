'''

Helper methods to work with a GPX file in companion to the upload photo set to facilitate adding lat/long coordinates.

Modern security concerns mean that many choose not to embed GPS data in photos taken with a smartphone; too, many DSLRs
simply lack this facility. The idea here is to use a GPX file recorded during a field session to estimate coordinates
based on time the photo was taken.
'''

import gpxpy
import pathlib
from pytz import timezone

import os
import sys
from typing import Union, List, Tuple, Dict
from datetime import datetime, timedelta

def parse_gpx(gpx_file: Union[pathlib.Path, str]) -> Dict[datetime, Tuple[str,str]]:
	'''
	Get points and their corresponding timestamp from the GPX file. The timestamp is optional according to the spec
	, but points without timestamps are useless for our purposes, so skip those points that lack it.

	GPX files use ISO8601 for timestamp

	:param gpx_file: gpx file to parse
	:return: points that meet our criteria in the form of {timestamp : (lat, long)}

	'''

	points = {}
	with open(gpx_file, 'r') as gfile:
		gpx_tree = gpxpy.parse(gfile)

	for track in gpx_tree.tracks:
		for seg in track.segments:
			for point in seg.points:
				if point.time == None:
					continue
				# Timestamp in the form of 2018-10-13T15:01:52Z
				timestamp = datetime.strptime(point.time,'%Y-%m-%dT%H:%M:%S%z')
				points[timestamp] = (point.latitude,point.longitude)

	return points