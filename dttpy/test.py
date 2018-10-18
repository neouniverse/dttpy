#
#! coding:utf-8

from plot import plottf

def testReference():
    xmlname = 'test.xml'    
    d = DttData(xmlname)
    d.getAllSpectrumName()

def testDttSpectrumInfo():
    xmlname = 'test.xml'
    d = DttData(xmlname)    
    chnameA = 'K1:PEM-IY0_SEIS_NS_SENSINF_OUT_DQ'
    d.getASDInfo(chnameA,ref=False)
    
def testASD():
    xmlname = 'test.xml'
    d = DttData(xmlname)    
    chnameA = 'K1:PEM-IY0_SEIS_NS_SENSINF_OUT_DQ'
    chnameB = 'K1:PEM-EX1_SEIS_NS_SENSINF_OUT_DQ'
    chnameC = 'K1:PEM-IY0_SEIS_WE_SENSINF_OUT_DQ'
    plt.figure(num=None, figsize=(12, 6), dpi=80)
    f,asd = d.getASD(chnameA,ref=True)
    plt.loglog(f,asd,label=chnameA+'Ref')
    f,asd = d.getASD(chnameA,ref=False)
    plt.loglog(f,asd,label=chnameA)
    f,asd = d.getASD(chnameB,ref=False)
    plt.loglog(f,asd,label=chnameB)
    #plt.ylim(1e-23,1e-12)
    plt.legend()
    plt.savefig('test_asd.png')
    plt.close()    
   
    
def testCSD():
    xmlname = 'test.xml'
    d = DttData(xmlname)
    chnameA = 'K1:PEM-IY0_SEIS_NS_SENSINF_OUT_DQ'
    chnameB = 'K1:PEM-EX1_SEIS_NS_SENSINF_OUT_DQ'
    chnameC = 'K1:PEM-IY0_SEIS_WE_SENSINF_OUT_DQ'
    f,csd,deg = d.getCSD(chnameA,chnameB,ref=False)
    plt.figure(num=None, figsize=(12, 6), dpi=80)
    plt.loglog(f,csd,label='/'.join([chnameB,chnameA]))
    #f,csd,deg = d.getCSD(chnameA,chnameC)
    plt.ylim(1e-23,1e-12)
    #plt.loglog(f,csd,label='/'.join([chnameC,chnameA]))
    plt.legend()
    plt.savefig('test_csd.png')
    plt.close()    

def testCoherence():
    xmlname = 'test.xml'
    d = DttData(xmlname)    
    chnameA = 'K1:PEM-IY0_SEIS_NS_SENSINF_OUT_DQ'
    chnameB = 'K1:PEM-EX1_SEIS_NS_SENSINF_OUT_DQ'
    chnameC = 'K1:PEM-IY0_SEIS_WE_SENSINF_OUT_DQ'
    f,mag,deg = d.getCoherence(chnameA,chnameB,ref=False)
    plt.figure(num=None, figsize=(12, 6), dpi=80)
    plt.subplot(211)
    plt.semilogx(f,mag,label='/'.join([chnameB,chnameA]))
    plt.legend()
    plt.subplot(212)
    plt.semilogx(f,deg,label='/'.join([chnameB,chnameA]))
    plt.legend()
    plt.savefig('test_coh.png')
    plt.close()       

  
def test_plottf():
    date = '180614'       
    sus = 'PR3'
    stage = 'IM'
    dof = 'L'
    plottf(date,sus,stage,dof)


if __name__=='__main__':
    test_plottf()
   
