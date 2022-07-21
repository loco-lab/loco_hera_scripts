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
parser.add_argument("--phase_switch", action="store_true",
        help='activate phase switching. Edit script to change from default settings.')
parser.add_argument('--eq',default=400,type=int,
        help='4bit eq. default=400. if your spectra be quantized, increase me')
parser.add_argument('--acc_len',type=int,default=2097152,
        help='cycle time *step size * walsh length mod biggest possible 32 bit number times nchan  = (((2^18)*8) mod (2^32*1024) = 2097152. set to -1 to skip setting') 

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
#s.pfb.set_fft_shift(0xffff)
s.pfb.set_fft_shift(0x1557)

for i in range(6):
    s.eq.set_coeffs(i, np.ones(s.eq.ncoeffs)*args.eq)
    if args.phase_switch:
        print("uploading walsh patterns.")
        s.phase_switch.set_walsh(i,8,i,0) #8 walshes, go as fast as possible
        print("it is now possible to enable phase switching")
print("setting accumulation length")
if args.acc_len!=-1:
    s.corr.set_acc_len(args.acc_len)

