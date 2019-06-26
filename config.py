import keyring
from typing import Dict, Optional, Any
from pyinaturalist.rest_api import get_access_token
flags = {}
vals =  {'timezone': 'America/New York',
         'accuracy': 50}

def set_flags(values:Dict[str,Any]):
    '''
    This could probably be set up in a more dynamic way but it seems more instructive to explicitly
    define flags so they can be mildly categorized

    :param values:
    :return:
    '''

    flag_names = [
    #region: Configuration
    'USE_SECURE_KEYRING',           # Use system credential store via the keyring module
    'IGNORE_DONEFILES',             # Ignore .done files in taxon folders & treat as un-uploaded observation
    #region: API

    #endregion

    #region: Processing batch level
    'USE_PER_BATCH_METADATA',       # Allow usage of meta-data that applies universally


    #endregion

    #region: Processing observation level
    'USE_EXIF_GEOTAG',              # Use EXIF tags as geotag data source
    'USE_GPX_GEOTAG',               # Use GPX file as geotag data source
    'GEOTAG_FALLBACK',              # If the selected geotag source cannot be used, try the other as backup
    'SKIP_GEOTAG'                   # Skip automated geotagging; this will result in poor quality observations, use carefully
    'PROCESS_PROJECT_RULES',        # Examine observations to see if they fit any criteria to be added to projects
    'USE_PER_OBSERVATION_METADATA', # Allow usage of a meta-data file for extended manual per-observation data
    #endregion

    ]

    global flags
    flags = {fk : values[fk] for fk in flag_names}


class Auth:
    '''
    Manage the iNat credentials
    '''

    token = ''

    def __init__(self, user: Optional[str],
                       pwd: Optional[str],
                       app_id: Optional[str],
                       app_secret: Optional[str]):
        if flags['USE_SECURE_KEYRING']:
            #Think it would be best to require user at the GUI, that way the keyring setup could be per user
            #by inserting it into the keyring fields as below
            #user = keyring.get_password('iNat','user')

            self.token =     get_access_token(username=user,
                             password=keyring.get_password('iNat', user),
                             app_id=keyring.get_password('iNat','{0}_app_id'.format(user)),
                             app_secret=keyring.get_password('iNat','{0}_secret'.format(user)))
        else:
            self.token = get_access_token(username=user,
                                          password=pwd,
                                          app_id=app_id,
                                          app_secret=app_secret)
