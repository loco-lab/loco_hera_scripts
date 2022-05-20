import hera_corr_f
from hera_corr_f import SnapFengine
import time 
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='Fem long observation. Script assumes one FEM/PAM input into N0/E2 on SNAP')
parser.add_argument("hostname", help = "ip address of the SNAP board to initialize")
#parser.add_argument("--bitfile", help = ".fpg file to program board with", default = None)
parser.add_argument("filename", help = "name of .npz file to write")
parser.add_argument("--acclen", help = "accumulation len of on board correlator", default = 16384)
parser.add_argument("--tobs", help = "time in seconds of observation", default = 3600)
parser.add_argument("--femstate", help = "state of the fem switch", default = "load")
args = parser.parse_args()

s = SnapFengine(args.hostname, redishost=None)
s.corr.set_acc_len(args.acclen)
fem1 = s.fems[0]
fem1.switch(args.femstate)

tstart = time.time()
tend = tstart+int(args.tobs)
t = time.time()
datastacks = []
times = []
while t < tend:
    t = time.time()
    corrs = {}
    for i in range(6):
        for j in range(i,6):
            corrs[(i,j)] = s.corr.get_new_corr(i,j)

    datastack = np.vstack(corrs.values())
    datastacks.append(datastack)
    times.append(t)

datas = np.dstack(datastacks)

np.savez(args.filename, data=datas, times=times, bls=corrs.keys())

