#!/usr/bin/env python
# coding: utf-8

# # Biological Plausibility for Tractograms
# 
# In the previous chapter, we considered an approach to parcellation that iteratively went through pairings of the labels in a volumetric parcellation atlas and assigned streamlines to groups based on those pairings.  By examining the result of this process we were able to make several insights.  One of these is that many of the streamlines found in tractograms are not **biologically plausible**.  What do we mean by this?
# 
# ## What does it mean for a streamline to be biologically plausible
# 
# In the previous chapter we presented the following criteria for a streamline to be considered biologically plausible
# 
# > it must terminate in reasonable areas and follow a sensible path as it traverses the brain
# 
# But what do we mean by these criteria?
# 
# ### "terminate in reasonable areas"
# 
# As we noted in a previous chapter describing the biological role of white matter, axons connect neurons to one another.  As such, an axon must begin and end in areas of the brain which house neurons.  Because streamlines ostensibly "represent" collections of axons, streamlines are expected to do the same.  With that in mind, although many areas of the brain that do house neuronal bodies, there are some areas which definitionally do not.  As such we can exclude streamlines which terminate in these areas from any subsequent segmentation, because they couldn't possibly represent a collection of axons.  Lets list a few of these areas below
# 
# - Hemispheric white matter 
# - Ventricles
# - "Unknown" areas
# - "Unlabeled" areas (i.e. values of 0)
# - On the midline of the corpus callosum
# 
# Lets reuse some of the code from the previous chapter to consider these.  Once the code has processed, and you can interact with the widget, take a look at collections of streamlines that are associated with areas in the above list.  Although these may not seem particularly remarkable upon visual inspection, they are nonetheless biologically implausible.

# In[1]:


#this code ensures that we can navigate the WiMSE repo across multiple systems
import subprocess
import os
#get top directory path of the current git repository, under the presumption that 
#the notebook was launched from within the repo directory
gitRepoPath=subprocess.check_output(['git', 'rev-parse', '--show-toplevel']).decode('ascii').strip()

#move to the top of the directory
os.chdir(gitRepoPath)

import nibabel as nib
import numpy as np

atlasPath=os.path.join(gitRepoPath,'exampleData','parc.nii.gz')
#load it as an object
atlasImg = nib.load(atlasPath)
atlasData = atlasImg.get_fdata()
#set the print option so it isn't printing in scientific notation
np.set_printoptions(suppress=True)
#condense to unique values
uniqueAtlasEntries=np.unique(atlasData).astype(int)

import pandas as pd
FSTablePath=os.path.join(gitRepoPath,'exampleData','FreesurferLookup.csv')
#read table using pandas
FSTable=pd.read_csv(FSTablePath)
#create a boolean vector for the indexes which are in uniqueAtlasEntries
currentIndexesBool=FSTable['#No.'].isin(uniqueAtlasEntries)
#create new data frame with the relevant entries
currentParcellationEntries=FSTable.loc[currentIndexesBool]

smallTractogramPath=os.path.join(gitRepoPath,'exampleData','smallTractogram.tck')
streamsObjIN=nib.streamlines.load(smallTractogramPath)

#because of how dipy does connectivity matrtricies, we have to relabel the atlas
remappingFrame=currentParcellationEntries.reset_index(drop=True)
#establish a copy
relabeledAtlas=atlasData.copy()
#iterate across unique label entries
for iLabels in range(len(remappingFrame)):
    #replace the current uniqueAtlasEntries value with the iLabels value
    #constitutes a simple renumbering schema
    relabeledAtlas[relabeledAtlas==uniqueAtlasEntries[iLabels]]=iLabels

from dipy.tracking import utils
#segment tractome into connectivity matrix from parcellation
M, grouping=utils.connectivity_matrix(streamsObjIN.tractogram.streamlines, atlasImg.affine, label_volume=relabeledAtlas.astype(int),
                        return_mapping=True,
                        mapping_as_streamlines=False)

resetTable=remappingFrame.reset_index()


# Now that the segemetation has been performed we can visualize the results

# In[2]:


dropDownList=list(zip(currentParcellationEntries['LabelName:'].to_list(), currentParcellationEntries['#No.'].to_list()))

sourceTractogram=streamsObjIN.tractogram

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

def updateFunction(regionIndex1,regionIndex2):
    currentRenumberIndex1=resetTable['index'].loc[resetTable['#No.']==regionIndex1].values[0]    
    currentRenumberIndex2=resetTable['index'].loc[resetTable['#No.']==regionIndex2].values[0]    
 
    
    #check to make sure this pairing is actually in the connections
    if (currentRenumberIndex1,currentRenumberIndex2) in grouping.keys(): 
        currentIndexes=grouping[currentRenumberIndex1,currentRenumberIndex2]
        subTractogram=extractSubTractogram(sourceTractogram,currentIndexes)
        get_ipython().run_line_magic('matplotlib', 'inline')
        plotParcellationConnectionWidget(subTractogram.streamlines)
    else:
        print('connection not present')

dropDownList=list(zip(currentParcellationEntries['LabelName:'].to_list(), currentParcellationEntries['#No.'].to_list()))

from ipywidgets import interact, interactive, fixed, interact_manual
from ipywidgets import Dropdown

#establish interactivity
interact(updateFunction, 
         regionIndex1=Dropdown(options=dropDownList, value=2, description="region1"), 
         regionIndex2=Dropdown(options=dropDownList, value=2, description="region2"),
        )


# If you look closely at the example streamline collections, you may also notice some streamlines that seem particularly... odd.  This brings us to our other criterion.
# 
# ### "follow a sensible path as it traverses the brain"
# 
# As noted in our discussion of the biological characteristics of axons, although they are very small they nonetheless occupy space.  For this reason, longer axons take up more room than shorter axons.  Many researchers [cite pareto optimality and such] have explored the costs associated with increasingly large volumes of white matter, and one overarching observation is that there is a general efficiency to the paths taken by axons:  they don't meander about unnecessarily or take wild detours.  Moreover, as an axon becomes longer, so too does the amount of time needed to transmit signals down it.  On an evolutionary scale, those delays can mean the difference between life and death.  As such we see that there are multiple selection pressures which might preference efficient white matter connections.  How can we identify streamlines which best reflect this characteristic?
# 
# #### What ISN'T a sensible path?
# 
# In the above visualization, if you select "Left-Cerebral-White-Matter" for both endpoints (which is admittedly already a biologically implausible category) you'll notice that three streamlines appear to cross the corpus callosum into the right hemisphere, but then do a 180 and return to the left hemisphere.  It's safe to assume that an axon (much less a collection of axons) wouldn't do this.  In the same way that we applied a mask to the image examples in previous chapters, is there a way for us to apply a filter to the tractogram to select only those streamlines that are doing something implausible like this? 
# 
# In our chapter introducing streamlines (The voxel and the streamline) two of the measures we computed were the displacement and length of the streamline.  By creating a ratio of these values we can compute the "efficiency" of a streamline--the degree to which the actual route taken by the streamline approaches a straight line (the most efficient way in which the streamline could connect the two points).  It must be admitted from the outset that this isn't actually the minimum *biologically plausible* route that the streamline could take.  The route taken by a maximally efficient streamline (i.e. a line) could very well take the streamline straight across ventricles, sulci, or cerebrospinal fluid.  All of these would be impossible in an actual brain, but in this null model of maximal efficiency, it's a useful starting point.
# 
# In the code block below we'll compute the efficiency for all of the streamlines in our tractogram and then utilize an interactive plot to visualize those streamlines that are below a the provided threshold efficiency value.  Try manually entering a value of .05 to see particularly inefficient streamlines.

# In[3]:


#initalize vector
streamlineEfficiencies=np.zeros(len(streamsObjIN.tractogram.streamlines))

for iStreamlines in range(len(streamsObjIN.tractogram.streamlines)):
    # compute the distance between the respective X Y and Z coordinates of each node
    currNodeDimDiffs=np.diff(streamsObjIN.tractogram.streamlines[iStreamlines],axis=0)

    #treat each of these as the side of a 3 dimensional triangle, and, as we
    #did in the chapter with satellite ocean masking, hypotenuse
    #compute elementwise square
    currElementWiseSquares=np.square(currNodeDimDiffs)

    #compute the sum for each row (i.e. node distance)
    currRowSquareSums=np.sum(currElementWiseSquares,axis=1)
    
    #compute the square root of these values
    #NOTE: these are the internode distances
    rowRootSquareSums=(np.sqrt(currRowSquareSums))
    
    #sum internode distances to get stream length
    currStreamLength=np.sum(rowRootSquareSums)
    
    #extract endpoints
    endpoint1=streamsObjIN.tractogram.streamlines[iStreamlines][1,:]
    endpoint2=streamsObjIN.tractogram.streamlines[iStreamlines][-1,:]
    #obtain the difference between these points
    firstLastNodeDimDiff=np.subtract(endpoint1,endpoint2)
    #compute the hypotenuse between these points
    currStreamlineDisplacement=np.sqrt(np.sum(np.square(firstLastNodeDimDiff)))
    streamlineEfficiencies[iStreamlines]=currStreamlineDisplacement/currStreamLength

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
    sw.plot(display_fraction=1, width=500, height=500, style=style, percentile=0)

def updateFunction(thresholdVal):   
    import numpy as np
    #get the indexes of the relevant streamlines and convert it to a useful format
    currentIndexes=np.squeeze(np.argwhere(streamlineEfficiencies<thresholdVal))
    subTractogram=extractSubTractogram(sourceTractogram,currentIndexes)
    get_ipython().run_line_magic('matplotlib', 'inline')
    plotParcellationConnectionWidget(subTractogram.streamlines)


from ipywidgets import interact, interactive, fixed, interact_manual
from ipywidgets import FloatSlider

#establish interactivity
interact(updateFunction, 
         thresholdVal=FloatSlider(value=np.mean(streamlineEfficiencies), min=0, max=1,step=.001, description="Efficiency Threshold", disabled=False, continuous_update=False, orientation='horizontal', readout=True, readout_format='.1f')
        )
#NOTE: EFFECIENCY SLIDER APPEARS TO BE BE BROKEN, STEP SIZE ISN'T RESPONSIVE TO PARAMETER INPUT


# ## Other Concerns for Biological Plausibility
# 
# ## Why care about biological plausibility, and what to do about it
