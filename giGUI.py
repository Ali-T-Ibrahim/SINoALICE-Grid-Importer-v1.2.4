import PySimpleGUI as sg
import cv2
from gridimporter import *
import gspread

#path = sg.popup_get_file('Select the grid you would like to import', 'Grid Importer')
sg.theme('Dark Blue')
close = False

inputs = [[sg.Text('Select image of grid:')],
          [sg.Input(default_text='Browse for image...', readonly=True,
                    disabled_readonly_background_color='#335267', key='-PATH-'), sg.FileBrowse()],

          [sg.Text('Select Class:'), sg.Text('Select number of weapons in grid:',
                                             justification='right', size=(28,1))],
          [sg.Combo(['Select Class...', 'Paladin', 'Crusher',
                     'Breaker', 'Gunner', 'Sorcerer', 'Minstrel',
                     'Cleric'], default_value='Select Class...',readonly=True, size=(13,8),key='-CLASS-'),

           sg.Combo(['Select Number...', '20', '19', '18', '17',
                     '16', '15', '14', '13', '12', '11', '10', '9',
                     '8', '7', '6', '5', '4', '3', '2', '1'],
                    default_value='Select Number...', auto_size_text=True,
                    readonly=True, size=(15,6), pad=((10, 0), 0),key='-GRIDNUM-')],
          
          [sg.Text('Note: Instructions on github page if needed', text_color='Red'),
           sg.Button(button_text='Next', pad=((34, 5), 0),key='FIRSTOK', auto_size_button=True), sg.Button(button_text='Cancel', key='-EXIT-')]
    ]


window = sg.Window('Grid Importer v1.0.1', inputs, button_color=('white', '#3e455c'))
weplist = []

while True:
    
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED or event == '-EXIT-' or event == '-EXIT1-':
        break
    
    elif event == 'FIRSTOK':
        try:
            Sclass = values['-CLASS-']    
            num = int(values['-GRIDNUM-'])
            path = r'{}'.format(values['-PATH-'])

            if values['-CLASS-'] == 'Select Class...':
                sg.popup('Warning', 'Please select a class.')
            elif values['-GRIDNUM-'] == 'Select Number...':
                sg.popup('Warning', 'Please select the number of weapons in your grid.')
            else:
                window.close()
                gridimg = cv2.imread(path)
                gridimg = cv2.resize(gridimg, (492,784))
                grid_viewer_column = [[sg.Text('Loading...')]]
                
                weapon_list = ['\n\nWeapons will appear here when found']
                weapon_listing_column =[[sg.ProgressBar(num, orientation='h', size=(20,50), pad=((85, 0), (0,35)), key='-PROGRESS-')],
                                        [sg.Button('Find\nWeapons', size=(15, 3), pad=((14, 10), (0,35)),
                                                   font=('Bold', '15'), disabled=False,key='-ACTIVATE-'),
                                         sg.Button('Send To\nAnalyzer', size=(15, 3), pad=((8, 0), (0,35)),
                                                   font=('Bold', '15'), disabled=True,key='-SEND-')],
                                        
                                        [sg.Text('Weapon List:', font=('Bold', '25'),justification='center', size=(19,1))],
                                        [sg.Listbox(weapon_list, size=(35,20), auto_size_text=False,
                                                    no_scrollbar=True, font=('Bold', '15'), key='-WEPBOX-')]
                                        ]
                
                layout = [[sg.Column(grid_viewer_column),
                          sg.VSeperator(color='white', pad=((450, 0),(0,0))),
                          sg.Column(weapon_listing_column)]
                          ]
                
                window = sg.Window('Grid Importer v1.0.1', layout, finalize=True, resizable=False,
                                   margins=((0), (50)), button_color=('white', '#3e455c'))
                winx, winy = window.CurrentLocation()
                cv2.imshow("MyGrid",gridimg)
                cv2.moveWindow('MyGrid', winx+20, winy+40)
                cv2.setWindowProperty('MyGrid', cv2.WND_PROP_TOPMOST, 1)
        except:
            sg.popup('Warning', 'Please make sure all entries are valid.')

    elif event == '-ACTIVATE-':
        findWeapons(gridimg, window, weplist, Sclass,num)
        window.FindElement('-ACTIVATE-').Update(disabled=True)
        window.FindElement('-SEND-').Update(disabled=False)
        window.refresh()

    elif event == '-SEND-':
        analyzein = [[sg.Text('Enter URL of your grid analyzer copy:', key='-URL-')],
                      [sg.Input()],
                      [sg.Text('Enter name of the worksheet to send data to:', key='-WORKSHEET-')],
                      [sg.Input()],
                      [sg.Text('The worksheet is the tab on the bottom of the spreadsheet', text_color='Red')],
                      [sg.Text('WARNING: worksheet name is case sensetive', text_color='Red')],
                      [sg.Button('Confirm', key='-CONFIRM-'), sg.Button(button_text='Cancel', key='-EXIT1-')]
                      ]
        window = sg.Window('Grid Importer v1.0', analyzein, finalize=True, no_titlebar=True,
                            keep_on_top=True, button_color=('white', '#3e455c'))

    elif event == '-CONFIRM-':
        #stats = getStats()
        url = values[0]
        worksheet = values[1]
        window.close()
        updateGrid(url, worksheet, weplist, Sclass)
        close = True

#exit loop don't touch
window.close()























































