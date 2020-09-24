#!/usr/bin/env python
# coding: utf-8

# # A first segmentation
# 
# In the previous chapter we examined a single streamline.  In this chapter we will perform a "segmentation" of sorts, wherein we divide up the whole brain tractogram.  One of the challenges we experienced in the previous chapter was that the whole brain tractogram is unweildy and we need the ability to look a specific sub-components of the tractogram in order to systematically make insights about our model of the brain's white matter.  But how would we do this?
# 
# ### How would you systematically divide up the white matter?
# We find ourselves in a position similar to the one we were in when considering the satellite images.  We need to narrow our consideration of the available data to more meaningful and useful sub-components.  But how would we do this with a whole brain tractogram?  Well, perhaps we can make use of another analogy we discussed earlier, namely the role of white matter as the "highways of the brain".  If we consider the various regions of the brain to be like the states of the United States, and the white matter to be the roads that connect them, perhaps we could sub-select based on where the roads begin and end.  After all, both white matter tracts and roads have to begin and end somewhere.
# 
# To to acheive our goal of tractogram sub-selection we can leverage the parcellation data we were looking at previously.  This data object assigns each voxel a label, and so we can--for each streamline--determine which labels its endpoints are closest to.
# 
# Lets begin by loading the parcellation once more

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
#reset the indexes, whicj were disrupted by the previous operation
#currentParcellationEntries=currentParcellationEntries.reset_index(drop=True)
currentParcellationEntries.tail(20)


# Now that we have the parcellation loaded, we can load our whole brain tractogram and perform the iterative assignment of streamlines to atlas labels.  In this way, each streamline will be assigned two numbers corresponding to the label number closest to its first and last node.  This method is at the heart of the field of [connectomics](https://en.wikipedia.org/wiki/Connectomics), and so it is not surprising that a great deal of research and ingenuity has been applied to developing software and algorithms for this approach.  In fact, [dipy](https://dipy.org/) has a very straightfoward function for this. 
# 
# Lets apply it now and look at the outputs.  We'll also plot an interactive visualization of the parcellation that can help serve as a reference for these sub-dividisions.
# (Note, this is a non-trivial set of computations, and so executing the next block my

# In[2]:


# load the tractography file into the streamsObjIN variable
smallTractogramPath=os.path.join(gitRepoPath,'exampleData','smallTractogram.tck')

streamsObjIN=nib.streamlines.load(smallTractogramPath)


from dipy.tracking import utils
#segment tractome into connectivity matrix from parcellation
M, grouping=utils.connectivity_matrix(streamsObjIN.tractogram.streamlines, atlasImg.affine, label_volume=atlasData.astype(int),
                        return_mapping=True,
                        mapping_as_streamlines=False)


# In[3]:


#this code ensures that we can navigate the WiMSE repo across multiple systems
import subprocess
import os
#get top directory path of the current git repository, under the presumption that 
#the notebook was launched from within the repo directory
gitRepoPath=subprocess.check_output(['git', 'rev-parse', '--show-toplevel']).decode('ascii').strip()

#move to the top of the directory
os.chdir(gitRepoPath)

import nibabel as nib
#establish path to parcellation
atlasPath=os.path.join(gitRepoPath,'exampleData','parc.nii.gz')
#load it as an object
atlasImg = nib.load(atlasPath)

from niwidgets import NiftiWidget
#plot it
atlas_widget = NiftiWidget(atlasImg)
atlas_widget.nifti_plotter(colormap='nipy_spectral')


# In the above table we can get a sense of which labels have the most streamlines connecting one another.  There's a number of things to note and keep in mind about these results.
# 
# -all streamlines are assigned
# -this assignment reveals that not all streamlines are biologically valid
# -
# 
# 
# Given the assignment we've just performed, we can also selectively visualize sub-selections of streamlines based on which parcellation labels the streamline terminations are closest to.
# 
# NOTE: not all labels share streamlines, and even amongst those that do, there may only be a few streamline that meet the connectivity criterion.

# In[4]:


#get tractogram from the Tck holder
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
    #check to make sure this pairing is actually in the connections
    if (regionIndex1,regionIndex2) in grouping.keys(): 
        currentIndexes=grouping[regionIndex1,regionIndex2]
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


# In[ ]:




