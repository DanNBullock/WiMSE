#!/usr/bin/env python
# coding: utf-8

# In[1]:


cd /Users/plab/Documents/gitDir/WMA_pyTools


# In[2]:


import WMA_pyFuncs
import nibabel as nib
import numpy as np
from scipy.spatial.distance import cdist
import itertools
    
    
from dipy.segment.clustering import QuickBundles
from dipy.segment.metric import ResampleFeature
from dipy.segment.metric import AveragePointwiseEuclideanMetric


# In[3]:


#streamlines=nib.streamlines.load('/Users/plab/Documents/ipynb/exampleData/smallTractogram.tck')
streamlines=nib.streamlines.load('/Users/plab/Downloads/5c5d35e2f5d2a10052842847/track.tck')


# In[4]:


neckClusters=WMA_pyFuncs.neckmentation(streamlines.streamlines)


# In[ ]:


#get tractogram from the Tck holder
sourceTractogram=streamlines.tractogram

#quick and dirty tractogram subsetter by Brad Caron
#https://github.com/bacaron
def extractSubTractogram(sourceTractogram,indexes):
    #import relevant package
    import nibabel as nib
    #extrect the desired streamlines into a new streamline object
    streamlines = sourceTractogram.streamlines[indexes]
    #establish tractogram object
    out_tractogram = nib.streamlines.tractogram.Tractogram(streamlines)
    #adjust the relevant header fields
    #don't bother for now, header is only relevant to Tck file
    #for headerFields in ['total_count','count','nb_streamlines']:
        #nb_streamlines is an int, whereas the others are strings, for some reason
    #    if headerFields == 'nb_streamlines':
    #        out_tractogram.header[headerFields] = len(streamlines)
    #    else:
    #        out_tractogram.header[headerFields] = '%s' %len(streamlines)
    return out_tractogram

#interactive plotting via niwidgets?  
#widget within a widget doesn't seem to work
def plotParcellationConnectionWidget(subTractogram):
    #import widget
    from niwidgets import StreamlineWidget
    #set widget object
    
    sw = StreamlineWidget(streamlines=subTractogram)
    #set plotting characteristics
    style = {'axes': {'color': 'red',
                  'label': {'color': 'white'},
                  'ticklabel': {'color': 'white'},
                  'visible': False},
         'background-color': 'black',
         'box': {'visible': False}}
    #plot it
    sw.plot(display_fraction=1, width=500, height=500, style=style, percentile=80)

def plotTract(tractIn):
    import numpy as np
    from dipy.viz import window, actor
    renderer = window.Scene()
    stream_actor = actor.line(tractIn)
    #renderer.set_camera(position=(-176.42, 118.52, 128.20),
    #               focal_point=(113.30, 128.31, 76.56),
    #                view_up=(0.18, 0.00, 0.98))
    get_ipython().run_line_magic('matplotlib', 'inline')
    renderer.add(stream_actor)
    
    window.show(renderer, size=(600, 600), reset_camera=True)

def updateFunction(clusterIndex):
        
    currentIndexes=neckClusters.clusters[clusterIndex].indices
    subTractogram=extractSubTractogram(sourceTractogram,currentIndexes)
    get_ipython().run_line_magic('matplotlib', 'inline')
    plotParcellationConnectionWidget(subTractogram.streamlines)


# In[ ]:


streamCountVec=np.zeros(len(neckClusters))    
for iClusters in range(len(neckClusters)):
    streamCountVec[iClusters]=len(neckClusters.clusters[iClusters].indices)
print(np.argsort(streamCountVec))


# In[ ]:


from ipywidgets import interact, interactive, fixed, interact_manual
from ipywidgets import IntSlider

#establish interactivity
interact(updateFunction, 
         clusterIndex=IntSlider(min=0, max=len(neckClusters), step=1,continuous_update=False)
        )


# In[ ]:





# In[ ]:




