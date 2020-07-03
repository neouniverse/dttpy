#
#! coding:utf-8

import sys
sys.path.insert(0,'../')    
from dttpy import DttData
import matplotlib.pyplot as plt

def testChannelInfo():
    print('--- test Channel Info ---')    
    xmlname = 'test.xml'
    d = DttData(xmlname)
    d.getAllSpectrumName()
    print('--- test Channel Info (End)---')    

def testDttSpectrumInfo():
    print('--- test DttSpectrumInfo ---')    
    xmlname = 'test.xml'
    d = DttData(xmlname)    
    chnameA = 'K1:PEM-EXV_SEIS_NS_SENSINF_IN1_DQ'
    d.getASDInfo(chnameA,ref=False)
    print('--- test DttSpectrumInfo (Info)---')
    
def testASD():
    xmlname = 'test.xml'    
    d = DttData(xmlname)
    chnameA = 'K1:PEM-EXV_SEIS_NS_SENSINF_IN1_DQ'
    chnameB = 'K1:PEM-IXV_SEIS_NS_SENSINF_IN1_DQ'
    chnameC = 'K1:PEM-IXV_TEST_SEIS_WE_SENSINF_OUT_DQ'
    
    plt.figure(num=None, figsize=(12, 6), dpi=80)
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
    chnameA = 'K1:PEM-IXV_SEIS_NS_SENSINF_IN1_DQ'
    chnameB = 'K1:PEM-IXV_SEIS_TEST_NS_SENSINF_IN1_DQ'
    f,csd,deg = d.getCSD(chnameA,chnameB,ref=False)
    plt.figure(num=None, figsize=(12, 6), dpi=80)
    print(csd)
    plt.loglog(f,csd,label='/'.join([chnameB,chnameA]))
    #plt.ylim(1e-23,1e-12)
    plt.legend()
    plt.savefig('test_csd.png')
    plt.close()    
    
def testCoherence():
    d = DttData('test.xml')
    chnameA = 'K1:PEM-IXV_SEIS_NS_SENSINF_IN1_DQ'
    chnameB = 'K1:PEM-EXV_SEIS_NS_SENSINF_IN1_DQ'
    f,mag = d.getASD(chnameA,ref=False)
    f,mag,deg = d.getCoherence(chnameA,chnameB,ref=False)
    
    fig, (ax0,ax1) = plt.subplots(2,1,figsize=(12, 6), dpi=80)
    ax0.semilogx(f,mag,label='/'.join([chnameB,chnameA]))
    ax0.legend()
    ax0.set_ylim(0,1)
    ax0.set_ylabel('Coherence',fontsize=20)
    ax1.semilogx(f,deg,label='/'.join([chnameB,chnameA]))
    ax1.legend()
    ax1.set_ylim(-180,180)
    ax1.set_yticks(range(-180,181,90))
    ax1.set_ylabel('Phase [deg]',fontsize=20)    
    ax1.set_xlabel('Frequency [Hz]',fontsize=20)    
    plt.savefig('test_coh.png')
    plt.close()
  
if __name__=='__main__':
    testChannelInfo() # OK
    #testCoherence() # OK
    #testDttSpectrumInfo() # OK    
    # bug
    #test_plottf()      
    testASD()
    testCSD()
    
