from gzip import READ
from typing import List
import constants as CONST


class _3497xA:
    
    def __init__(self, name):
        self.name = name
        self.channel_list = dict.fromkeys(CONST.FUNCTIONS)
        self.scan_list = '(@'

    def addChannel(self, channel, function):
        self.channel_list[function] += channel + ','
        return self.channel_list

    def clearChannels(self):
        for function in self.channel_list.keys:
            self.channel_list[function] = ''

        return self.channel_list

    def configure(self) -> str:
        ''' Returns SCPI command for configuration of all active channels. Also initializes scan_list.'''
        cmd = ''
        for idx, function in enumerate(self.channel_list.keys):
            if self.channel_list[function]:
                # Adds command command and removes trailing comma
                cmd += f"CONF:{CONST.CONF_CMDS[idx]} (@{self.channel_list[function][:-1]}\n)"
                self.scan_list += self.channel_list[function]


        self.scan_list = f'{self.scan_list[:-1]})'
        return cmd

    def scan(self) -> str:
        '''Returns SCPI command for preparing a scan on all active channels.'''
        return f"{CONST.SCAN_CMD} {self.scan_list}\n"

    def trigConfig(self, trig_num=1, trig_interval=0) -> str:
        '''Returns SCPI command for setting number of triggers and trigger interval'''
        return (
            f"{CONST.TRIG_SOUR} TIMER\n",
            f"{CONST.TRIG_COUNT} {trig_num}\n",
            f"{CONST.TRIG_TIMER} {trig_interval}\n"
        )

    def run() -> str:
        return f"{CONST.READ}\n"
