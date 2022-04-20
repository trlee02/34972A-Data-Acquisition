from faulthandler import disable
from lib2to3.pgen2.token import RPAR
from queue import Empty
import pyvisa
import PySimpleGUI as sg
from _3497xA import _3497xA
from typing import List
import time
import re

# SCPI Documentation here
# https://documentation.help/Keysight-34970A-34972A/Welcome.htm


def com(command):
    instr.write(command)



def comb_list(lists):
    return f'(@{",".join(lists)})'

rm = pyvisa.ResourceManager()
# instr = rm.open_resource('TCPIP0::169.254.9.72::inst0::INSTR')

'''UNCOMMENT THIS'''
# instr = rm.open_resource('USB0::0x0957::0x2007::MY57003725::0::INSTR')
# instr.timeout = 10000
# instr.write('INST:DMM ON')
# instr.write('*RST')
# instr.write('FORMAT:READING:CHAN ON')

# GUI setup
sg.theme('DarkTeal12')
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
    [sg.Multiline(size=(60, 10), key='RESULTS', disabled=True, autoscroll=True)],
    [sg.Button('START', size=(37, 1), key='START'), sg.Button('CLEAR RESULTS', size=(15,1), key=('CLR RESULTS'))],
    [sg.Button('READ', size=(54, 1), key='READ')],
    [sg.Multiline(size=(60,5), key='CMD LINE')],
    [sg.Button('RUN', size=(54,1), key='RUN')]
]


layout = [
    [
        sg.Column(channel_column),
        sg.VSeparator(),
        sg.Column(results_column)
    ]
]

def formatResults(results: str, channels: List[str]) -> str:
    temp_results = tuple(results.split(sep=','))
    paired_results = tuple(temp_results[x:x + 2] for x in range(0, len(temp_results), 2))

    channels.sort()
    chl_results = dict.fromkeys(channels, '')
    for pair in paired_results:
        chl_results[pair[1]]  = f"{chl_results[pair[1]]},{pair[0]}"
    
    return '\n'.join([f"{funct}:\t{re.split('^,',result)[1]}" for funct, result in chl_results.items()])
    # print(paired_results)


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
            dmm.addChannel(values['CHANNEL'], values['FUNCTION']) 
    elif event == 'CLEAR':
        window['CHANNEL LIST'].update('')
        dmm.clearChannels()
        print(dmm.channel_list)
    elif event == 'START':
        if not values['RESULTS']:
            com(dmm.start())
            com(dmm.fetch())
            results = formatResults(instr.read()[:-1], dmm.scan_list.split(','))
            window['RESULTS'].update(f"{results}")
        else: 
            com(dmm.start())
            com(dmm.fetch())
            results = formatResults(instr.read()[:-1], dmm.scan_list.split(','))
            
            
            
    elif event == 'CONFIG':
        com(dmm.configure())
        com(dmm.scan())
        print(dmm.configure())
        print(dmm.scan())
    elif event == 'SET':
        com(dmm.trigConfig(values['NUM TRIGS'], values['INTERVAL']))
        print(dmm.trigConfig(values['NUM TRIGS'], values['INTERVAL']))
    elif event == 'RUN':
        com(values['CMD LINE'])
        print(values['CMD LINE'])
    
    elif event == 'READ':
        filled = False
        if not values['RESULTS']:
            res = values['RESULTS']
        else:
            res = f"{values['RESULTS']}\n\n"
        for i in range(0, int(values['NUM TRIGS'])):
            com(dmm.start())
            com(dmm.fetch())
            results = formatResults(instr.read()[:-1], dmm.scan_list.split(','))
            
            if filled:
                res = (f"{res}\n\n{results}")
                window['RESULTS'].update(f"{res}")
            else:
                filled = True
                res += (f"{results}")
                
                window['RESULTS'].update(f"{res}")
            window.read(timeout=0)
            time.sleep(float(values["INTERVAL"]))


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
