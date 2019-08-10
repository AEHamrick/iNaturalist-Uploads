import keyring
from enum import Enum
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
    global flags
    
    #region: Configuration
    flags['USE_SECURE_KEYRING'] = values['USE_SECURE_KEYRING'] # Use system credential store via the keyring module
    flags['IGNORE_DONEFILES'] = False                          # Unused; Ignore .done files in taxon folders & treat as un-uploaded observation
    #region: API

    #endregion

    #region: Processing batch level
    flags['USE_PER_BATCH_METADATA'] = False       # Unused; Allow usage of meta-data that applies universally e.g., tag for a bioBlitz event
    flags['WRITE_KEYFILE'] = False                # Unused; The key file will be a delimited file that allows for manual
                                                  #   addition of data to some or all observations in a batch

    #endregion

    #region: Processing observation level
    flags['GEOTAG_PRIMARY'] = geotag_methods.get_method(values) # GPX, EXIF, manual source for geotag
    flags['GEOTAG_FALLBACK'] = values['geotag_fallback_flag']   # If the selected geotag source has no data, try the other as a backup
    flags['GEOTAG_PRIVACY'] = values['geotag_privacy']          # Private/public/obscured
    flags['GEOTAG_ACCURACY'] = values['geotag_acc']        # Accuracy of geotag rendering in meters
    flags['APPLY_PROJECT_RULES'] = True                         # Evaluate observations for project membership
    #endregion

    





class Auth:
    '''
    Manage the iNat credentials
    '''

    token = ''
    app_id = ''
    app_secret = ''
    

    def __init__(self, user: str,
                       pwd: Optional[str] = None,
                       app_id: Optional[str] = None ,
                       app_secret: Optional[str] = None):
        

        
        if flags['USE_SECURE_KEYRING']:
            
            # TODO: Figure out a better way to do this in windows that corresponds to the service / user / password model
            #  that keyring uses

            self.app_id     = keyring.get_password('iNat_app_id','{0}'.format(user))
            self.app_secret = keyring.get_password('iNat_secret','{0}'.format(user))

            self.token =     get_access_token(username=user,
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

#region: Enums for use in flags
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
        
        