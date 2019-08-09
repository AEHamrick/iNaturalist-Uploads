
from pyinaturalist.rest_api import create_observations

from pyinaturalist.rest_api import add_photo_to_observation

from classes import Observation
import config
from requests import HTTPError


def upload_obs(obs: Observation):


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
        r = create_observations(params=params, access_token=config.Auth.token)
    
        obs.inat_id = r[0]['id']
    
        for file in obs.photos:
    
            r = add_photo_to_observation(observation_id=obs.inat_id ,
                                         file_object=open(file, 'rb'),
                                         access_token=config.Auth.token)

    except HTTPError as ex:
        obs.inat_result = 'Error creating observation: {0}'.format(ex)
        
    except Exception as ex:
        raise
    
    else:
        obs.inat_result = 'ok'
    
    
        