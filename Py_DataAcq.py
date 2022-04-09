from faulthandler import disable
from lib2to3.pgen2.token import RPAR
from queue import Empty
import pyvisa
import PySimpleGUI as sg
from _3497xA import _3497xA

# SCPI Documentation here
# https://documentation.help/Keysight-34970A-34972A/Welcome.htm


def com(command):
    DMM.write(command)


def comb_list(lists):
    return f'(@{",".join(lists)})'

# rm = pyvisa.ResourceManager()
# DMM = rm.open_resource('TCPIP0::169.254.208.22::inst0::INSTR')

# GUI setup
sg.theme('Dark Grey 3')
channel_column = [
    [sg.Text("Channel", size=(10,1)), sg.InputText(size=(12, 1), key='CHANNEL')],
    [sg.Text("Function", size=(10,1)), sg.InputText(size=(12, 1), key='FUNCTION')],
    [sg.Button('ADD', size=(22, 1), key='ADD')],
    [sg.Multiline(size=(23, 5), key='CHANNEL LIST')],
    [sg.Button('CONFIG', size=(22, 1), key='CONFIG')],
    [sg.Button('CLEAR', size=(22,1), key='CLEAR')],
    [sg.Text("Num Triggers", size=(10,1)), sg.InputText(size=(12, 1), key='NUM TRIGS')],
    [sg.Text("Interval(s)", size=(10,1)), sg.InputText(size=(12, 1), key='INTERVAL')],
    [sg.Button('SET', size = (22, 1), key='SET')]

]

results_column = [
    [sg.Text("Results")],
    [sg.Multiline(size=(40, 10), key='RESULTS', disabled=True)],
    [sg.Button('START', size=(20, 1), key='START'), sg.Button('CLEAR RESULTS', size=(15,1), key=('CLR RESULTS'))],
    [sg.Multiline(size=(40,5), key='CMD LINE')],
    [sg.Button('RUN', size=(37,1), key='RUN')]
]


layout = [
    [
        sg.Column(channel_column),
        sg.VSeparator(),
        sg.Column(results_column)
    ]
]


dmm = _3497xA("34972A")

window = sg.Window('Test', layout).Finalize()


# All commands right now are shown as print('COMMAND') right now to simulate real commands to the DMM 

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event in (None, 'Close Window'):  # if user closes window or clicks cancel
        break
    if event == 'ADD':
        if values['CHANNEL LIST']:
            window['CHANNEL LIST'].update(
                f"{values['CHANNEL LIST']}\n{values['FUNCTION']}:{values['CHANNEL']}") # Display new Channel
            dmm.addChannel(values['CHANNEL'], values['FUNCTION'])
        else:
            window['CHANNEL LIST'].update(
                f"{values['FUNCTION']}:{values['CHANNEL']}")
            scan_list += values['CHANNEL'] + ','
            dmm.addChannel(values['CHANNEL'], values['FUNCTION']) 
    elif event == 'CLEAR':
        window['CHANNEL LIST'].update('')
        dmm.clearChannels()
        print(dmm.channel_list)
        scan_list='(@'
    elif event == 'START':
        if not values['RESULTS']:
            window['RESULTS'].update(f"{values['RESULTS']}\n{dmm.run()}")
            print(dmm.run())
        else: 
            window['RESULTS'].update("Hello There!")
    elif event == 'CONFIG':
        print(dmm.configure())
        print(dmm.scan())
    elif event == 'SET':
        print(dmm.trigConfig(values['NUM TRIGS'], values['INTERVAL']))
    elif event == 'RUN':
        print(values['RUN'])





        


window.close()


# com("*RST")

# voltsDC_list = '101:103'
# freq_list = '104:106'

# # configure channels
# com(f"CONF:VOLT:DC (@{voltsDC_list})")
# print(f"CONF:VOLT:DC (@{voltsDC_list})")
# com(f"CONF:FREQ (@{freq_list})")

# # setup automated scan with channels
# com(f"ROUTe:SCAN {comb_list({voltsDC_list, freq_list})}")
# print(f"ROUTe:SCAN {comb_list({voltsDC_list, freq_list})}")
# # setup triggers
# com("TRIG:COUNT 3")
# com("TRIG:SOURce TIMER")
# com("TRIG:TIMER 3")

# # format output
# com("FORMAT:READING:CHAN ON")

# # query readings
# com("R?")

# # print data
# print(DMM.read())
