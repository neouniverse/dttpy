#
#! coding:utf-8

from dttdata import DttData
import numpy as np


def plottf(date,sus,stage,dof,prefix='./template'):
    ''' Plot transfer function from template xml file of the diaggui(dtt).

    This function export png file which plots single TF about dof you choose, 
    does not plot other dof. So, if you choose dof as "L", this function 
    plots the TF from L to L, does not plot coupling components such as a L-T,L-Y, 
    and so on. (However, if you want plot about copuling composnent, you can plot 
    with some modification.)

    Rule of the  dtt xml file name is "<sus>_<stage>_<dof>_<date>.xml".
    <sus> is a name of the suspension; PR2,PR3,..
    <stage> is a name of the stage; IM,TM,..
    <dof> is a excitation point; L,T,..    
    
    Parameter
    ---------
    date : str
        JST date, which is given like "YYMMDD".
    sus : str
        Name of the suspension.
    stage : str
        Name of the stage.
    dof : str
        Name of the excitation point.
    prefix : str
        Place where the dtt xml files are located. Default is "./template"
    '''
    #
    xmlname = './template/{0}_{1}{2}_exc_{3}.xml'.format(sus,stage,dof,date)
    chA = 'K1:VIS-{0}_{1}_DAMP_{2}_IN1'.format(sus,stage,dof)
    chB = 'K1:VIS-{0}_{1}_TEST_{2}_EXC'.format(sus,stage,dof)
    d = DttData(xmlname)
    s = d.spect[0]
    f1,mag1,deg1 = d.getCoherence(chA,chB)
    f2,mag2,deg2 = d.getTF(chA,chB)
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
    plt.suptitle('Transfer Function of the {0}, \n'\
                 'from "{1}" to "{2}"'.format(sus,chB,chA),fontsize=10)
    ax_pos = ax2.get_position()
    fig.text(ax_pos.x1*1.01, ax_pos.y0,
             'GPS:{0} \n'\
             'BW={1:3.2f} Hz, ave={2}'\
             ''\
             ''.format(int(float(s.t0)),float(s.BW),s.Averages,s.Window),
                 rotation=90,verticalalignment='bottom')                     
    plt.savefig(xmlname.replace('xml','png'))    
    plt.close()
    print('plot as {}'.format(xmlname.replace('xml','png')))
    
    
if __name__ == '__main__':
    date = '180614'       
    sus = 'PR3'
    stage = 'IM'
    dof = 'L'
    plottf(date,sus,stage,dof)
    
