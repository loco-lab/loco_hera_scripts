# scraps from ipython term

# test 1: turn phase switching off and on a few times for repeatbilit y
s.phase_switch.enable_mod(); s.phase_switch.enable_demod()
s.phase_switch.set_delay(0)
s.sync.arm_sync()
PS=True
D=[];PSlog=[]
for i in range(5):
    if PS: #if on, turn off
        s.phase_switch.disable_mod();s.phase_switch.disable_demod()
        PS=False
    else:
        s.phase_switch.enable_mod();s.phase_switch.enable_demod()
        PS=True
    print("reading corr number",i)
    %time D.append(s.corr.get_new_corr(0,1))
    PSlog.append(PS)
filename = 'herasnap.'+datetime.datetime.now().strftime('%Y-%m-%d-%H%M')+'
.npz'
print('saving to:',filename)
np.savez(filename,D=D,PSlog=PSlog)
#remove 20dB of attenuation from systematic



# test 2: cycles through 3000 walsh delay settings. Long, takes 20h
s.phase_switch.enable_mod(); s.phase_switch.enable_demod()
delays = np.arange(0,3000,1)
D=[]; i=0; curr_delays=[]
for n,d in enumerate(delays):
    print("setting delay to",d)
    s.phase_switch.set_delay(d)
    curr_delays.append(d)
    s.sync.arm_sync()#TODO add a local reset so a master reset isn't requi
red
    print("reading corr",n, "in file",i)
    %time D.append(s.corr.get_new_corr(0,1))
    print("mean sys 280-312:",np.mean(D[-1][280:312].real))
    i +=1
    if i==100:
        filename = '8July2022_longdelay/herasnap.'+str(i)+'.'+datetime.dat
etime.now().strftime('%Y-%m-%d-%H%M')+'.npz'
        print('saving to:',filename)
        np.savez(filename,D=D,delays=curr_delays)
        i=0
        curr_delays=[]; D=[]


