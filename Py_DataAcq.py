import pyvisa

# SCPI Documentation here
# https://documentation.help/Keysight-34970A-34972A/Welcome.htm

def com(command):
    DMM.write(command)

def comb_list(lists):
    return f'(@{",".join(lists)})'

rm = pyvisa.ResourceManager()
DMM = rm.open_resource('TCPIP0::169.254.208.22::inst0::INSTR')

com("*RST")

voltsDC_list = '101:103'
freq_list = '104:106'

# configure channels
com(f"CONF:VOLT:DC (@{voltsDC_list})")
print(f"CONF:VOLT:DC (@{voltsDC_list})")
com(f"CONF:FREQ (@{freq_list})")

# setup automated scan with channels
com(f"ROUTe:SCAN {comb_list({voltsDC_list, freq_list})}")
print(f"ROUTe:SCAN {comb_list({voltsDC_list, freq_list})}")
# setup triggers
com("TRIG:COUNT 3")
com("TRIG:SOURce TIMER")
com("TRIG:TIMER 3")

# format output
com("FORMAT:READING:CHAN ON")

# query readings
com("R?")

# print data
print(DMM.read())


