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



	