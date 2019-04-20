from typing import Dict, Any, List
from classes import Observation
'''
Business-rule type observation processing


'''

projects = {}


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