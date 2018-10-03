#
#! coding:utf-8

from dttdata import DttData
import numpy as np


def plottf(xmlname,chA,chB):
    d = DttData(xmlname)
    f1,mag1,deg1 = d.getCoherence('K1:VIS-PR3_IM_DAMP_L_IN1','K1:VIS-PR3_IM_TEST_L_EXC')
    f2,mag2,deg2 = d.getTF('K1:VIS-PR3_IM_DAMP_L_IN1','K1:VIS-PR3_IM_TEST_L_EXC')
    #
    import matplotlib.pyplot as plt
    fig,(ax0,ax1,ax2) = plt.subplots(3,1)
    ax0.loglog(f2,mag2,label='',color='black')
    ax0.set_ylabel('Magnitude',fontsize=10)
    ax0.set_ylim(1e-7,1e0)
    ax0.set_yticks(np.logspace(-8,0,5))
    ax0.grid(b=True, which='major', color='gray', linestyle='-')
    ax0.grid(b=True, which='minor', color='gray', linestyle=':')
    ax2.semilogx(f1,mag1,label='',color='black')
    ax2.set_ylim(0,1)
    ax2.set_yticks([0,0.25,0.5,0.75,1])    
    ax2.set_ylabel('Coherence',fontsize=10)
    ax2.grid(b=True, which='major', color='gray', linestyle='-')
    ax2.grid(b=True, which='minor', color='gray', linestyle=':')    
    ax1.semilogx(f1,deg1,color='black')
    ax1.set_yticks(range(-180,181,90))
    ax1.set_ylim(-180,180)
    ax1.set_ylabel('Degree [deg]',fontsize=10)
    ax1.grid(b=True, which='major', color='gray', linestyle='-')
    ax1.grid(b=True, which='minor', color='gray', linestyle=':')
    ax2.set_xlabel('Frequency [Hz]',fontsize=10)
    plt.subplots_adjust(hspace=0.15,top=0.90)
    ax0.yaxis.set_label_coords(-0.1,0.5)
    ax2.yaxis.set_label_coords(-0.1,0.5)
    ax1.yaxis.set_label_coords(-0.1,0.5)    
    plt.setp(ax0.get_xticklabels(), visible=False)
    plt.setp(ax1.get_xticklabels(), visible=False)    
    plt.suptitle('Transfer Function \n {0} / {1}'.format(chA,chB),fontsize=10)
    plt.savefig(xmlname.replace('xml','png'))
    plt.close()
    
    
if __name__ == '__main__':
    sus = 'PR3'
    exc = 'IML'
    date = '180614'
    xmlname = './template/{0}_{1}_exc_{2}.xml'.format(sus,exc,date)
    chA = 'K1:VIS-PR3_IM_DAMP_L_IN1'
    chB = 'K1:VIS-PR3_IM_TEST_L_EXC'
    plottf(xmlname,chA,chB)
    
