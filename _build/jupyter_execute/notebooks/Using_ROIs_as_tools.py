#!/usr/bin/env python
# coding: utf-8

# # _Using_ ROIs as tools
# 
# In the previous chapter ("ROIs as tools") we considered ROIs as tools _independent of any specific application_ .  This gave us a feel for both their characteristics as data objects (and how they are generated/formed) _as well as_ the manner in which they represent particular volumes of space in the brain.  Establishing this conceputal link and how to leverage ROI tools in concert with our knowledge of brain anatomy is _essential_ to performing advanced, automated, and high-quality white matter anatomy segmentations
# 
# Thus, having established **what** an ROI is lets begin to take a look at how to use them.  We'll begin with perhaps the most common form of an ROI, a planar ROI.
# 
# ## A first pass use of an ROI in a segmentation
# 
# In the previous chapter ("ROIs as tools") we initially generated (planar) ROIs by arbitrarily selecting a dimension and a coordinate.  For a first pass demonstration of using an ROI to sub-select streamlines we can adopt the same strategy.
# 
# In the interactive visualization below you will be able to select a coordinate, dimension _and_ an instruction as to whether you would like to **include** or **exclude** streamlines that pass through the plane you have created.  **Be warned**:  if you select a criteria that is particularly generous (in that it sub-selects many streamlines) the selection and/or visualization process may take a moment to execute.  Given that a single exclusion criteria can only be so effective, this is more likely to be an issue using **exclude** than **include**.
# 
# The next three code cells are divided in such a way as to facilitate ease of use.  They are:
# 
# - 1. The loading cell, which loads the relevant data objects
# - 2. The plane definition cell, which allows the user to define and view their planar ROI
# - 3. The segmentation cell, which applies the planar ROI as a segmentation criterion. 
# 
# In order to perform a preliminary segmentation operation you'll have to load the data in cell 1, define a plane in cell 2, and then apply and view the segmentation in cell 3.  Subsequent segmentation demonstrations in this chapters will not require you to reload the data, and so will only have portions corresponding to cells 2 and 3.
# 
# IMPORTANT NOTE: given that the output of the ROI definition cell feeds in to the segmentation cell, the user is instructed to specify their ROI parameters **before** clicking through to the next cell.  Neglecting to do this (and/or rapidly clicking the run button) will run the ROI generation and applications steps with their default values, which may not always provide an informative demonstration.

# In[1]:


#Loading cell: loads relevant objects

#this code ensures that we can navigate the WiMSE repo across multiple systems
import subprocess
import os
#get top directory path of the current git repository, under the presumption that 
#the notebook was launched from within the repo directory
gitRepoPath=subprocess.check_output(['git', 'rev-parse', '--show-toplevel']).decode('ascii').strip()

#establish path to the wma_tools repo
wma_toolsDirPath=os.path.join(gitRepoPath,'wma_pyTools')   

#change to the wma_tools path, load the function set, then change back to the top directory
os.chdir(wma_toolsDirPath)
import WMA_pyFuncs
os.chdir(gitRepoPath)

import nibabel as nib
from nilearn.plotting import plot_roi
import matplotlib

#establish path to t1
t1Path=os.path.join(gitRepoPath,'exampleData','t1.nii.gz')   

#import the data
t1img = nib.load(t1Path)
import numpy as np
#done to establish bounds of image in acpc space
fullMask = nib.nifti1.Nifti1Image(np.ones(t1img.get_fdata().shape), t1img.affine, t1img.header)
#pass full mask to boundary function
t1DimBounds=WMA_pyFuncs.returnMaskBoundingBoxVoxelIndexes(fullMask)
#convert the coords to subject space in order set max min values for interactive visualization
convertedBoundCoords=nib.affines.apply_affine(t1img.affine,t1DimBounds)


smallTractogramPath=os.path.join(gitRepoPath,'exampleData','smallTractogram.tck')
streamsObjIN=nib.streamlines.load(smallTractogramPath)

#get tractogram from the Tck holder
sourceTractogram=streamsObjIN.tractogram



# In[2]:


#ROI definition cell: defines the ROI for later use

naiveDimDictionary={'x':0,'y':1,'z':2}

def genAndViewPlanarROI(planeCoord,dimension,xCoord,yCoord,zCoord):
    
    from nilearn import plotting
    import nibabel as nib
    import numpy as np
    
    #refuse to plot if coord is outside of dim bound
    if np.logical_or(np.min(convertedBoundCoords[:,naiveDimDictionary[dimension]])>planeCoord,                     np.max(convertedBoundCoords[:,naiveDimDictionary[dimension]])<planeCoord):
        print('requested coordinate exceeds selected dimension\'s bounds')
    else:    
        segPlane=WMA_pyFuncs.makePlanarROI(t1img, planeCoord, dimension)
    
        get_ipython().run_line_magic('matplotlib', 'inline')
        plotting.plot_roi(roi_img=segPlane, bg_img=t1img, cut_coords=[xCoord,yCoord,zCoord])
        
from ipywidgets import interact, interactive, fixed, interact_manual
from ipywidgets import Dropdown
from ipywidgets import IntSlider

#establish objects for visualization interaction

dimList=list(['x','y','z'])

dimension=Dropdown(options=dimList, description="dimension for plane")
planeCoord=IntSlider(min=np.min(convertedBoundCoords.astype(int)), max=np.max(convertedBoundCoords.astype(int)), step=1,continuous_update=False)
  

interact(genAndViewPlanarROI,     dimension=dimension,     planeCoord=planeCoord,      xCoord=IntSlider(min=np.min(convertedBoundCoords[:,0].astype(int)), max=np.max(convertedBoundCoords[:,0].astype(int)), step=1,continuous_update=False),      yCoord=IntSlider(min=np.min(convertedBoundCoords[:,1].astype(int)), max=np.max(convertedBoundCoords[:,1].astype(int)), step=1,continuous_update=False),     zCoord=IntSlider(min=np.min(convertedBoundCoords[:,2].astype(int)), max=np.max(convertedBoundCoords[:,2].astype(int)), step=1,continuous_update=False))
    


# In[3]:


#Segmentation application:  Segments the tractogram using the previously generated ROI

#generate the roi from the preceeding visualization using the output
segPlane=WMA_pyFuncs.makePlanarROI(t1img, planeCoord.value, dimension.value)
    
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
def plotSegmentedStreamsWidget(subTractogram):
    #import widget
    from niwidgets import StreamlineWidget
    #set widget object
    
    sw = StreamlineWidget(streamlines=subTractogram)
    #set plotting characteristics
    style = {'axes': {'color': 'red',
                  'label': {'color': 'white'},
                  'ticklabel': {'color': 'white'},
                  'visible': True},
         'background-color': 'black',
         'box': {'visible': True}}
    #plot it
    sw.plot(display_fraction=1, width=1000, height=1000, style=style, percentile=0)
    #sw.plot(display_fraction=1, width=1000, height=1000, percentile=0)
    

    
def updateFunction(instruction):
    import numpy as np
    import matplotlib.pyplot as plt  

    if instruction == 'Include':
        instruction=True
    else:
        instruction=False

    #use the criteria application function to find the relevant streamlines
    streamBool=WMA_pyFuncs.applyNiftiCriteriaToTract(sourceTractogram.streamlines, segPlane, instruction, 'any')
    
    streamsToPlot=extractSubTractogram(sourceTractogram,np.where(streamBool)[0])
    
    plotSegmentedStreamsWidget(streamsToPlot.streamlines)
    
    from niwidgets import NiftiWidget
    
    #curFig=ipyv.pylab.gcf()
    #ipyv.pylab.view(distance=100)
    

        
    
from ipywidgets import interact, interactive, fixed, interact_manual
from ipywidgets import Dropdown
from ipywidgets import IntSlider

#establish objects for visualization interaction

instructionList=list(['Include','Exclude'])

interact(updateFunction,     instruction=Dropdown(options=instructionList, description="instruction"))


# ### Considering the output of a single planar ROI
# 
# As you might be able to tell, the use of a single planar ROI does not return a coherent segmentation.  Indeed, typically most segmentations requre a number of criteria in order to return a coherent anatomical structure (i.e. a white matter tract).  Furthermore, even when performing a multi criteria segmentation, it turns out that a _full_ planar ROI is still too coarse (particularly when used as an _inclusion_ criteria--as an exclusion criteria, it can suffice just fine).  In effect (though not quite, as will be discussed later), all that one is doing with a full planar ROI is indexing _all_ streamlines which traverse the specified coordinate.  This is not a very delicate operation.  In the next section we'll consider how to use partial planar ROIs (as we were introduced to in the previous chapter) and see how much more useful they can be.
# 
# ## A modified planar ROI
# 
# As you'll likely note from the following interactive plot there are several more parameters that you (the user) must provide.  These include
# 
# - 1.  The "planeCoord" for the intial plane (as before)
# - 2.  The dimension for the intial plane (as before)
# - 3.  The "planeCoord" for the new "cut" plane
# - 4.  The dimension for the new "cut" plane
# - 5.  Which portion of the intial plane to keep after the cut has been performed
# 
# Indeed, this is a more complicated action than the creation of a simple planar ROI.  Moreover, it is possible for the user to make malformed requests (i.e. requests that, _a priori_, will result in an error)--there is only so much guard railing that can be provided here.  Some examples of potential ways to generate errors with the following widget:
# 
# - 1.  Attempting to apply a cut to a plane using another plane in the same dimension (i.e. "x" and "x").  The two planes will be parallel (if not identical) to one another, and so they will not intersect in an orthogonal fashion
# - 2.  Attempting to request coordinates that are outside of the dimension's bounds.
# - 3.  Attempting to keep a portion of a plane that does not have a sensible interpretation with respect to the source plane (i.e. trying to keep the "anterior" portion of a cut Y plane)
# 
# The code below attempts to return informative feedback when malform requests have been made, but it is likely still possible to create such requests which will not return informative feedback.
# 
# For an informative demo, try and segment the streamlines passing superior to the corpus callosum.  This means setting the following parameters:
# 
# - 1.  planeCoord=-26
# - 2.  dimension=y
# - 3.  cutCoord=24
# - 4.  cutDim=z
# - 5.  superior

# In[4]:


naiveDimDictionary={'x':0,'y':1,'z':2}

def genAndViewPlanarROI(planeCoord,dimension,cutCoord,cutDim,keepPortion,xCoord,yCoord,zCoord):
    
    from nilearn import plotting
    import nibabel as nib
    import numpy as np
    import pandas as pd
    
    #refuse to plot if coord is outside of dim bound
    if np.any([np.min(convertedBoundCoords[:,naiveDimDictionary[dimension]])>planeCoord,               np.max(convertedBoundCoords[:,naiveDimDictionary[dimension]])<planeCoord,               np.min(convertedBoundCoords[:,naiveDimDictionary[cutDim]])>cutCoord,               np.max(convertedBoundCoords[:,naiveDimDictionary[cutDim]])<cutCoord]):
        print('requested coordinate exceeds selected dimension\'s bounds')
    else:    
        segPlane=WMA_pyFuncs.makePlanarROI(t1img, planeCoord, dimension)
        
        #first though we need to generate a planar ROI to "cut" with
        knife_roi=WMA_pyFuncs.makePlanarROI(t1img, cutCoord , cutDim)

        cutPlaneTable=WMA_pyFuncs.findMaxMinPlaneBound(knife_roi)
        
        #refuse to plot if improper keep dimension is requested
        if np.logical_not(naiveDimDictionary[cutDim]==cutPlaneTable['dimIndex'].loc[cutPlaneTable['boundLabel']==keepPortion].to_numpy(int)):
            print('requested keep portion not consistent with cut plane')
        elif naiveDimDictionary[cutDim]==naiveDimDictionary[dimension]:
            print('intial plane and cut plane are parallel, no meaningful intersection will occur.')
        else:

            #now cut the roi_img ROI
            cut_roi=WMA_pyFuncs.sliceROIwithPlane(segPlane,knife_roi,keepPortion)
    
            get_ipython().run_line_magic('matplotlib', 'inline')
            plotting.plot_roi(roi_img=cut_roi, bg_img=t1img, cut_coords=[xCoord,yCoord,zCoord])
        
from ipywidgets import interact, interactive, fixed, interact_manual
from ipywidgets import Dropdown
from ipywidgets import IntSlider

#establish objects for visualization interaction

dimList=list(['x','y','z'])
portionList=list(['posterior','anterior','caudal','rostral', 'medial','lateral','left', 'right','inferior','superior'])

dimension=Dropdown(options=dimList, description="dimension for initial plane")
planeCoord=IntSlider(min=np.min(convertedBoundCoords.astype(int)), max=np.max(convertedBoundCoords.astype(int)), step=1,continuous_update=False)
cutDim=Dropdown(options=dimList, description="dimension for cut plane")
cutCoord=IntSlider(min=np.min(convertedBoundCoords.astype(int)), max=np.max(convertedBoundCoords.astype(int)), step=1,continuous_update=False)
keepPortion=Dropdown(options=portionList, description="portion of initial plane to keep")   

interact(genAndViewPlanarROI,     dimension=dimension,     planeCoord=planeCoord,      cutCoord=cutCoord,     cutDim=cutDim,      keepPortion=keepPortion,      xCoord=IntSlider(min=np.min(convertedBoundCoords[:,0].astype(int)), max=np.max(convertedBoundCoords[:,0].astype(int)), step=1,continuous_update=False),      yCoord=IntSlider(min=np.min(convertedBoundCoords[:,1].astype(int)), max=np.max(convertedBoundCoords[:,1].astype(int)), step=1,continuous_update=False),     zCoord=IntSlider(min=np.min(convertedBoundCoords[:,2].astype(int)), max=np.max(convertedBoundCoords[:,2].astype(int)), step=1,continuous_update=False))
    


# In[5]:


#Segmentation application:  Segments the tractogram using the previously generated ROI

#generate the roi from the preceeding visualization using the output
segPlane=WMA_pyFuncs.makePlanarROI(t1img, planeCoord.value, dimension.value)
knife_roi=WMA_pyFuncs.makePlanarROI(t1img, cutCoord.value , cutDim.value)
cut_roi=WMA_pyFuncs.sliceROIwithPlane(segPlane,knife_roi,keepPortion.value)
    
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
def plotSegmentedStreamsWidget(subTractogram):
    #import widget
    from niwidgets import StreamlineWidget
    #set widget object
    
    sw = StreamlineWidget(streamlines=subTractogram)
    #set plotting characteristics
    style = {'axes': {'color': 'red',
                  'label': {'color': 'white'},
                  'ticklabel': {'color': 'white'},
                  'visible': True},
         'background-color': 'black',
         'box': {'visible': True}}
    #plot it
    sw.plot(display_fraction=1, width=1000, height=1000, style=style, percentile=0)
    #sw.plot(display_fraction=1, width=1000, height=1000, percentile=0)
    

    
def updateFunction(instruction):
    import numpy as np
    import matplotlib.pyplot as plt  

    if instruction == 'Include':
        instruction=True
    else:
        instruction=False

    #use the criteria application function to find the relevant streamlines
    streamBool=WMA_pyFuncs.applyNiftiCriteriaToTract(sourceTractogram.streamlines, cut_roi, instruction, 'any')
    
    streamsToPlot=extractSubTractogram(sourceTractogram,np.where(streamBool)[0])
    
    plotSegmentedStreamsWidget(streamsToPlot.streamlines)
    
    from niwidgets import NiftiWidget
    
    #curFig=ipyv.pylab.gcf()
    #ipyv.pylab.view(distance=100)
    

        
    
from ipywidgets import interact, interactive, fixed, interact_manual
from ipywidgets import Dropdown
from ipywidgets import IntSlider

#establish objects for visualization interaction

instructionList=list(['Include','Exclude'])

interact(updateFunction,     instruction=Dropdown(options=instructionList, description="instruction"))


# In[ ]:





# ## Once more, but this time with a sphere
# 
# Lets try performing another cursory segmentation, but this time we'll us a sphere.  Because of how a sphere works in practice (at least as a singleton criteria) we'll constrain the demo to using the ROI as an **inclusion** criterion.  As such we'll perform the segmentation in two steps, only one of which is interactive:
# 
# - 1.  Define the location and radius of the sphere
# - 2.  Apply the segmentation criteria and view the output
# 
# Hint: a good demonstration of a how to use a sphere in a segmentation requires a careful application.  Try placing your sphere at the [splenium of the corpus callosum](https://en.wikipedia.org/wiki/Corpus_callosum#Structure) using the coordinate [0,25,0].

# In[6]:


#ROI definition cell: defines the ROI for later use

def genAndViewSphereROI(sphereXCoord,sphereYCoord,sphereZCoord,sphereRadius,xCoord,yCoord,zCoord):
    
    from nilearn import plotting
    import nibabel as nib
    import numpy as np
    
    #refuse to plot if coord is outside of dim bound
    if np.any(      [np.min(convertedBoundCoords[:,0])-sphereRadius>sphereXCoord,                      np.max(convertedBoundCoords[:,0])+sphereRadius<sphereXCoord,                      np.min(convertedBoundCoords[:,1])-sphereRadius>sphereYCoord,                      np.max(convertedBoundCoords[:,1])+sphereRadius<sphereYCoord,                      np.min(convertedBoundCoords[:,2])-sphereRadius>sphereZCoord,                      np.max(convertedBoundCoords[:,2])+sphereRadius<sphereZCoord]):
        print('requested coordinate and radius pairing exceeds selected dimension\'s bounds')
    else:    
        segSphere=WMA_pyFuncs.createSphere(sphereRadius, [sphereXCoord,sphereYCoord,sphereZCoord], t1img)
    
        get_ipython().run_line_magic('matplotlib', 'inline')
        plotting.plot_roi(roi_img=segSphere, bg_img=t1img, cut_coords=[xCoord,yCoord,zCoord])
        
from ipywidgets import interact, interactive, fixed, interact_manual
from ipywidgets import Dropdown
from ipywidgets import IntSlider

#establish objects for visualization interaction

#establish dynamic boundary specification at a later date using .observe methodology
#def updateCoordBoundaries(*args):
#    sphereXCoord.min=np.min(convertedBoundCoords[:,0]).astype(int)-sphereRadius
#    sphereXCoord.max=np.max(convertedBoundCoords[:,0]).astype(int)+sphereRadius
#    https://ipywidgets.readthedocs.io/en/latest/examples/Using%20Interact.html#Arguments-that-are-dependent-on-each-other

sphereRadius=IntSlider(min=1, max=30, step=1,continuous_update=False,description="sphere radius")
sphereXCoord=IntSlider(min=np.min(convertedBoundCoords[:,0]).astype(int), max=np.max(convertedBoundCoords[:,0]).astype(int), step=1,continuous_update=False,description="sphere X coordinate")
sphereYCoord=IntSlider(min=np.min(convertedBoundCoords[:,1]).astype(int), max=np.max(convertedBoundCoords[:,1]).astype(int), step=1,continuous_update=False,description="sphere Y coordinate")
sphereZCoord=IntSlider(min=np.min(convertedBoundCoords[:,2]).astype(int), max=np.max(convertedBoundCoords[:,2]).astype(int), step=1,continuous_update=False,description="sphere Z coordinate")

interact(genAndViewSphereROI,     sphereRadius=sphereRadius,     sphereXCoord=sphereXCoord,     sphereYCoord=sphereYCoord,     sphereZCoord=sphereZCoord,     xCoord=IntSlider(min=np.min(convertedBoundCoords[:,0].astype(int)), max=np.max(convertedBoundCoords[:,0].astype(int)), step=1,continuous_update=False),      yCoord=IntSlider(min=np.min(convertedBoundCoords[:,1].astype(int)), max=np.max(convertedBoundCoords[:,1].astype(int)), step=1,continuous_update=False),     zCoord=IntSlider(min=np.min(convertedBoundCoords[:,2].astype(int)), max=np.max(convertedBoundCoords[:,2].astype(int)), step=1,continuous_update=False))
    


# In[7]:


#Segmentation application:  Segments the tractogram using the previously generated ROI

#generate the roi from the preceeding visualization using the output
segSphere=WMA_pyFuncs.createSphere(sphereRadius.value, [sphereXCoord.value,sphereYCoord.value,sphereZCoord.value], t1img)
    
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
def plotSegmentedStreamsWidget(subTractogram):
    #import widget
    from niwidgets import StreamlineWidget
    #set widget object
    
    sw = StreamlineWidget(streamlines=subTractogram)
    #set plotting characteristics
    style = {'axes': {'color': 'red',
                  'label': {'color': 'white'},
                  'ticklabel': {'color': 'white'},
                  'visible': True},
         'background-color': 'black',
         'box': {'visible': True}}
    #plot it
    sw.plot(display_fraction=1, width=1000, height=1000, style=style, percentile=0)
    #sw.plot(display_fraction=1, width=1000, height=1000, percentile=0)

    
import numpy as np
import matplotlib.pyplot as plt  

#use the criteria application function to find the relevant streamlines
streamBool=WMA_pyFuncs.applyNiftiCriteriaToTract(sourceTractogram.streamlines, segSphere, True , 'any')
    
streamsToPlot=extractSubTractogram(sourceTractogram,np.where(streamBool)[0])
    
plotSegmentedStreamsWidget(streamsToPlot.streamlines)


# ### Considering the output of a single spherical ROI
# 
# The output of a sphere-based segmentation (and its sensibility/interpretability) is _highly_ dependant on the placement of the sphere's centroid and the selection of its radius.  If you used the recomended coordinate for the [splenium of the corpus callosum](https://en.wikipedia.org/wiki/Corpus_callosum#Structure), [0,25,0], you ought to have obtained a streamline collection that roughly corresponds to the forceps major.  Alternatively, if you selected a different location (or perhaps slected a radius that was too large) it is possible that your result may resemble more of a hairball than a coherent structure.  This is because a spherical ROI, when used as an inclusion criterion (and when used to detect _any_ volumetric traversal), can be just as generous as a planar ROI, if not moreso.
# 
# #### How generous is a sphere?
# 
# Although a planar ROI spans an entire dimension, and thus manifests as a point cloud with tens of thousands of coordinates (~182^2=33124 in the case of a Y plane ROI using the current T1 image as a refrence), only a fraction of those coordinates overap with voxels that could validly carry streamlines.  As an illustration of this we can note that a Y plane at coordinate value 32 would overlap with about 3320 valid voxels, which would be comperable to a spherical ROI with a with radius of about 9.3 mm (though, as should be clear by this point, when operating with NiFTI based ROIs we are exclusively working with integer based values).  The true difference between these two methods become more stark when we consider what the application of a single criteria of either kind essentially translates to for human users.
# 
# ### What are we doing when we segment with a sphere or a plane?
# 
# In either the spherical or planar case, when we use an ROI as an _inclusion_ criteria to segment streamlines we are **essentially\*** asking if any streamlines traverse the volumes that correspond to those ROIs.  When we use an ROI as an _exclusion_ criteria we are essentially (and, in fact, [actually](https://github.com/DanNBullock/wma_pyTools/blob/eedc973f8810d9f449b704c1e1d45bb05ab3902c/WMA_pyFuncs.py#L715)) just negating this output.  Regardless, in the case of the planar ROI this basically* boils down to whether or not the streamline crosses the plane in question.  The use of a spherical ROI is a bit more complicated though, in that it essentially segments any streamline that comes within the specified radius value of the centroid point.  Thus, in a manner of speaking, a spherical ROI is better thought of as indicating extremely specific point in the brain (the specified centroid value) _and_ an associated value (in the form of the radius) relating to uncertianty or variability--a tolerance of sort.  For example, if you were relatively certian about the route traversed by your track of interest you might provide a particularly conservative value.  On the other end of the spectrum, if you were less sure, you could provide a more generous value, and then attempt to further constrain your streamlines by the application of additional segmentation criteria.
# 
# ## Practical notes on ROI use (up to this point)
# 
# Thus far, the usage cases of ROIs for segmentation have necessarily relied on the user to specify a coordinate.  As such the manner in which we have defined and used ROIs for segmentation is decidedly "manual".  If our goal is to develop reliable, high-quality (and possibly automatable) segmentations, then we'll need to do better.  Manual segmentation is still a viable approach, and one which is often applied in medical settings (when performed by experts).  Typically such individuals place their planar and spherical ROIs by referring to an anatomical scan (i.e. a T1) and selecting their coordinates based on positions relative to landmark structures.  Indeed this insight will prove to be central as we develop our anatomically-based segmentaton abilities in later chapters.
# 
# Before we move on to anatomically-based segmentations, we need to make note of some general concerns that apply to segmentations generally.
# 
# ## Those pesky asterisks 
# 
# Earlier in this chapter, you may have noticed that several asterisks were used to qualify what was actually goin on when a segmentation criteria was applied.  The notion of "traversal" and "intersection" was appealed to, but we never really provided details as to what sort of mathematical operation was being performed when we applied a segmentation criterion. In essence: we do this by determining, for each streamline, if **any** coordinate from the streamline is within some distance threshold (i.e. .5 mm) of any coordinate of the ROI.  In practice, this ends up being moderately computationally expensive.  Why?  Because, for each coordinate of the streamline, our intersection algorithm has to compute the distance between that coordinate, and each coordinate of the ROI (which equals [number of streamline nodes] * [number of ROI coordinates] computations). Indeed, one of the algorithmic speed-ups we use is [only considering streamlines that have **any** nodes within the ROI bounds](https://github.com/DanNBullock/wma_pyTools/blob/eedc973f8810d9f449b704c1e1d45bb05ab3902c/WMA_pyFuncs.py#L656) and, among those streamlines, [only those nodes that fall within the ROI bounds](https://github.com/DanNBullock/wma_pyTools/blob/eedc973f8810d9f449b704c1e1d45bb05ab3902c/WMA_pyFuncs.py#L704).  Given that we're having to compute the distances between all coordinates in an ROI and all nodes in streamline, it might seem like we should sample either these a bit more sparsely.  That would be a bad idea insofar as segmentation is concerned.  To see why, lets consider two important caviots about how segmentation is performed. 
# 
# ### Segmentation caviot 1 - the tolerance distance
# A careful and attentive reader of the preceeding paragraph will note that the mathematical operation we described doesn't actually directly map on to the notion of "traversal".  Indeed, as it turns out there are certian circumstances where the operation would return a true (i.e. "this streamline meets the specified criteria") for a given streamline even though the streamline didn't actually "intersect" or "traverse" the ROI.  How?  Imagine that we had a planar ROI and a streamline that traveled perfectly perpendicular with it, such that it got to within the threshold distance of the planar ROI _but never actually crossed it_.  Indeed, the streamline doesn't even need to travel alongside the planar ROI the entire time--it could just move to within the threshold distance, and then move away again (so long as at least one node meets this criteria).  In either case the algorithm we just described would still return a True for that streamline.  But this isn't the only problem.
# 
# ### Segmentation caviot 2 - not all streamlines are created (or stored) equal
# In addition to the aforementioned possibility, it's also possible that this algorithm (which is, in essence, the one that is typically used in segmentation) might **fail to detect** a streamline that we would consider to be intersecting with the ROI.  How?  If we think back to our previous discussion of step-sizes between streamline nodes, we realize that its possible for there to actually be fairly sizable amounts of distance between nodes, particularly if the streamlines have been ["compressed"](https://dipy.org/documentation/1.0.0./examples_built/streamline_length/).  If the inter-node distance is enough to where the streamline "traverses" the ROI (i.e. there are nodes on either side of the ROI), but no individual node is within the distance threshold, then the algorithm will fail to detect this intersection.  For example, if the nearest nodes on either side of a planar ROI are 2 mm from the plane, but the threshold distance is .5, the "intersection" will go unnoticed.  This is particularly an issue with planar ROIs, but less so with fuller, volumetric ROIS (e.g. spheres).  
# 
# For the moment, there's really nothing we can do about these possibilities.  In the first case, we may not be too worried about it, since .5 is pretty close, and we'd probably be comfortable calling that an intersection.  In the latter case, we're probably not comfortable with that outcome, but we can safeguard against it by ensuring that our streamlines are sampled at a rate that takes into account the threshold distance of our intersection algorithm.  Regardless, having made note of these issues, we can move on to anatomically based segmentations.
