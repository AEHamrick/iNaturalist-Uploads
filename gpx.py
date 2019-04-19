'''

Helper methods to work with a GPX file in companion to the upload photo set to facilitate adding lat/long coordinates.

Modern security concerns mean that many choose not to embed GPS data in photos taken with a smartphone; too, many DSLRs
simply lack this facility. The idea here is to use a GPX file recorded during a field session to estimate coordinates
based on time the photo was taken.
'''

import gpxpy
import pathlib

import os
import sys
from typing import Union, List, Tuple, Dict
from datetime import datetime, timedelta

def parse_gpx(gpx_file: Union[pathlib.Path, str]) -> Dict[datetime, Tuple[str,str]]:
	'''Get points and their corresponding times from the GPX file'''

	points = {}
	with open(gpx_file, 'r') as gfile:
		gpx_tree = gpxpy.parse(gfile)

		for track in gpx_tree.tracks:
			for seg in track.segments:
				for point in seg.points:
					points[point.time] = (point.latitude,point.longitude)


	return points