#
#! coding:utf-8

import numpy as np
import sys
sys.path.insert(0,'../')    
from dttpy import DttData
import matplotlib.pyplot as plt

  
if __name__=='__main__':
    xmlname1 = './1636_1_ab_MICH_BS.xml'
    xmlname2 = './1704_3_a_MICH_ITMY.xml'        
    d1 = DttData(xmlname1)
    d1.getAllSpectrumName()

    label=['G_mich','A_bs*C_mich','A_bs*C_mich/(1+G_mich)']
    
    chB = ['K1:VIS-BS_ISCINF_L_IN1']
    chA = ['K1:VIS-BS_ISCINF_L_IN2']

    fig,ax = plt.subplots(3,3,figsize=(12,7),sharex=True)
    
    for i in range(1):
        for j in range(1):            
            bs2mich = d1.getTF(chA[i],chB[j],ref=False,db=True)
            f,mag,deg = bs2mich
            ax[j][i].semilogx(f,mag,'ro',label='Current')
            ax[j+1][i].semilogx(f,deg,'ro',label='Current')
            #
            bs2mich = d1.getTF(chA[i],chB[j],ref=True,db=True)
            f,mag,deg = bs2mich
            ax[j][i].set_title('{2}={0}/{1}'.format(chB[j],chA[i],label[i]),fontsize=7)
            ax[j+1][i].set_title('{2}={0}/{1}'.format(chB[j],chA[i],label[i]),fontsize=7)
            ax[j][i].semilogx(f,mag,'kx-',label='Feb 21, 2020')
            ax[j+1][i].semilogx(f,deg,'kx-',label='Feb 21, 2020')
            ax[j][i].legend(loc='upper right')
            ax[j+1][i].legend(loc='upper right')
            ax[j+1][i].set_ylim(-180,180)
            ax[j+1][i].set_yticks(range(-180,181,90))        
            ax[j+1][i].grid(b=True,which='both',linestyle='--')
            ax[j][i].grid(b=True,which='both',linestyle='--')            

    chB = ['K1:LSC-MICH1_IN1']
    chA = ['K1:VIS-BS_ISCINF_L_OUT','K1:VIS-BS_ISCINF_L_EXC']
    for j in range(1):                        
        for i in range(2):
            bs2mich = d1.getTF(chA[i],chB[j],ref=False,db=True)
            f,mag,deg = bs2mich
            ax[j][i+1].semilogx(f,mag,'ro',label='Current')
            ax[j+1][i+1].semilogx(f,deg,'ro',label='Current')
            bs2mich = d1.getTF(chA[i],chB[j],ref=True,db=True)
            f,mag,deg = bs2mich
            ax[j][i+1].set_title('{2}={0}/{1}'.format(chB[j],chA[i],label[i+1]),fontsize=7)
            ax[j+1][i+1].set_title('{2}={0}/{1}'.format(chB[j],chA[i],label[i+1]),fontsize=7)            
            ax[j][i+1].semilogx(f,mag,'kx-',label='Feb 21, 2020')            
            ax[j+1][i+1].semilogx(f,deg,'kx-',label='Feb 21, 2020')
            ax[j+1][i+1].legend(loc='upper right')            
            ax[j][i+1].legend(loc='upper right')                
            ax[j+1][i+1].set_ylim(-180,180)
            ax[j+1][i+1].set_yticks(range(-180,181,90))        
            ax[j+1][i+1].grid(b=True,which='both',linestyle='--')
            ax[j][i+1].grid(b=True,which='both',linestyle='--')


    bs2mich = d1.getCoherence(chA[i],chB[j],ref=False)
    f,mag = bs2mich
    ax[2][2].semilogx(f,mag,'ro',label='Current')
    bs2mich = d1.getCoherence(chA[i],chB[j],ref=True)
    f,mag = bs2mich
    ax[2][2].semilogx(f,mag,'kx-',label='Feb 21, 2020')
    ax[2][2].legend(loc='lower left')                
    ax[2][2].set_title('{2}={0}/{1}'.format(chB[0],chA[1],label[1+1]),fontsize=7)
    ax[2][2].set_ylim(0,1.1)
    ax[2][2].set_yticks(np.arange(0,1.01,0.25))        
    ax[2][2].grid(b=True,which='both',linestyle='--')
    ax[2][2].grid(b=True,which='both',linestyle='--')
    [ax[2][i].set_xlabel('Frequency [Hz]') for i in range(3)]
    ylabel=['Magnitude (dB)','Phase (deg.)','Coherence']
    [ax[i][0].set_ylabel(ylabel[i]) for i in range(3)]
    
    plt.tight_layout()
    plt.savefig('test_cal.png')
    plt.close()
