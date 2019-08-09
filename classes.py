import os, sys
from pathlib import Path
from pendulum import DateTime, tz
from typing import List, Union, Tuple, Dict, Optional

'''
classes
'''

class Observation():
	'''

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

	# TODO: Mechanism for getting the ID from name
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