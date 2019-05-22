import sys
if sys.version_info[0] >= 3:
    import PySimpleGUI as sg
else:
    import PySimpleGUI27 as sg

#TODO: tooltips
tooltips = {}

#region: options frame
options_layout = \
    [[sg.Text('Geotagging method'),sg.Radio('GPX', "geotag", key = 'geotag_gpx', default=True), sg.Radio('EXIF', "geotag", key='geotag_exif')],
     [sg.Text('Geotagging privacy'),sg.InputCombo(['Public','Obscured','Private'], default_value='Obscured', key='geotag_privacy', tooltip=None)],
     [sg.Checkbox('Use keyfile', key = 'keyfile', disabled=True),sg.Checkbox('Geotag fallback', key = 'geotag_fallback', disabled=True)],
     #TODO: Make sure to note in the tooltips some sensible comparisons for these values
     [sg.Text('Geotagging accuracy'),sg.InputCombo([5,10,50,100,500], default_value='Obscured', key='geotag_privacy', tooltip=None)],
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




layout = [[options, file],
          [sg.Ok(),sg.Cancel()]]

window = sg.Window('Window Title', layout)

while True:                 # Event Loop
  event, values = window.Read()
  print(event, values)
  if event is None or event == 'Exit':
      break
  if event == 'Show':
      # change the "output" element to be the value of "input" element
      window.Element('_OUTPUT_').Update(values['_IN_'])

window.Close()