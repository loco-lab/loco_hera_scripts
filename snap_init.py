import hera_corr_f
from hera_corr_f import SnapFengine
import numpy as np 
import argparse

parser = argparse.ArgumentParser(description='Inputs for snap startup')
parser.add_argument("hostname", help = "ip address of the SNAP board to initialize")
parser.add_argument("--bitfile", help = ".fpg file to program board with", default = None)
#parser.add_argument("--ref", help = "reference frequency for clocking", default = 10)
#parser.add_argument("--samplerate", help = "Sampling Rate for ADC", default = 500)
#parser.add_argument("--numchannel", help = "Demux mode for SNAP, 1ch = demux by 4, 2ch = demux by 2, 4ch = no demux", dfault = 4)
args = parser.parse_args()



s = SnapFengine(args.hostname, redishost=None)

if args.bitfile == None:
    s.fpga.transport.prog_user_image()
else:
    s.fpga.transport.upload_to_ram_and_program(str(args.bitfile))

s.initialize_adc()


while True:
    try:
        s.align_adc()
    except:
        continue
    else:
        break

print("init")
s.initialize()
s.sync.arm_sync()
s.pfb.set_fft_shift(0xffff)

for i in range(6):
    s.eq.set_coeffs(i, np.ones(s.eq.ncoeffs)*400)


