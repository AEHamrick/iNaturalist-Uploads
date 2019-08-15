import sys
if sys.version_info[0] >= 3:
    import PySimpleGUI as sg
else:
    import PySimpleGUI27 as sg


from config import set_flags, flags, geotag_methods, tooltips
from obs_processing import *
from api_interactions import upload_obs, Auth
from custom_logging import create_logger

# TODO: tooltips
# TODO: Even out spacing
# TODO: Test logging
# TODO: Keyfile layout
# TODO: Upload in batches with a pause in between to check iNat and made adjustments if needed

logger = create_logger(Path(__file__).parent, 'iNat')


#region: config frame
config_layout = \
    [[sg.Checkbox('Use system keyring', key = 'use_secure_keyring', default=True, enable_events=True)],
     [sg.Text('User'),sg.In(default_text='',key='api_user', enable_events=True)],
     [sg.Text('Pass'),sg.In(default_text='',key='api_pass',password_char='*',disabled=True)],
     [sg.Text('App id'),sg.In(default_text='',key='api_id',size=(65, None),disabled=True)],
     [sg.Text('API secret'), sg.In(default_text='', key='api_secret',size=(65, None),disabled=True)]
    ]

config = sg.Frame('Config',
                   config_layout,
                   title_color=None,
                   background_color=None,
                   title_location=None,
                   relief=sg.DEFAULT_FRAME_RELIEF,
                   size=(None, None),
                   font=None,
                   pad=None,
                   border_width=None,
                   key=None,
                   tooltip=None,
                   right_click_menu=None,
                   visible=True)
#endregion


#region: options frame
options_layout = \
    [[sg.Text('Geotagging primary'),sg.Radio('GPX', "geotag", key = 'geotag_primary_gpx', default=True),
                                    sg.Radio('EXIF', "geotag", key='geotag_primary_exif'),
                                    sg.Radio('Manual (not recommended for large batches)', "geotag", key='geotag_primary_manual')],
     
     [sg.Checkbox('Geotag fallback (try other source)', key = 'geotag_fallback_flag', default=False,enable_events=True),
      sg.Text('Geotag match window'),sg.InputCombo([0,1,2,5,8,24], default_value=1, key='geotag_match_window', tooltip=None)],
     
     [sg.Text('Geotagging privacy'),sg.InputCombo(['Public','Obscured','Private'], default_value='Obscured', key='geotag_privacy', tooltip=None)],
     [sg.Checkbox('Use keyfile', key = 'use_keyfile', disabled=True)],
     #TODO: Make sure to note in the tooltips some sensible comparisons for these values
     [sg.Text('Geotagging accuracy'),sg.InputCombo([5,10,50,100,500], default_value=50, key='geotag_acc', tooltip=None)],
    ]

options = sg.Frame('Options',
                   options_layout,
                   title_color=None,
                   background_color=None,
                   title_location=None,
                   relief=sg.DEFAULT_FRAME_RELIEF,
                   size=(None, None),
                   font=None,
                   pad=None,
                   border_width=None,
                   key=None,
                   tooltip=None,
                   right_click_menu=None,
                   visible=True)

#endregion
#region: file nav frame

file_layout = \
    [[sg.Text('Working folder'),sg.In('',key='path_working'), sg.FolderBrowse(target='path_working',
                                                                             initial_folder='%UserProfile%\desktop',
                                                                              key='wrk_btn')],
     [sg.Text('Keyfile'), sg.In('', key='path_key',disabled=True), sg.FolderBrowse(target='path_key', disabled=True,
                                                                               initial_folder='%UserProfile%\desktop',
                                                                               key='key_btn')],
     [sg.Text('Global meta file'), sg.In('', key='path_meta',disabled=True), sg.FolderBrowse(target='path_meta', disabled=True,
                                                                               initial_folder='%UserProfile%\desktop',
                                                                               key='mta_btn')]
    ]

file = sg.Frame('Files',
                file_layout,
                title_color=None,
                background_color=None,
                title_location=None,
                relief=sg.DEFAULT_FRAME_RELIEF,
                size=(None, None),
                font=None,
                pad=None,
                border_width=None,
                key=None,
                tooltip=None,
                right_click_menu=None,
                visible=True)
#endregion

#region: progress bars frame
#TODO: Leave this til later
progress_layout = []

progress = sg.Frame('Progress',
                    progress_layout,
                    title_color=None,
                    background_color=None,
                    title_location=None,
                    relief=sg.DEFAULT_FRAME_RELIEF,
                    size=(None, None),
                    font=None,
                    pad=None,
                    border_width=None,
                    key=None,
                    tooltip=None,
                    right_click_menu=None,
                    visible=True)
#endregion

layout = [[config],
          [options, file],
          [sg.Submit('Begin processing')],
          [sg.Exit()]]

window = sg.Window('iNaturalist bulk upload', layout)

for k in window.AllKeysDict.keys():
    window.Element(k).Tooltip = tooltips[k]

logger.info('Entering event loop')
while True:                 # Event Loop
    event, values = window.Read()
    print(event, values)
    if event is None or event == 'Exit':
        break
    if event == 'Show':
        # Update the gui
        window.Element('_OUTPUT_').Update(values['_IN_'])
        logger.debug('Window updated')
        
    if event == 'use_secure_keyring':
        window.Element('api_pass').Update(disabled=  values['USE_SECURE_KEYRING'])
        window.Element('api_id').Update(disabled=  values['USE_SECURE_KEYRING'])
        window.Element('api_secret').Update(disabled=  values['USE_SECURE_KEYRING'])
        # TODO: When processing starts, make sure to update these fields after Auth populates, or popup and continue if
        #  it fails
        logger.debug('Credentials updated')
   
    if event == 'Begin processing':
        
        if values['path_working'] == '':
            msg = 'No working directory specified, nothing to do'
            logger.error(msg)
            sg.PopupError(msg,title='No working directory')
            continue
        logger.info('Here we go')
        set_flags(values)
        logger.debug('Flags set')
        auth = Auth(values['api_user'])

        window.Element('api_id').Update(auth.app_id)
        window.Element('api_secret').Update(auth.app_secret)
        logger.debug('Auth set')
        
        #Assemble observations from working folder with taxon, file(s), date, global values
        # TODO: Rework this to handle one obs or obs folder at a time so one bad file doesn't kill the batch before
        #   .done files are written
        
        obs = assemble_skeleton_observations(Path(values['path_working']))
        logger.info('{0} observations found'.format(str(len(obs))))
        
        #Run primary geotagging
        if not flags['GEOTAG_PRIMARY'] == geotag_methods.manual:
            logger.info('Starting {0} geotagging'.format(flags['GEOTAG_PRIMARY'].value))
            assign_coordinates_to_obs(obs, flags['GEOTAG_PRIMARY'], Path(values['path_working']))
            
            #Run secondary geotagging if applicable
            if flags['GEOTAG_FALLBACK']:
                logger.info('Starting fallback geotagging for {0} observations'.format(str(len([x for x in obs if not x.coordinates]))))
                
                assign_coordinates_to_obs(obs, geotag_methods.get_fallback_method(flags['GEOTAG_PRIMARY']), Path(values['path_working']))
    
        # TODO: Apply processing rules if indicated
        #process_rules(obs)
        # TODO: Apply project membership rules if indicated
        #process_project_rules(obs)
    
        # TODO: Generate skeleton keyfile
        # TODO: Consume completed keyfile
        
        #Transmit observations
        logger.info('Transmitting observations')
        for o in obs:
            upload_obs(o, auth.token)
        
        #Create .done files
        ok_result = [x for x in obs if x.inat_result == 'ok']
        logger.info('{0} ok response(s) received out of {1} observation(s)'.format(str(len(ok_result)),
                                                                            str(len(obs))))
        
        logger.info('Creating .done files for {0} ok responses'.format(str(len(ok_result))))
        for o in ok_result:
            (o.path / '.done').touch()
            
        logger.info('Finished with this batch')

logger.info('Exiting')
window.Close()