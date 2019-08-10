import os, sys
from enum import Enum
from pathlib import Path
from pendulum import DateTime, tz
from typing import List, Union, Tuple, Dict, Optional
import keyring
from config import flags
from pyinaturalist.rest_api import get_access_token

from logging import getLogger

logger  = getLogger()

class Observation():
	'''
	iNaturalist terms an uploaded instance of flora or fauna an observation. For purposes of this utility, at its
	barest an Observation is a taxon ID, 1 photo, and a datestamp derived from the photo's creation date; ideally
	there will also be geotag coordinates, geotag privacy, and metadata such as tags or project memberships. Comments
	and metadata will likely by way of to-be-implemented keyfile creation/consumption.
	'''

	#Keep these matched by index
	photos = []
	coordinates: Tuple[float, float] = tuple()

	path: Path = None
	taxon_id: int = None
	taxon_name: str = None
	comment: str = None
	observed_on: DateTime = None
	tzone: tz = None
	
	geotag_accuracy: int = None
	geotag_privacy: str = None

	inat_id: int = None #This comes back from the API, hang on to it just in case we need to update
	inat_result: str = None #Keep track of which observations uploaded successfully or not; per docs a bad upload will raise an exception

	# TODO: Once implemented mechanism for deriving ID from name goes here
	tags: List[str] = []
	fields: List[str] = []
	projects: List[int] = []

	def __init__(self, taxon_id: int, taxon_name: Optional[str], photos: List[Path], accuracy: Optional[int] = 50,
				 privacy: Optional[str] = 'Obscured'):

		self.taxon_id = taxon_id
		self.taxon_name = taxon_name
		self.photos = photos
		self.geotag_accuracy = accuracy
		self.geotag_privacy = privacy
		
		self.path = self.photos[0].parent


class Auth:
	'''
    Manage the iNat credentials
    '''
	
	token = ''
	app_id = ''
	app_secret = ''
	
	def __init__(self, user: str,
				 pwd: Optional[str] = None,
				 app_id: Optional[str] = None,
				 app_secret: Optional[str] = None):
		
		if flags['USE_SECURE_KEYRING']:
			
			# TODO: Figure out a better way to store creds in windows that corresponds to the service / user / password model
			#  that keyring uses
			
			self.app_id = keyring.get_password('iNat_app_id', '{0}'.format(user))
			self.app_secret = keyring.get_password('iNat_secret', '{0}'.format(user))
			
			# TODO: Add some error checking and logging around this
			self.token = get_access_token(username=user,
										  password=keyring.get_password('iNat', user),
										  app_id=self.app_id,
										  app_secret=self.app_secret)
		else:
			
			self.app_id = app_id
			self.app_secret = app_secret
			
			self.token = get_access_token(username=user,
										  password=pwd,
										  app_id=app_id,
										  app_secret=app_secret)

class geotag_methods(Enum):
	gpx = 'GPX'
	exif = 'EXIF'
	manual = 'MANUAL'
	
	@staticmethod
	def get_method(values):
		if values['geotag_primary_gpx']:
			return geotag_methods.gpx
		elif values['geotag_primary_exif']:
			return geotag_methods.exif
		elif values['geotag_primary_manual']:
			return geotag_methods.manual
		else:
			raise ValueError('Mismatch between values from GUI and geotag methods')
	
	@staticmethod
	def get_fallback_method(primary):
		if primary == geotag_methods.gpx:
			return geotag_methods.exif
		elif primary == geotag_methods.exif:
			return geotag_methods.gpx
		else:
			raise ValueError('Mismatch between values from GUI and geotag fallback method')
		
class geotag_privacy(Enum):
	#TODO: Implement in gui and observation processing
	open = 'Public'
	obscured = 'Obscured'
	private = 'Private'
	
	