
from pyinaturalist.rest_api import create_observations
from pyinaturalist.rest_api import add_photo_to_observation
from classes import Observation
from logging import getLogger
from requests import HTTPError

logger = getLogger()


def upload_obs(obs: Observation, token:str):
    
    logger.debug('upload_obs()')

    params = {'observation':
                  {'taxon_id'                           : obs.taxon_id,
                   'species_guess'                      : obs.taxon_name,
                   'observed_on_string'                 : str(obs.observed_on),
                   'time_zone'                          : obs.tzone,
                   'description'                        : obs.comment,
                   'tag_list'                           : obs.tags,
                   #'latitude'                           : obs.coordinates[0],
                   #'longitude'                          : obs.coordinates[1],
                   'positional_accuracy'                : obs.geotag_accuracy,  # meters,

                   'observation_field_values_attributes':
                       [{'observation_field_id': '', 'value': ''}],
                   }, }

    try:
        logger.info('Uploading observation for taxon {0}'.format(obs.taxon_id))
        r = create_observations(params=params, access_token=token)
    
        obs.inat_id = r[0]['id']
    
        for file in obs.photos:
    
            r = add_photo_to_observation(observation_id=obs.inat_id ,
                                         file_object=open(file, 'rb'),
                                         access_token=token)

    except HTTPError as ex:
        obs.inat_result = 'Error creating observation: {0}'.format(ex)
        logger.error('Bad result from iNaturalist API, skipping this one')
        logger.exception(ex)
    
    except Exception as ex:
        raise
    else:
        logger.info('Success')
        obs.inat_result = 'ok'
    
    

def get_taxon_id(name:str) -> str:
    
    #TODO: Need to be able to get a taxon ID from the API or from the web interface to simplify setting up the upload folders
    pass