from gzip import READ
from typing import List
import constants as CONST
import re


class _3497xA:
    
    def __init__(self, name):
        self.name = name
        self.channel_list = dict.fromkeys(CONST.FUNCTIONS, '')
        self.scan_list = ''

    def addChannel(self, channel: str, function: str):
        self.channel_list[function] += channel + ','
        return self.channel_list

    def clearChannels(self):
        for function in self.channel_list.keys():
            self.channel_list[function] = ''

        return self.channel_list

    def configure(self) -> str:
        ''' Returns SCPI command for configuration of all active channels. Also initializes scan_list.'''
        self._scan_list = ''
        cmd = ''
        for idx, function in enumerate(self.channel_list.keys()):
            if self.channel_list[function]:
                # Adds command command and removes trailing comma
                cmd += f"{CONST.CONF_CMDS[idx]} (@{self.channel_list[function][:-1]})\n"
                self._scan_list += self.channel_list[function]


        self._scan_list = f'{self._scan_list[:-1]}'
        return f"{cmd}FORMAT:READING:CHAN ON\n"

    def scan(self) -> str:
        '''Returns SCPI command for preparing a scan on all active channels.'''
        return f"{CONST.SCAN_CMD} (@{self._scan_list})"

    def trigConfig(self, trig_num=1, trig_interval=0) -> str:
        '''Returns SCPI command for setting number of triggers and trigger interval'''
        return (
            f"{CONST.TRIG_SOUR} TIMER\n"
            f"{CONST.TRIG_COUNT} {trig_num}\n"
            f"{CONST.TRIG_TIMER} {trig_interval}"
        )

    def start(self) -> str:
        return f"{CONST.INIT}"

    def fetch(self) -> str:
        return f"{CONST.FETCH}"

    # def read(self, num_trig, trig_interval) -> str:
    #     for i in range(0, num_trig):
            


    @property
    def scan_list(self) -> str:
        _list = self._scan_list.split(sep=',')
        full_list = ''
        for chl in _list:
            if ':' in chl:
                temp = list(range(int(chl.split(':')[0]), int(chl.split(':')[1] )+ 1))
                  
                full_list+=f"{(','.join(str(item) for item in temp))},"
            else: 
                a = [f'{chl}']
                full_list+=f"{chl},"

        return re.split(',$',full_list)[0]
    
    @scan_list.setter
    def scan_list(self, value):
        self._scan_list = value

