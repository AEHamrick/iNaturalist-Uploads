import sys
if sys.version_info[0] >= 3:
    import PySimpleGUI as sg
else:
    import PySimpleGUI27 as sg

#TODO: Oops, having this in gitignore is more secure but hampers working on multiple devices; sort that
from creds import iNat
from config import Auth
from obs_processing import *
from api_interactions import upload_obs

#TODO: tooltips
#TODO: Even out spacing
# TODO: Flags method
tooltips = {}

#region: config frame
# TODO: Get the credentials to update when user is changed
# TODO: Get rid of hardcoded creds
config_layout = \
    [[sg.Checkbox('Use system keyring', key = 'USE_SECURE_KEYRING', default=True, enable_events=True)],
     [sg.Text('User'),sg.In(default_text=iNat.USER.value,key='api_user')],
     [sg.Text('Pass'),sg.In(default_text=iNat.PWD.value,key='api_pass',password_char='*',disabled=True)],
     [sg.Text('App id'),sg.In(default_text=iNat.APP_ID.value,key='api_id',size=(65, None),disabled=True)],
     [sg.Text('API secret'), sg.In(default_text=iNat.SECRET.value, key='api_secret',size=(65, None),disabled=True)]
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
     
     [sg.Checkbox('Geotag fallback (try other source)', key = 'geotag_fallback_flag', default=False,enable_events=True)],
     
     [sg.Text('Geotagging privacy'),sg.InputCombo(['Public','Obscured','Private'], default_value='Obscured', key='geotag_privacy', tooltip=None)],
     [sg.Checkbox('Use keyfile', key = 'keyfile', disabled=True)],
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
                                                                             initial_folder='%UserProfile%\desktop')],
     [sg.Text('Keyfile'), sg.In('', key='path_key',disabled=True), sg.FolderBrowse(target='path_key', disabled=True,
                                                                               initial_folder='%UserProfile%\desktop')],
     [sg.Text('Global meta file'), sg.In('', key='path_meta',disabled=True), sg.FolderBrowse(target='path_meta', disabled=True,
                                                                               initial_folder='%UserProfile%\desktop')]
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

while True:                 # Event Loop
    event, values = window.Read()
    print(event, values)
    if event is None or event == 'Exit':
        break
    if event == 'Show':
        # change the "output" element to be the value of "input" element
        window.Element('_OUTPUT_').Update(values['_IN_'])
    
    if event == 'USE_SECURE_KEYRING':
        window.Element('api_pass').Update(disabled=  values['USE_SECURE_KEYRING'])
        window.Element('api_id').Update(disabled=  values['USE_SECURE_KEYRING'])
        window.Element('api_secret').Update(disabled=  values['USE_SECURE_KEYRING'])
        
    if event == 'Begin processing':
    
        auth = Auth(values['api_user'])
        
        #Assemble observations from working folder with taxon, file(s), date, global values
        obs = assemble_skeleton_observations(Path(values['path_working']))
        #Run primary geotagging
        if not values['geotag_primary_manual']:
            assign_coordinates_to_obs(obs,'{0}{1}'.format('GPX' if values['geotag_primary_gpx'] else '', # TODO: This is kind of hacky?
                                                          'EXIF' if values['geotag_primary_exif'] else ''),
                                  values)
            #Run secondary geotagging if applicable
            if values['geotag_fallback_flag']:
                assign_coordinates_to_obs(obs, '{0}{1}'.format('GPX' if not values['geotag_primary_gpx'] else '',
                                                               'EXIF' if not values['geotag_primary_exif'] else ''),
                                      values)
    
        # TODO: Apply processing rules if indicated
        #process_rules(obs)
        # TODO: Apply project membership rules if indicated
        #process_project_rules(obs)
    
        # TODO: Generate skeleton keyfile
        # TODO: Consume completed keyfile
        
        #Transmit observations
        for o in obs:
            upload_obs(o)
        
        #Create .done files
        for o in [x for x in obs if x.inat_result == 'ok']:
            (o.path / '.done').touch()


window.Close()