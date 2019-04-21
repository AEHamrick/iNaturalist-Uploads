import keyring
from typing import Dict, Optional
from pyinaturalist.rest_api import get_access_token
flags = {}
vals =  {'timezone': 'America/New York',
         'accuracy': 50}

class Auth:
    '''
    Manage the iNat credentials
    '''

    token = ''

    def __init__(self, gui_creds: Optional[Dict[str,str]]):
        if flags['USE_SECURE_KEYRING']:
            user = keyring.get_password('iNat','user')

            self.token =     get_access_token(username=user,
                             password=keyring.get_password('iNat', user),
                             app_id=keyring.get_password('iNat','{0}_app_id'.format(user)),
                             app_secret=keyring.get_password('iNat','{0}_secret'.format(user)))
        else:
            self.token = get_access_token(username=gui_creds['user'],
                                          password=gui_creds['pass'],
                                          app_id=gui_creds['app_id'],
                                          app_secret=gui_creds['app_secret'])
