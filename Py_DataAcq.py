import pyvisa

rm = pyvisa.ResourceManager()
DMM = rm.open_resource('TCPIP0::169.254.208.22::inst0::INSTR')

DMM.write("*RST")

# configure channels


# read channels

# print data


print(DMM.write("SYST:ERR?"))
print(DMM.read())