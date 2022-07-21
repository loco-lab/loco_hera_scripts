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

#plot this kind of data
In [628]: plt.figure()
     ...: data = np.load('herasnap.2022-07-13-1445.npz')
     ...: for i,d in enumerate(data['D']):
     ...:     if data['PSlog'][i]:color='tab:blue'
     ...:     else: color='tab:orange'
     ...:     plt.plot(dB(np.abs(d)),color=color)
     ...: plt.title('blue=PS ON, orange=PS OFF\n eq=2047 (max)')
     ...: plt.xlabel('chan [out of 0-250MHz]')
     ...: plt.ylabel('amp [db]')
     ...: plt.show()

#heres a more advanced one 
In [705]: plt.figure()
     ...: data = np.load('herasnap.2022-07-14-1144.npz')
     ...: data_sys_off = np.load('herasnap.2022-07-14-1232.npz')
     ...: data_walsh4 = np.load('herasnap.2022-07-14-1304.npz')
     ...: for i,d in enumerate(data['D']):
     ...:     if data['PSlog'][i]:color='tab:blue'
     ...:     else: color='tab:orange'
     ...:     plt.plot(dB(np.abs(d)),color=color)
     ...: plt.plot(dB(np.abs(data_sys_off['D'][1])),color='tab:blue',ls='--')
     ...: plt.plot(dB(np.abs(data_sys_off['D'][0])),color='tab:orange',ls='--')
     ...: plt.plot(dB(np.abs(data_walsh4['D'][1])),color='tab:blue',ls=':')
     ...: plt.title('blue=PS ON, orange=PS OFF, dash=SYS OFF\n dotted=walsh4')
     ...: plt.xlabel('chan [out of 0-250MHz]')
     ...: plt.ylabel('dB')
     ...: plt.grid()
     ...: plt.show(block=False)

In [761]: #plot the residual (PS ON - NO SYS) for different power levels
     ...: data_lo = np.load('herasnap.2022-07-14-1144.npz')
     ...: data_hi = np.load('herasnap.2022-07-14-1802.npz')
     ...: data_sys_off=np.load('herasnap.2022-07-14-1232.npz')
     ...: plt.figure()
     ...: for i,d in enumerate(data_sys_off['D']): #I THINK these all have 4 integra
     ...: tions
     ...:     if data['PSlog'][i]:color='tab:blue'
     ...:     else: color='tab:orange'
     ...:     res_mag_hi = np.abs(data_hi['D'][i]) - np.abs(d)
     ...:     res_mag_lo = np.abs(data_lo['D'][i]) - np.abs(d)
     ...:     plt.plot(dB(res_mag_hi),ls = '-',color=color)
     ...:     plt.plot(dB(res_mag_lo),ls=':',color=color)
     ...: plt.title('ang(sys)-abs(no sys)\n solid=reference, dotted=-5dB')
     ...: plt.show(block=False)


#a complicated beasty that compares switching and sys on off
In [663]: plt.figure()
     ...: data = np.load('herasnap.2022-07-13-1510.npz')
     ...: data_sys_off = np.load('herasnap.2022-07-13-1445.npz')
     ...: for i,d in enumerate(data['D']):
     ...:     if data['PSlog'][i]:color='tab:blue'
     ...:     else: color='tab:orange'
     ...:     plt.scatter(d[277].real,d[277].imag,color=color)
     ...: plt.scatter(data_sys_off['D'][1][277].real,data_sys_off['D'][1][277].imag,
     ...: color='tab:blue',marker='*')
     ...: plt.scatter(data_sys_off['D'][0][277].real,data_sys_off['D'][0][277].imag,
     ...: color='tab:orange',marker='*')
     ...: plt.title('blue=PS ON, orange=PS OFF\n circles=SYS ON, stars=SYS OFF\n ch=
     ...: 277')
     ...: plt.xlabel('real')
     ...: plt.ylabel('imag')
     ...: plt.grid()
     ...: plt.show(block=False)


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


