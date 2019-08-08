import sys
if sys.version_info[0] >= 3:
    import PySimpleGUI as sg
else:
    import PySimpleGUI27 as sg

from creds import iNat
from obs_processing import *
#TODO: tooltips
#TODO: Even out spacing
tooltips = {}

#region: config frame
#TODO: Store some defaults somewhere and pull in here
config_layout = \
    [[sg.Text('User'),sg.In(default_text=iNat.USER.value,key='api_user')],
     [sg.Text('Pass'),sg.In(default_text=iNat.PWD.value,key='api_pass',password_char='*')],
     [sg.Text('API key'),sg.In(default_text=iNat.APP_ID.value,key='api_key',size=(65, None))],
     [sg.Text('API secret'), sg.In(default_text=iNat.SECRET.value, key='api_secret',size=(65, None))]
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
    [[sg.Text('Geotagging primary'),sg.Radio('GPX', "geotag", key = 'geotag_gpx', default=True), sg.Radio('EXIF', "geotag", key='geotag_exif')],
     [sg.Checkbox('Geotag fallback', key = 'geotag_fallback_flag', default=False,enable_events=True)],
     [sg.Text('Geotagging fallback'),sg.Radio('Try other source', "geotag_fallback", key = 'geotag_other_one', disabled=True),
                                     sg.Radio('None', "geotag_fallback", key='geotag_none', default=True, disabled=True)],
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
    if event == 'geotag_fallback_flag':
        #enable/disable the fallback dialog appropriately
        window.Element('geotag_other_one').Update(disabled= not values['geotag_fallback_flag'])
        window.Element('geotag_none').Update(disabled= not values['geotag_fallback_flag'])
        pass
    if event == 'Begin processing':
        pass
    
        #Assemble observations from working folder with taxon, file(s), date, global values
        obs = assemble_skeleton_observations(values['path_working'])
        #Run primary geotagging
    
        #Run secondary geotagging if selected
    
        # TODO: Generate skeleton keyfile
        
        # TODO: Consume completed keyfile
    
        #Establish API connection
    
        #Transmit observations


window.Close()