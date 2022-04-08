from faulthandler import disable
from queue import Empty
import pyvisa
import PySimpleGUI as sg

# SCPI Documentation here
# https://documentation.help/Keysight-34970A-34972A/Welcome.htm


def com(command):
    DMM.write(command)


def comb_list(lists):
    return f'(@{",".join(lists)})'

# rm = pyvisa.ResourceManager()
# DMM = rm.open_resource('TCPIP0::169.254.208.22::inst0::INSTR')

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
    [sg.Button('START', size=(36, 1), key='START')]
]


layout = [
    [
        sg.Column(channel_column),
        sg.VSeparator(),
        sg.Column(results_column)
    ],

]

scan_list = '(@'
dc_volts = '(@'
ac_volts = '(@'
freq = '(@'
period = '(@'
ohms = '(@'
ohms_4W = '(@'
temp = '(@'
dc_cur = '(@'
ac_cur = '(@'

channel_list = [
    dc_volts,
    ac_volts,
    freq,
    period,
    ohms,
    ohms_4W,
    temp,
    dc_cur,
    ac_cur
]

function_list = [
    'DC Volts',
    'AC Volts',
    'Frequency',
    'Period',
    'Ohms',
    'Ohm 4W',
    'Temperature',
    'DC Current',
    'AC Current'
]




def assign_functions(active_channels):
    channels = active_channels.splitlines()
    for a_channel in channels:
        for idx, function in enumerate(function_list):
            if function in a_channel:
                channel_list[idx] += a_channel.split(':',1)[1] + ','
        
        
        

window = sg.Window('Test', layout).Finalize()
# window.Maximize()
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event in (None, 'Close Window'):  # if user closes window or clicks cancel
        break
    if event == 'ADD':
        if values['CHANNEL LIST']:
            window['CHANNEL LIST'].update(
                f"{values['CHANNEL LIST']}\n{values['FUNCTION']}:{values['CHANNEL']}") # Display new Channel
            scan_list += values['CHANNEL'] + ',' # append new channel to scan list
        else:
            window['CHANNEL LIST'].update(
                f"{values['FUNCTION']}:{values['CHANNEL']}")
            scan_list += values['CHANNEL'] + ','
    elif event == 'CLEAR':
        window['CHANNEL LIST'].update('')
        scan_list='(@'
    elif event == 'START':
        if not values['RESULTS']:
            window['RESULTS'].update(f"{values['RESULTS']}\nHello There!")
        else: 
            window['RESULTS'].update("Hello There!")
    elif event == 'CONFIG':
        # Read the channel list
        # Assign channels to functions
        assign_functions(values["CHANNEL LIST"])
        print(channel_list)
        # configure all channels in functions




        


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
