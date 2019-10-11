Dttpy
====

Dttpy can convert data embedded in the xml diaggui file to numpy.array and FrequencySeries.

This version is for GWpy user.

## Install
Clone or download own workspace.

## How to use
1. Prepare the diaggui file which is 

## How to use
Download dttdata.py on your work space. In this case, file name is 'test.xml'.

Call DttData module and you can use some methods 

```
from dttdata import DttData
d = DttData('test.xml')
chnameA = 'K1:PEM-IY0_SEIS_NS_SENSINF_OUT_DQ'
chnameB = 'K1:PEM-EX1_SEIS_NS_SENSINF_OUT_DQ'
f,asd = d.getASD(chnameA, ref = False, gwpy = False)
f,mag,deg = d.getCoherence(chnameA, chnameB, ref=False)
...

```

Also you can plot.

```
...
import matplotlib.pyplot as plt
fig, (ax0,ax1) = plt.subplots(2,1,figsize=(12, 6), dpi=80)
ax0.semilogx(f, mag, label = '/'.join([chnameB,chnameA]))
ax0.legend()
ax0.set_ylim(0,1)
ax0.set_ylabel('Coherence',fontsize=20)
ax1.semilogx(f,deg,label='/'.join([chnameB,chnameA]))
ax1.legend()
ax1.set_ylim(-180,180)
ax1.set_yticks(range(-180,181,90))
ax1.set_ylabel('Phase [deg]',fontsize=20)
ax1.set_xlabel('Frequency [Hz]',fontsioze=20)
plt.savefig('test_coh.png')
plt.close()
```

Or, if you want to use gwpy
```
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
```

![result_image](./tests/test_coh.png)

## Contribution
Koki.Okutomi

## Licence

[MIT](https://github.com/MiyoKouseki/dttpy/tree/master/LICENCE)

## Author

[TaikiTanaka](https://github.com/TTanakaTT)