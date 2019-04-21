
from pyinaturalist.rest_api import create_observations

from pyinaturalist.rest_api import add_photo_to_observation

from classes import Observation
import config


def upload_obs(obs: Observation):


    params = {'observation':
                  {'taxon_id'                           : obs.taxon_id,
                   'species_guess'                      : obs.taxon_name,
                   'observed_on_string'                 : str(obs.observed_on),
                   'time_zone'                          : config.vals['time_zone'],
                   'description'                        : obs.comment,
                   'tag_list'                           : obs.tags,
                   'latitude'                           : obs.coordinates[0],
                   'longitude'                          : obs.coordinates[1],
                   'positional_accuracy'                : config.vals['ACCURACY'],  # meters,

                   'observation_field_values_attributes':
                       [{'observation_field_id': '', 'value': ''}],
                   }, }


    r = create_observations(params=params, access_token=config.Auth.token)

    new_observation_id = r[0]['id']

    for file in obs.photos:

        r = add_photo_to_observation(observation_id=new_observation_id,
                                     file_object=open(file, 'rb'),
                                     access_token=config.Auth.token)


    pass
