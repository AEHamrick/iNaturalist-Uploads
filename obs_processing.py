from typing import Dict, Any, List
from classes import Observation

from PIL import Image
from import_functions import get_date, get_lat_long, nearest_datetime
import config
'''
Business-rule type observation processing


'''

projects = {}


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