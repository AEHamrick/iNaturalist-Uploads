import os, sys
from datetime import datetime
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

	taxon_id: int = None
	taxon_name: str = None
	comment: str = ''
	observed_on: datetime = None

	# TODO: Mechanism for getting the ID from name
	tags: List[str] = []
	fields: List[str] = []
	projects: List[int] = []

	def __init__(self, taxon_id: int, taxon_name: Optional[str], photos: List[str]):

		self.taxon_id = taxon_id
		self.taxon_name = taxon_name
		self.photos = photos
