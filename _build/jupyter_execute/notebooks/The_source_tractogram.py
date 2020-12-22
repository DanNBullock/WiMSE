#!/usr/bin/env python
# coding: utf-8

# # The source tractogram
# 
# To begin to explore our tractography model, we first have to load the fibergroup.  There are several different file standards for storing tractography including .tck, .trk and .fg.  Despite their differences, they are alike in that they are composed of some finite number of streamlines.   

# In[1]:


#this code ensures that we can navigate the WiMSE repo across multiple systems
import subprocess
import os
#get top directory path of the current git repository, under the presumption that 
#the notebook was launched from within the repo directory
gitRepoPath=subprocess.check_output(['git', 'rev-parse', '--show-toplevel']).decode('ascii').strip()

#move to the top of the directory
os.chdir(gitRepoPath)

import matplotlib
import nibabel as nib
import numpy as np

# load the tractography file into the streamsObjIN variable
smallTractogramPath=os.path.join(gitRepoPath,'exampleData','smallTractogram.tck')

#same for T1
t1Path=os.path.join(gitRepoPath,'exampleData','t1.nii.gz')

# load the tractography file into the streamsObjIN variable
streamsObjIN=nib.streamlines.load(smallTractogramPath)

# determine the number of streamlines
streamCount=list(np.shape(streamsObjIN.tractogram.streamlines))
print(streamCount)


# Above we see the total number of streamlines contained within this tractogram.  Typically we would want a million or more in order to adequately cover the entire white matter of the brain.  Here though, we are working with a smaller number as it is easier to use in a notebook.
# 
# Lets plot a random selection of 10 of these streamlines so we can get a sense of what streamlines look like when visualized

# In[17]:





# In[19]:


randomIndexes=np.random.randint(streamCount, size= 10)

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

subTractogram=extractSubTractogram(streamsObjIN,randomIndexes)
get_ipython().run_line_magic('matplotlib', 'inline')
plotParcellationConnectionWidget(subTractogram.streamlines)


# What you should see (after zooming in) is a random collection of colored "strings" floating in space.  Each of these strings represents the tractography algorithm's (the algorithm that generated all of the streamliens in the tractogram) best guess as to where there's "likely" a coherent bundle of axons.  Although it's difficult to tell from this visualization the coloring of these lines corresponds to the direction in which the streamline is primarily traveling.  Green indicates that the streamline is primarily anterior-posteriorly oriented, blue indicates that the streamline is primarily superior-inferiorly oriented, and red indicates that the streamline is primarily left-right oriented.
# 
# To get a beter sense of the meaning of these colors, and how these individual streamlines can come together to reprsent the white matter of the brain, it's useful to look at the entire tractogram

# In[20]:


get_ipython().run_line_magic('matplotlib', 'inline')
plotParcellationConnectionWidget(streamsObjIN.streamlines)


# Thats quite a mess!  Even so, we can begin to see how the streamlines come together to represent the white matter of the brain. Keep in mind though that we only have a fraction of the streamlines that we would typically use to model a brain's white matter.  Regardless, what now?
# 
# #### Now that we have a whole brain tractogram how do we garner insight?
# 
# As it turns out there are really only a limited number of quantative assesments that can be applied directly to a whole tractography object.  For example you could create a histogram of the streamline lengths composing the tractogram, but this wouldn't give you very useful insight about the brain.
# 
# The problem we face here is not unlike the problem we faced when dealing with digital images.  In those cases we needed to to some form of post-processing in order to obtain more quantative and 
