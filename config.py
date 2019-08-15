from typing import Dict, Optional, Any
from logging import getLogger
from enum import Enum
flags = {}

logger = getLogger()

def set_flags(values:Dict[str,Any]):
    '''
    This could probably be set up in a more dynamic way but it seems more instructive to explicitly
    define flags so they can be mildly categorized compared to how disorganized the gui values dict is

    :param values:
    :return:
    '''
    global flags
    
    #region: Configuration
    flags['USE_SECURE_KEYRING'] = values['use_secure_keyring'] # Use system credential store via the keyring module
    flags['IGNORE_DONEFILES'] = False                          # Ignore .done files in observation folders
                                                               #  i.e., treat as un-uploaded observation
    flags['GPX_DIR_NAME'] = 'gpx'                              # easier to skip this folder in a few places
    flags['GEOTAG_TIMESTAMP_WINDOW'] = values['geotag_match_window'] # value +- the observation's observed_on timestamp a gpx timestamp must fall to count as a match
    #region: Processing batch level
    flags['USE_PER_BATCH_METADATA'] = False       # Unused; Allow usage of meta-data that applies universally e.g., tag for a bioBlitz event
    flags['WRITE_KEYFILE'] = False                # Unused; The key file will be a delimited file that allows for manual
                                                  #   addition of data to some or all observations in a batch

    #endregion
    #region: Processing observation level
    flags['GEOTAG_PRIMARY'] = geotag_methods.get_method(values) # GPX, EXIF, manual source for geotag
    flags['GEOTAG_FALLBACK'] = values['geotag_fallback_flag']   # If the selected geotag source has no data, try the other as a backup
    flags['GEOTAG_PRIVACY'] = values['geotag_privacy']          # Private/public/obscured
    flags['GEOTAG_ACCURACY'] = values['geotag_acc']             # Accuracy of geotag rendering in meters
    flags['APPLY_PROJECT_RULES'] = True                         # Evaluate observations for project membership
    #endregion

    logger.info('Flags set')



#region: data structures
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


class geotag_privacy(Enum):
    # TODO: Implement in gui and observation processing
    open = 'Public'
    obscured = 'Obscured'
    private = 'Private'

tooltips = {
    'use_secure_keyring'    : 'Pull credentials from the OS\'s secure password store',
    'api_user'              : 'iNaturalist username',
    'api_pass'              : 'iNaturalist password',
    'api_id'                : 'iNaturalist API ID',
    'api_secret'            : 'iNaturalist API secret',
    'geotag_primary_gpx'    : 'Use GPX files as primary geotagging data source',
    'geotag_primary_exif'   : 'Use EXIF metadata per image as primary geotagging data source',
    'geotag_primary_manual' : 'Assign no geotagging data programmatically',
    'geotag_fallback_flag'  : 'If primary geotagging data source has no data, try the other source',
    'geotag_match_window'   : 'GPX coordinate must be timestamped +- this value in hours to constitute a match to an observation',
    'geotag_privacy'        : 'Open privacy allows any user to see the exact coordinates of your observation.\n' +\
                              'Obscured privacy means users will see an observation within a broad geographic area \n' + \
                              'Private means that no location information will be displayed at all\n' + \
                              'Obscured privacy is recommended; please consult the documentation before using Open privacy',
    'use_keyfile'           : '(Unused) Write a keyfile that can be used to manipulate observations\' data before consuming it ' +\
                              'and submitting the updated observations' ,
    'geotag_acc'            : 'Radius in meters of the accuracy circle around your observation coordinates',
    'path_working'          : 'Top level path the application will scan for observations and gpx files' ,
    'wrk_btn'               : 'Browse for the path your observations are in',
    'path_key'              : '(Unused) Path to read and write the keyfile ',
    'key_btn'               : '(Unused)Browse for a path for the keyfile',
    'path_meta'             : '(Unused) Path to find other metadata files',
    'mta_btn'               : '(Unused) Browse for metadata file path',
    'Begin processing'      : 'Begin processing',
    'Exit'                  : 'Exit'
}

#endregion