#
#! coding:utf-8


import numpy as np
import sys
sys.path.insert(0,'../dttpy') 
from dttdata import DttData
from gwpy.frequencyseries import FrequencySeries

SubType = {'1':'ASD','2':'CSD','3':'COH'}

class ExpandedDttData(DttData):
    def __init__(self, xmlname):
        super(ExpandedDttData, self).__init__(xmlname)
        pass

        
    def getCoherence(self, chnameA, chnameB, ref=False, gwpy = False, **kwargs):
        coherence = list(filter(lambda x:x.Subtype == "COH", self.spect))
        coherence = list(filter(lambda x:x.Channel['ChannelA'] == chnameA, coherence))
        if not ref:
            coherence = list(filter(lambda x: 'Reference' not in x.Name , coherence))
        if gwpy == False:
            return coherence[0].f, coherence[0].spectrum
        elif gwpy == True:
            print(coherence[0].spectrum)
            print(coherence[0].f)
            return FrequencySeries(data = coherence[0].spectrum, frequencies = coherence[0].f, channel = chnameA + ' ' +chnameB)
        else:
            print('!')
            return None

    def getAllASDInfo(self,ref = False):
        allASDInfo = {}
        asd = filter(lambda x:x.Subtype == "ASD", self.spect)
        for a in asd:
            for channel in a.Channel:
                allASDInfo[a.Channel[channel]] = {'channel': channel, 'average': a.Averages, 't0': a.t0, 'dt': a.dt}
        return allASDInfo
            
    def getAllASDName(self,ref = False):
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
        chNameAs = self.getAllAChName(ref)
        chNameBs = self.getAllASDName(ref)
        flag = 0
        CSDs = [[] for i in range(int(len(chNameAs) * (len(chNameAs) - 1) / 2))]
        l = 0
        for i, chNameA in enumerate(chNameAs):
            for j,chNameB in enumerate(chNameBs):
                if i < j:
                    if self.getResultNum(chNameA) == 0 or self.getResultNum(chNameB) == 0:
                        flag = -1
                    if flag == 0:
                        chNames = self.alignCh([chNameA, chNameB])
                        chNameA = chNames[0]
                        chNameB = chNames[1]
                    if gwpy:
                        CSDs[l] = self.getCSD(chNameA, chNameB, ref, gwpy)
                        l+= 1
                    else:
                        CSDs[l] = [self.getCSD(chNameA, chNameB, ref, gwpy), chNameA, chNameB]
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

                    
