# Imports
import os
from typing import Optional

import PySimpleGUI as sg
import bashstuff as bs

sg.set_options(font='Default 18')

images = bs.getImages()
#print(images)

# layout
def main():
    tagdropdown = ["Find:NominalPilot", "Find:OtrSmoke", "Find:NominalSearchEx", "Find:NominalDetails",
                   "Find:NominalAllImageFile", "Find:NominalSearhPlusImage",
                   "Find:NominalDetailsPlusImage", "Find:DataReference" "Find:Swagger", "Find:Swagger-nominal-only",
                   "Find:NominalPdf",
                   "Find:NominalFingerPrint", "Tdawn:TravelSearch", "Tdawn:TravelDetails", "Smv:SmvVehicleSearch",
                   "Smv:SmvVehicleDetails",
                   "Sltd:SltdSearch", "Sltd:SltdDetails"]
    layout = [
        [sg.Text('What is the name of your drone app:                  '),
         sg.Radio('drone', 'dronegrp', key='-R1-', default=True, enable_events=True),
         sg.Radio('drone1', 'dronegrp', key='-R2-', enable_events=True)],
        [sg.Text('Enter the sprint number (e.g. 47_full, 47_pilot):'),
         sg.Input(key='-INSprintNo-', enable_events=True)],
        [sg.T('_' * 90)],

        [sg.Frame('Filter either Tags, Tests or None',
                  [[sg.Radio('None', 'mvnfilter', key='-F1-', default=True, enable_events=True),
                    sg.Radio('Tags', 'mvnfilter', key='-F2-', enable_events=True),
                    sg.Radio('Tests', 'mvnfilter', key='-F3-', enable_events=True)],
                   [sg.Text('Enter the test to run (e.g. GAP_001305):          ', visible=False, key='-INcliText-'),
                    sg.Input(key='-INclitest-', visible=False, enable_events=True, size=(950, 1), ),
                    sg.Text('Select tag from the list:                                   ', visible=False,
                            key='-ddtagstext-'),
                    sg.DropDown(tagdropdown, key='-ddtags-', visible=False, enable_events=True)],
                   ], key='-testframe-', size=(1100, 110), border_width=0)],

        [sg.T('_' * 90)],
        [sg.Text('Enter the latest drone build number:                '),
         sg.Input(key='-INdronebuild-', enable_events=True)],
        [sg.Text(size=(30, 1), key='-OUT Event-', text_color='yellow')],
        [sg.Text(key='-OUT Values-', text_color='red', auto_size_text=True)],
        [sg.Button('Run', visible=False), sg.Button('Exit')],
    ]

    # window initialisation
    window = sg.Window('I-DRONER', layout, keep_on_top=True, resizable=False)

    # loop
    while True:
        event, values = window.read()
        print(event, values)
        if event in (sg.WIN_CLOSED, 'Exit'):
            break

        INSprintNo = values['-INSprintNo-'].replace("-", "_")
        INclitest = values['-INclitest-'].replace("-", "_").upper()
        ddtags = values['-ddtags-']
        INdronebuild = values['-INdronebuild-']

        if values['-R1-']:
            dronevalue = 'drone'
        else:
            dronevalue = 'drone1'

        if event == '-F3-':
            window['-INcliText-'].update(visible=True)
            window['-INclitest-'].update(visible=True)
            window['-ddtagstext-'].update(visible=False)
            window['-ddtags-'].update(visible=False)
            window['-ddtags-'].update(value='')
            ddtags = ''

        if event == '-F2-':
            window['-ddtagstext-'].update(visible=True)
            window['-ddtags-'].update(visible=True)
            window['-INcliText-'].update(visible=False)
            window['-INclitest-'].update(visible=False)
            window['-INclitest-'].update(value='')
            INclitest = ''

        if event == '-F1-':
            window['-INcliText-'].update(visible=False)
            window['-INclitest-'].update(visible=False)
            window['-INclitest-'].update(value='')
            window['-ddtagstext-'].update(visible=False)
            window['-ddtags-'].update(visible=False)
            window['-ddtags-'].update(value='')
            ddtags = ''
            INclitest = ''

        if len(values['-INSprintNo-']) and len(values['-INdronebuild-']):
            window['Run'].update(visible=True)
            window['-OUT Values-'].update(text_color='light green')
        else:
            window['Run'].update(visible=False)
            window['-OUT Values-'].update(text_color='red')

        if event == '-INdronebuild-' and values['-INdronebuild-'] and values['-INdronebuild-'][-1] not in (
                '0123456789'):
            window['-INdronebuild-'].update(values['-INdronebuild-'][:-1])
            try:
                INdronebuild = INdronebuild[:-1]
            except:
                print('an error occured')

        # window['-OUT Event-'].update(f'event = {event}')

        runValue = f'{dronevalue} build promote -p nstest=\"st,{images}\" -p sprint_no={INSprintNo} -p tagcli={ddtags} -p testcli={INclitest} ileap/st-automation {INdronebuild} acp-notprod'
        runValueMsg = f'{dronevalue} build promote -p nstest=st -p sprint_no={INSprintNo} -p tagcli={ddtags} -p testcli={INclitest} ileap/st-automation {INdronebuild} acp-notprod'
        window['-OUT Values-'].update(runValueMsg)

        if event == 'Run':
            os.system(runValue)
            sg.Popup('You sent', f'{runValue}', keep_on_top=True, no_titlebar=True)
            window.close()


    # close
    window.close()


if __name__ == '__main__':
    main()