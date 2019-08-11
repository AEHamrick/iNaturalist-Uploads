
from pyinaturalist.rest_api import create_observations, add_photo_to_observation, get_access_token
from classes import Observation
from logging import getLogger
from requests import HTTPError
from typing import Optional
import keyring

from config import flags

logger = getLogger()


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