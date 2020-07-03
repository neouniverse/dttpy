#
#! coding:utf-8

import xml.etree.ElementTree as ET
from xml.etree import ElementTree
import base64
import binascii
import numpy as np
import matplotlib.pyplot as plt

SubType = {'1':'ASD','2':'CSD','3':'TF','4':'???','5':'COH'}
average_type = {'0':'Fixed','1':'Exponential','2':'Accumulative'} # not comfirmed
window_type = {'0':'Uniform','1':'Hanning','2':'Flat-top',
               '3':'Welch','4':'Bartlet','5':'BMH'} # not comfirmed

class DttXMLSpectrum():
    def __init__(self,child):
        self.Name = child.attrib["Name"]
        self._getAttribute(child)
        self._getStream(child)
        
    def _getAttribute(self,child):
        self.dt       = child.find("./Param[@Name='dt']").text
        self.t0       = child.find("./Time[@Type='GPS']").text        
        self.BW       = child.find("./Param[@Name='BW']").text
        self.f0       = child.find("./Param[@Name='f0']").text
        self.df       = child.find("./Param[@Name='df']").text
        self.N        = int(child.find("./Param[@Name='N']").text)
        self.Window   = child.find("./Param[@Name='Window']").text
        self.AveType  = child.find("./Param[@Name='AverageType']").text
        self.Averages = child.find("./Param[@Name='Averages']").text        
        self.Flag     = child.find("./Param[@Name='Flag']").text
        self.Subtype  = SubType[child.find("./Param[@Name='Subtype']").text]
        self.M        = int(child.find("./Param[@Name='M']").text)
        self.dim      = child.find('./Array/Dim').text
        channel = child.findall("./Param[@Unit='channel']")
        self.Channel  = list(map(lambda x:{x.attrib['Name']:x.text},channel))
        Channel = self.Channel[0]
        for c in self.Channel:
            Channel.update(c)           
        self.Channel = Channel

    def showInfo(self):
        fmt = 'dt [s]\t:{dt:2.10f}\n'+\
              't0(GPS)\t:{t0:10.1f}\n'+\
              'BW [Hz]\t:{bw:2.10f} \n'+\
              'f0 [Hz]\t:{f0:2.10f} \n'+\
              'df [Hz]\t:{df:2.10f} \n'+\
              'average\t:{average:12d} \n'+\
              'Points\t:{n:12d} \n'+\
              'window\t:{window:12s} \n'+\
              'type\t:{aveType:12s}\n'+\
              'flag\t:{flag:12s}'              
        text = fmt.format(dt=float(self.dt),
                          t0=float(self.t0),
                          bw=float(self.BW),
                          f0=float(self.f0),
                          df=float(self.df),
                          n=int(self.N),
                          window=self.Window,
                          aveType=self.AveType,
                          average=int(self.Averages),
                          flag=self.Flag
        )
        print(text)
        
    def _getStream(self,child):
        stream_str = child.find('./Array/Stream').text
        stream_bin = binascii.a2b_base64(stream_str)                   
        if self.Subtype == 'ASD': # float : asd           
            self.spectrum = np.frombuffer(stream_bin, dtype=np.float32)
            self.f        = np.arange(len(self.spectrum))*float(self.df)
        elif self.Subtype == 'CSD': # floatcomplex : cross spectrum
            self.spectrum = np.frombuffer(stream_bin, dtype=np.float32)
            real = self.spectrum[0::2]
            real = real.reshape(self.M,self.N)
            imag = self.spectrum[1::2]
            imag = imag.reshape(self.M,self.N)
            imag = 1j*imag
            c = real+imag
            #print c[0,:5]
            # Cxy
            # x:ChannelA
            # y:ChannelB[0-]
            self.csd = np.absolute(c)
            self.deg = np.rad2deg(np.angle(c))            
            self.f        = np.arange(len(self.csd[0]))*float(self.df)
        elif self.Subtype == '???': # float : coherence?
            self.spectrum = np.frombuffer(stream_bin, dtype=np.float32)
            self.f        = np.arange(len(self.spectrum))*float(self.df)
            #print len(self.spectrum),len(self.f)


class DttXMLTransferFunction():
    def __init__(self,child):
        self.Name = child.attrib["Name"]
        self._getAttribute(child)
        self._getStream(child)
        
    def _getAttribute(self,child):
        #self.dt       = child.find("./Param[@Name='dt']").text
        #self.t0       = child.find("./Time[@Type='GPS']").text        
        self.BW       = child.find("./Param[@Name='BW']").text
        self.f0       = child.find("./Param[@Name='f0']").text
        self.df       = child.find("./Param[@Name='df']").text
        self.N        = int(child.find("./Param[@Name='N']").text)
        self.Window   = child.find("./Param[@Name='Window']").text
        self.AveType  = child.find("./Param[@Name='AverageType']").text
        self.Averages = child.find("./Param[@Name='Averages']").text        
        self.Flag     = child.find("./Param[@Name='Flag']").text
        self.Subtype  = SubType[child.find("./Param[@Name='Subtype']").text]
        self.M        = int(child.find("./Param[@Name='M']").text)
        self.dim      = child.find('./Array/Dim').text
        channel = child.findall("./Param[@Unit='channel']")
        self.Channel  = list(map(lambda x:{x.attrib['Name']:x.text},channel))
        Channel = self.Channel[0]
        for c in self.Channel:
            Channel.update(c)           
        self.Channel = Channel

    def showInfo(self):
        fmt = 'dt [s]\t:{dt:2.10f}\n'+\
              't0(GPS)\t:{t0:10.1f}\n'+\
              'BW [Hz]\t:{bw:2.10f} \n'+\
              'f0 [Hz]\t:{f0:2.10f} \n'+\
              'df [Hz]\t:{df:2.10f} \n'+\
              'average\t:{average:12d} \n'+\
              'Points\t:{n:12d} \n'+\
              'window\t:{window:12s} \n'+\
              'type\t:{aveType:12s}\n'+\
              'flag\t:{flag:12s}'              
        text = fmt.format(dt=float(self.dt),
                          t0=float(self.t0),
                          bw=float(self.BW),
                          f0=float(self.f0),
                          df=float(self.df),
                          n=int(self.N),
                          window=self.Window,
                          aveType=self.AveType,
                          average=int(self.Averages),
                          flag=self.Flag
        )
        print(text)
        
    def _getStream(self,child):
        stream_str = child.find('./Array/Stream').text
        stream_bin = binascii.a2b_base64(stream_str)
        #print(stream_bin)
        #print(self.Subtype)
        #
        if self.Subtype == 'ASD': # float : asd           
            self.spectrum = np.frombuffer(stream_bin, dtype=np.float32)
            #self.f        = np.arange(len(self.spectrum))*float(self.df)
        elif self.Subtype == 'CSD': # floatcomplex : cross spectrum
            self.spectrum = np.frombuffer(stream_bin, dtype=np.float32)
            real = self.spectrum[0::2]
            real = real.reshape(self.M,self.N)
            imag = self.spectrum[1::2]
            imag = imag.reshape(self.M,self.N)
            imag = 1j*imag
            c = real+imag
            #print c[0,:5]
            # Cxy
            # x:ChannelA
            # y:ChannelB[0-]
            self.csd = np.absolute(c)
            self.deg = np.rad2deg(np.angle(c))            
            #self.f   = np.arange(len(self.csd[0]))*float(self.df)
        elif self.Subtype == 'TF':
            self.spectrum = np.frombuffer(stream_bin, dtype=np.float32)
            real = self.spectrum[0::2]
            real = real.reshape(self.M+1,self.N)
            imag = self.spectrum[1::2]
            imag = imag.reshape(self.M+1,self.N)
            imag = 1j*imag
            c = real+imag
            self.mag = np.absolute(c)
            self.deg = np.rad2deg(np.angle(c))
            #print('mag',self.mag)
            #print('deg',self.deg)            
            #self.f  = np.arange(len(self.mag[0]))*float(self.df)
            #print('###',self.f,self.df)
            #exit()
        elif self.Subtype == 'COH':
            self.spectrum = np.frombuffer(stream_bin, dtype=np.float32)
            self.spectrum = self.spectrum.reshape(self.M+1,self.N)            
            self.mag = self.spectrum
        else:
            raise ValueError('!')

class DttXMLTestParameter():
    def __init__(self,child):
        self.Name = child.attrib["Name"]
        self._getAttribute(child)
        
    def _getAttribute(self,child):
        #self.dt       = child.find("./Param[@Name='dt']").text
        #self.t0       = child.find("./Time[@Type='GPS']").text        
        self.sp       = child.find("./Param[@Name='SweepPoints']").text
        #print(self.sp)
        self.sp = list(map(float,self.sp.split()))[0::2]
                        

class DttData():
    def __init__(self,xmlname):
        '''
        '''
        tree = ElementTree.parse(xmlname)
        root = tree.getroot()
        self.spect = [DttXMLSpectrum(child) for child in \
                      root.findall("./LIGO_LW[@Type='Spectrum']")]
        if not self.spect:
            self.tfmode = True            
            self.spect = [DttXMLTransferFunction(child) for child in \
                          root.findall("./LIGO_LW[@Type='TransferFunction']")]
            huge = root.findall("./LIGO_LW[@Type='TestParameter']")
            hoge = DttXMLTestParameter(huge[0])
            self.f = hoge.sp            

    def getAllSpectrumName(self):
        ''' 
        
        '''
        for s in self.spect:
            print(s.Name,s.Subtype,s.Channel['ChannelA'])
            

    def getASDInfo(self,chname,ref=False):
        '''

        '''
        asd = filter(lambda x:x.Subtype=="ASD", self.spect)
        asd = filter(lambda x:x.Channel['ChannelA']==chname, asd)
        asd = list(asd)
        if len(asd)==1:
            asd = asd[0]
        else:
            raise ValueError('Error!')        
        asd.showInfo()
        
    def getASD(self,chname,ref=False):
        '''

        '''
        asdlist = filter(lambda x:x.Subtype=="ASD", self.spect)
        asdlist = filter(lambda x:x.Channel['ChannelA']==chname, asdlist)
        asdlist = list(asdlist)
        if len(asdlist)==0:
            raise ValueError('No ASD with : {0}'.format(chname))

        for asd in asdlist:
            print(asd.Name,asd.Subtype)
            if ref==False:
                if 'Result' in asd.Name:
                    return asd.f,asd.spectrum
                else:
                    raise ValueError('No name')                    
            elif ref==True:
                if 'Reference' in asd.Name:
                    return asd.f,asd.spectrum
                else:
                    raise ValueError('No reference')
            else:
                print('!')
                return None
        print('!')

    def getResultNum(self,chname,ref=False):
        '''

        '''
        asd = list(filter(lambda x:x.Subtype=="ASD", self.spect))
        asd = list(filter(lambda x:x.Channel['ChannelA']==chname, asd))
        num = asd[0].Name
        return int(num.split('[')[1][0])
    
    def getCSD(self,chnameA,chnameB,ref=False,**kwargs):
        '''

        '''
        import re
        csd = list(filter(lambda x:x.Subtype=="CSD", self.spect))
        csd = list(filter(lambda x:x.Channel['ChannelA']==chnameA, csd))
        if not ref:
            csd = list(filter(lambda x: 'Reference' not in x.Name , csd))
            
        numA = self.getResultNum(chnameA,**kwargs)
            
        for c in csd[0].Channel.keys():
            if csd[0].Channel[c] == chnameB:
                num = int(c[:-1].split('[')[1])
                if num >= numA:
                    num = num -1
                elif num < numA:
                    num = num
                #print numA,num,csd[0].Channel[c]
        return csd[0].f,csd[0].csd[num],csd[0].deg[num]
    

    def getCoherence(self,chnameA,chnameB,ref=False):
        '''
        '''
        if not self.tfmode:        
            freq = None
            freq,CSD_AB,deg = self.getCSD(chnameA,chnameB)
            freq,ASD_A = self.getASD(chnameA)
            freq,ASD_B = self.getASD(chnameB)
            mag = (CSD_AB/(ASD_A*ASD_B))**2
        else:
            import re        
            csd = list(filter(lambda x:x.Subtype=="COH", self.spect))
            csd = list(filter(lambda x:x.Channel['ChannelA']==chnameA, csd))
            if not ref:
                csd = list(filter(lambda x: 'Reference' not in x.Name , csd))
            else:
                csd = list(filter(lambda x: 'Reference' in x.Name , csd))

            if len(csd)==1:
                csd = csd[0]
            else:
                raise ValueError('!')
            chnames = list(csd.Channel.values())
            label = list(csd.Channel.keys())
            print(chnameA,chnames)
            num = chnames.index(chnameB)
            if ref:
                freq = csd.mag[0]
            else:
                freq = self.f                
            mag = csd.mag[num]
            
        return freq,mag

    def getTF(self,chnameA,chnameB,ref=False,db=True):
        '''
        '''
        if not self.tfmode:
            f = None
            f,CSD_AB,deg = self.getCSD(chnameA,chnameB)
            f,ASD_A = self.getASD(chnameA)
            f,ASD_B = self.getASD(chnameB)
            mag = CSD_AB/(ASD_B*ASD_B)
            return f,mag,deg    
        else:
            import re        
            csd = list(filter(lambda x:x.Subtype=="TF", self.spect))
            csd = list(filter(lambda x:x.Channel['ChannelA']==chnameA, csd))
            if not ref:
                csd = list(filter(lambda x: 'Reference' not in x.Name , csd))
            else:
                csd = list(filter(lambda x: 'Reference' in x.Name , csd))

            if len(csd)==1:
                csd = csd[0]
            else:
                raise ValueError('!')

            chnames = list(csd.Channel.values())
            label = list(csd.Channel.keys())
            print(chnameA,chnames)
            num = chnames.index(chnameB)
            if ref:
                freq = csd.mag[0]
            else:
                freq = self.f
            mag = csd.mag[num]
            deg = csd.deg[num]

            if db:
                mag = 20*np.log10(mag)
            
            return freq,mag,deg
