#
#! coding:utf-8

def plotCoherence(filename):
    import matplotlib.pyplot as plt
    import sys
    sys.path.insert(0,'../')
    from dttpy.dttdata import DttData
    import numpy as np
    d = DttData('test.xml')
    chnameA = 'K1:PEM-IXV_SEIS_NS_SENSINF_IN1_DQ'
    chnameB = 'K1:PEM-EXV_SEIS_NS_SENSINF_IN1_DQ'
    coherence = d.getCoherence(chnameA, chnameB, ref=False, gwpy = True)
    csd = d.getCSD(chnameA, chnameB, ref=False, gwpy = True)
    from gwpy.plot import Plot
    plot = Plot(coherence, np.angle(csd, deg = True), figsize=(12, 6), dpi=80, separate = True, sharex = True)
    ax = plot.get_axes()
    for a in ax:
        a.get_lines()[0].set_label('/'.join([chnameB,chnameA]))
        a.set_xscale('log')
        a.legend()
    ax[0].set_ylim(0,1)
    ax[0].set_ylabel('Coherence',fontsize=20)
    ax[1].set_ylim(-180,180)
    ax[1].set_yticks(range(-180,181,90))
    ax[1].set_ylabel('Phase [deg]',fontsize=20)
    plot.tight_layout()
    plot.savefig('test_coh.png')
    plt.close()

def plotAllCSD(filename):
    import matplotlib.pyplot as plt
    import sys
    sys.path.insert(0,'../dttpy') 
    from expandedDttData import ExpandedDttData
    import numpy as np
    d = ExpandedDttData('test.xml')
    csds = d.getAllCSD(ref=False, gwpy = True)
    from gwpy.plot import Plot
    j = 0
    for i, csd in enumerate(csds):
        plot = Plot(csd.real, np.angle(csd, deg = True), figsize=(12, 6), dpi=80, separate = True, sharex = True)
        ax = plot.get_axes()
        if 'K1:PEM-IXV_SEIS_NS_SENSINF_IN1_DQ' in format(csd.channel) or 'K1:PEM-EXV_SEIS_NS_SENSINF_IN1_DQ' in format(csd.channel):
            for a in ax:
                a.get_lines()[0].set_label(csd.channel)
                a.set_xscale('log')
                a.legend()
            ax[0].set_ylabel('Cross Spectrum Density',fontsize=20)
            ax[1].set_ylim(-180,180)
            ax[1].set_yticks(range(-180,181,90))
            ax[1].set_ylabel('Phase [deg]',fontsize=20)
            plot.savefig(filename.split('.')[0] + format(j) + '.' + filename.split('.')[1])
            plot.tight_layout()
            plt.close()
            j+= 1

    
if __name__=='__main__':
    plotCoherence('test_coh.png')
    #plotAllCSD('test_csd.png')
    
