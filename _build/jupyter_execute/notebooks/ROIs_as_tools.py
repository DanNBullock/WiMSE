#!/usr/bin/env python
# coding: utf-8

# # ROIs as tools
# 
# In our previous chapters on images and NiFTIs the elementary action of "masking" was discussed.  In essence, what we were doing there was selecting a subset of the object's elements based on the application of some quantative criteria.  In the digital 2-D image we used distance from a color, while in the brain NiFTI case we used whether or not a particular voxel corresponded to a given label in an associated parcellation.  Conceptually we're not doing anything that different in the case of tractograms and streamlines:  we want to subselect some finite number of the streamlines in a tractogram in accordance with an explicitly selected criterion.  So how do we do that?  We use a Region of Interest (ROI) (and a streamline's relation to it).  Lets consider ROIs a bit more closely.
# 
# ### What is an ROI?
# 
# In practice, a Region of Interest can be stored in a number of ways, but the specifics of this are beyond the scope of our purpose.  What we want to know is "what is the fundamental characteristic of an ROI that makes it of use to us?".  At its heart, an ROI, in the context of streamline/tractogram segmentation, is a [point cloud](https://en.wikipedia.org/wiki/Point_cloud): a set of X, Y, and Z coordinates corresponding to points in the same relative coordinate space as your tractogram. Whereas the streamlines of a tractogram are an ordered sequence of coordinates, the coordinates of an ROI are not in any particular order.  Typically, they are used to define a particular volume of space and are sampled in a regular fashion, forming a 3-D lattice.  Often times these take the shape of a sphere or plane.  In a moment, we will begin by creating an example (and formatless) planar ROI. 

# ## ROIs in practice
# 
# It is worth noting that the [ROI description provided above](#what_is_an_roi?) is quite general, and imposes only the most limited constraints on what an ROI could actually be.  For example, there is nothing precluding an investigator from creating a single point ROI, or at the other extreme, an ROI spanning the entire reference volume (i.e. the volume of space that the ROI is sub-selecting from).  In practice though, there are certian general categories of ROIs that tend to be used, due to the kinds of kinds of queries/applications they can be used for.  Lets consider a few of these now:
# 
# ### A planar ROI
# 
# A _full_ plane is a special case of a region of interest.  Specifically, it constitutes a "flat" (in that it exhibits the minimum level of thickness possible, in one dimension) set of coordinates which (in the case of a _full_ plane ROI) extend the full span of the "other" dimensions of the reference space.  For example, a planar ROI located at X = -20, would be a plane extending the _entire_ Y and Z dimensions, but only occupying a single "slice" in the X dimension.  Note that, the essential characteristics for specifying a planar ROI are:
# 
# - 1. The coordinate of interest
# - 2. The dimension of interest
# 
# Lets interact with an example at **-20** in the **X** plane.  Note the use of _WMA_pyFuncs.makePlanarROI_ with these inputs to generate the desired ROI.  As you move the X slider (labeled _xCoord_) throught the X dimension, notice that the entire saggital image changes color, indicating the presence of the ROI/mask. 

# In[1]:


#this code ensures that we can navigate the WiMSE repo across multiple systems
import subprocess
import os
#get top directory path of the current git repository, under the presumption that 
#the notebook was launched from within the repo directory
gitRepoPath=subprocess.check_output(['git', 'rev-parse', '--show-toplevel']).decode('ascii').strip()

#establish path to the 
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

#use a wma_tools function to make a planar roi.
roi_img=WMA_pyFuncs.makePlanarROI(t1img, -20 , 'x')

import numpy as np
#done to establish bounds of image in acpc space
fullMask = nib.nifti1.Nifti1Image(np.ones(t1img.get_fdata().shape), t1img.affine, t1img.header)
#pass full mask to boundary function
t1DimBounds=WMA_pyFuncs.returnMaskBoundingBoxVoxelIndexes(fullMask)
#convert the coords to subject space in order set max min values for interactive visualization
convertedBoundCoords=nib.affines.apply_affine(t1img.affine,t1DimBounds)

from ipywidgets import interact, interactive, fixed, interact_manual
from ipywidgets import IntSlider

#wrapper for interactive visualization
def rotateAndPlotWrapper(xCoord,yCoord,zCoord):
    from nilearn import plotting
    import nibabel as nib
    import numpy as np

    get_ipython().run_line_magic('matplotlib', 'inline')
    plotting.plot_roi(roi_img=roi_img, bg_img=t1img, cut_coords=[xCoord,yCoord,zCoord])
    
interact(rotateAndPlotWrapper,     xCoord=IntSlider(min=np.min(convertedBoundCoords[:,0].astype(int)), max=np.max(convertedBoundCoords[:,0].astype(int)), step=1,continuous_update=False),      yCoord=IntSlider(min=np.min(convertedBoundCoords[:,1].astype(int)), max=np.max(convertedBoundCoords[:,1].astype(int)), step=1,continuous_update=False),     zCoord=IntSlider(min=np.min(convertedBoundCoords[:,2].astype(int)), max=np.max(convertedBoundCoords[:,2].astype(int)), step=1,continuous_update=False))


# ### A partial planar ROI
# 
# A full plane ROI isn't the only trick we have up our sleeve.  It's also possible to "cut" the full plane ROI to obtain a partial plane ROI.  Note that, in order to do this we would need to provide:
# 
# - 1. The coordinate to cut the original ROI
# - 2. The dimension along which that [singleton] cut coordinate should be interpreted
# - 3. The portion of the original ROI we want to keep, provided in relative anatomical terms.
# 
# Note how this is done by using _WMA_pyFuncs.makePlanarROI_ to make _knife\_roi_, and then how 'posterior' is used with _WMA\_pyFuncs.sliceROIwithPlane_

# In[2]:


#use a wma_tools function to make a planar roi.
#roi_img=WMA_pyFuncs.makePlanarROI(t1img, -20 , 'x')
#we already have this from the previous run, so lets use it here

#first though we need to generate a planar ROI to "cut" with
knife_roi=WMA_pyFuncs.makePlanarROI(t1img, 0 , 'y')

#now cut the roi_img ROI
cut_roi=WMA_pyFuncs.sliceROIwithPlane(roi_img,knife_roi,'posterior')

from ipywidgets import interact, interactive, fixed, interact_manual
from ipywidgets import IntSlider

#wrapper for interactive visualization
def rotateAndPlotWrapper(xCoord,yCoord,zCoord):
    from nilearn import plotting
    import nibabel as nib
    import numpy as np

    get_ipython().run_line_magic('matplotlib', 'inline')
    plotting.plot_roi(roi_img=cut_roi, bg_img=t1img, cut_coords=[xCoord,yCoord,zCoord])
    
interact(rotateAndPlotWrapper,     xCoord=IntSlider(min=np.min(convertedBoundCoords[:,0].astype(int)), max=np.max(convertedBoundCoords[:,0].astype(int)), step=1,continuous_update=False),      yCoord=IntSlider(min=np.min(convertedBoundCoords[:,1].astype(int)), max=np.max(convertedBoundCoords[:,1].astype(int)), step=1,continuous_update=False),     zCoord=IntSlider(min=np.min(convertedBoundCoords[:,2].astype(int)), max=np.max(convertedBoundCoords[:,2].astype(int)), step=1,continuous_update=False))



# ### A spherical ROI
#  
# The construction of a spherical ROI proceeds in much the same was as a planar roi, except the point cloud lattice now extends in 3 dimensions.  There are two important characteristics for a spherical ROI which can, in essence, sum up (or be used to generate) the sphere.
# 
# - 1.  The center coordinate
# - 2.  The radius
# 
# 
# Lets generate a spherical ROI now.  We will be using a [ready-made function](https://github.com/cosanlab/nltools/blob/91822a45778415ee2cdded7134e60bcde2bb7814/nltools/mask.py#L50) taken from the [nitools toolkit](https://github.com/cosanlab/nltools/tree/91822a45778415ee2cdded7134e60bcde2bb7814) to generate this example sphere (centered at 0,0,0)

# In[3]:


radius=10
point=[0,0,0]
outputSphereNifti=WMA_pyFuncs.createSphere(radius, point, t1img)

from nilearn import plotting
import nibabel as nib
import numpy as np
def rotateAndPlotWrapper(xCoord,yCoord,zCoord):
    get_ipython().run_line_magic('matplotlib', 'inline')
    plotting.plot_roi(roi_img=outputSphereNifti, bg_img=t1img, cut_coords=[xCoord,yCoord,zCoord])
    
interact(rotateAndPlotWrapper, xCoord=IntSlider(min=np.min(convertedBoundCoords[:,0].astype(int)), max=np.max(convertedBoundCoords[:,0].astype(int)), step=1,continuous_update=False),  yCoord=IntSlider(min=np.min(convertedBoundCoords[:,1].astype(int)), max=np.max(convertedBoundCoords[:,1].astype(int)), step=1,continuous_update=False), zCoord=IntSlider(min=np.min(convertedBoundCoords[:,2].astype(int)), max=np.max(convertedBoundCoords[:,2].astype(int)), step=1,continuous_update=False))


# ### A modified spherical ROI
# 
# it is also possible to modify this spherical ROI in the same way that we modified the planar ROI.  As before we have to provide:
# 
# - 1. The coordinate to cut the original ROI
# - 2. The dimension along which that [singleton] cut coordinate should be interpreted
# - 3. The portion of the original ROI we want to keep, provided in relative anatomical terms.
# 
# Lets cut the sphere from the previous example in half, at the origin and keep the anterior half.

# In[4]:


#first though we need to generate a planar ROI to "cut" with
knife_roi=WMA_pyFuncs.makePlanarROI(t1img, 0 , 'y')

#now cut the roi_img ROI
cutSphere_roi=WMA_pyFuncs.sliceROIwithPlane(outputSphereNifti,knife_roi,'anterior')

from ipywidgets import interact, interactive, fixed, interact_manual
from ipywidgets import IntSlider

#wrapper for interactive visualization
def rotateAndPlotWrapper(xCoord,yCoord,zCoord):
    from nilearn import plotting
    import nibabel as nib
    import numpy as np

    get_ipython().run_line_magic('matplotlib', 'inline')
    plotting.plot_roi(roi_img=cutSphere_roi, bg_img=t1img, cut_coords=[xCoord,yCoord,zCoord])
    
interact(rotateAndPlotWrapper,     xCoord=IntSlider(min=np.min(convertedBoundCoords[:,0].astype(int)), max=np.max(convertedBoundCoords[:,0].astype(int)), step=1,continuous_update=False),      yCoord=IntSlider(min=np.min(convertedBoundCoords[:,1].astype(int)), max=np.max(convertedBoundCoords[:,1].astype(int)), step=1,continuous_update=False),     zCoord=IntSlider(min=np.min(convertedBoundCoords[:,2].astype(int)), max=np.max(convertedBoundCoords[:,2].astype(int)), step=1,continuous_update=False))


# ### An anatomically defined ROI
# 
# Finally, and certianly not lastly, we can generate ROIs by using pre-existing anatomical atlases.  We only need provide the following:
# 
# - A reference anatomical atlas/parcellation (volumetric)
# - An indicator of which label we would like extracted (typically a name or an integer)
# 
# This turns out to be an extremely useful capability which we will explore in subsequent chapters.  Below you'll be able to select the anatomically related ROI and view its location in the brain.
# 
# Remember back to the example of a multi object map from when we were considering 2 dimensional satellite images (chapter "Multi object maps in images").  This is, in essence, the same sort of masking operation, except that (1) we're now doing it in 3 dimensions and (2) we are no longer having to use color-distance as a proxy as the labeled entires are provided directly to is un the form of integer labels (see chapter "How to interpret a volumetric brain segmentation" for a review)
# 
# Note:  Its possible to modify anatomically defined ROIs in the same fashion as we modified planar and spherical ROIs previously.  We'll save that for a more advanced lesson though.

# In[5]:


#establish path to t1
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

dropDownList=list(zip(currentParcellationEntries['LabelName:'].to_list(), currentParcellationEntries['#No.'].to_list()))


#import the data
atlasImg = nib.load(atlasPath)

def rotateAndPlotWrapper(roiNum,xCoord,yCoord,zCoord):
    from nilearn import plotting
    import nibabel as nib
    import numpy as np
    
    anatomicalROI=WMA_pyFuncs.roiFromAtlas(atlasImg,roiNum)
    
    get_ipython().run_line_magic('matplotlib', 'inline')
    plotting.plot_roi(roi_img=WMA_pyFuncs.alignROItoReference(anatomicalROI,t1img), bg_img=t1img, cut_coords=[xCoord,yCoord,zCoord])
    
from ipywidgets import Dropdown

interact(rotateAndPlotWrapper,     roiNum=Dropdown(options=dropDownList, value=2, description="anatomicalLabel"),     xCoord=IntSlider(min=np.min(convertedBoundCoords[:,0].astype(int)), max=np.max(convertedBoundCoords[:,0].astype(int)), step=1,continuous_update=False),      yCoord=IntSlider(min=np.min(convertedBoundCoords[:,1].astype(int)), max=np.max(convertedBoundCoords[:,1].astype(int)), step=1,continuous_update=False),     zCoord=IntSlider(min=np.min(convertedBoundCoords[:,2].astype(int)), max=np.max(convertedBoundCoords[:,2].astype(int)), step=1,continuous_update=False))


# In[ ]:




