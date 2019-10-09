
#
#! coding:utf-8


import numpy as np
from gwpy.frequencyseries import FrequencySeries

from dttdata import DttData

SubType = {'1':'ASD','2':'CSD','3':'COH'}

class ExpandedDttData(DttData):
    def __init__(self, xmlname):
        super(ExpandedDttData, self).__init__(xmlname)
        pass
 
    def getAllSpectrumName(self):
        allSpectrumName = []
        spect = filter(lambda x:x.Subtype == "ASD" or x.Subtype == "CSD", self.spect)
        for s in spect:
            for channel in s.Channel:
                allSpectrumName.append([s.Subtype, channel, s.Channel[channel]])
        return allSpectrumName
        
    def printAllASDInfo(self,ref=False):
        asd = filter(lambda x:x.Subtype == "ASD", self.spect)
        for a in asd:
            for channel in a.Channel:
                print('{ ' + channel, a.Channel[channel])
                print(' average: ' + format(a.Averages))
                print(' t0: ' + a.t0)
                print(' dt: ' + a.dt + ' }')
            
    def getAllASDName(self,ref=False):
        names = []
        for s in self.spect:
            if s.Subtype == 'ASD':                
                if ref == False:
                    if 'Result' in s.Name:
                       names.append(s.Channel['ChannelA'])
                elif ref == True:
                    if 'Reference' in s.Name:
                       names.append(s.Channel['ChannelA'])
                else:
                    print('ref is Unauthorized value!')
        return names

    def getAllAChName(self,ref = False):
        names = []
        for s in self.spect:
            if s.Subtype == 'CSD':                
                if ref == False:
                    if 'Result' in s.Name:
                       names.append(s.Channel['ChannelA'])
                elif ref == True:
                    if 'Reference' in s.Name:
                       names.append(s.Channel['ChannelA'])
                else:
                    print('ref is Unauthorized value!')
                    return None
        return names

    def getAllASD(self, ref = False, gwpy = False):        
        names= self.getAllASDName(ref)
        ASDs = []
        for name in names:
            if gwpy:
                ASD = self.getASD(name, ref, gwpy)
                ASDs.append(ASD)
            else:
                f,asd = self.getASD(name, ref, gwpy)
                ASDs.append([f, asd, name])
        ASDs = np.array(ASDs)
        return ASDs
            
    def alignCh(self, chnames, ref = False):
        alignNums = []
        alignNames = []

        for chname in chnames:
            alignNums.append(self.getResultNum(chname,ref))
        alignNums.sort()
        for alignnum in alignNums:
            for chname in chnames:
                if alignnum == self.getResultNum(chname,ref):
                    alignNames.append(chname)
                    break
        return alignNames
    
    def getAllCSD(self, ref = False, gwpy = False):
        anames = self.getAllAChName(ref)
        bnames = self.getAllASDName(ref)
        flag = 0
        CSDs= []
        for i in range(len(anames)):
            for j in range(len(bnames)):
                if i<j:
                    if self.getResultNum(anames[i]) == 0 or self.getResultNum(bnames[j]) == 0:
                        flag = -1
                    if flag == 0:
                        chname = self.alignCh([anames[i],bnames[j]])
                        achname = chname[0]
                        bchname = chname[1]
                    else:
                        achname = anames[i]
                        bchname = bnames[j]
                    if gwpy:
                        CSD = self.getCSD(achname, bchname, ref, gwpy)
                        CSDs.append(CSD)
                    else:
                        f, mag, deg = self.getCSD(achname, bchname, ref, gwpy)
                        CSDs.append([f, mag, deg, achname, bchname])
        CSDs =  np.array(CSDs)
        return CSDs
        
    def getAllCoherence(self, ref = False, gwpy = False):
        COHs = []
        CSDs = self.getAllCSD(ref, gwpy)
        for CSD_AB in CSDs:
            if gwpy:
                ASD_A = self.getASD(CSD_AB.channel.split()[0], ref, gwpy)
                ASD_B = self.getASD(CSD_AB.channel.split()[1], ref, gwpy)
                COH = (CSD_AB / (ASD_A * ASD_B)) ** 2
            else:
                f, asd_A = self.getASD(CSD_AB[3], ref, gwpy)
                f, asd_B = self.getASD(CSD_AB[4], ref, gwpy)
                coh = (CSD_AB[1] / (asd_A * asd_B)) ** 2
                COH = [CSD_AB[0], coh, CSD_AB[3], CSD_AB[4]]
                
            COHs.append(COH)
        COHs = np.array(COHs)
        return COHs

                    
