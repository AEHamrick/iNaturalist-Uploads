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
    flags['USE_SECURE_KEYRING'] = values['USE_SECURE_KEYRING'] # Use system credential store via the keyring module
    flags['IGNORE_DONEFILES'] = False                          # Ignore .done files in observation folders
                                                               #  i.e., treat as un-uploaded observation
    flags['GPX_DIR_NAME'] = 'gpx'                              # easier to skip this folder in a few places
    flags['GEOTAG_TIMESTAMP_WINDOW'] = 1 # value +- the observation's observed_on timestamp a gpx timestamp must fall to count as a match
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

#endregion