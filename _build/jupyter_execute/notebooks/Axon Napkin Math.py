#!/usr/bin/env python
# coding: utf-8

# 
# 
# In the case of **gray matter**, it is the activity of the neurons that is of particular salience, however a static image cannot capture this.  As such, researchers often turn to functional MRI scanning to assess the activities of cortical tissue over a given period of time. In this way, the data structure for fMRI is extended over a 4th dimension, time.  This allows researchers to investigate how blood oxygen levels (**BOLD**, a proxy measure for neural activity) evolve over time, and associate these changes with experimental manipulations. However, the **white mater** does not contain neuron bodies, and thus typically does not exhibit the kind of biophysical processes that are measured by fMRI. Moreover, what we are intreseted in, relative to **white matter** is not it's *activity* but rather, its *connectivity*.  Just as fMRI does not measure brain/neuronal activity directly, the imaging modality used in the study of **white mater**, diffusion MRI, doesn't measure the characteristic of interest (axonal structure/connectivity) directly.  Instead, diffusion MRI measures the propensity of water to move in a specific direction.  Because **myelin** (the lipid-dense neural structure component which gives white matter it's lighter apperance) restricts water from escaping out of an axon, water thus tends to move in a direction that is perpindicular to the axon (in other words, along the length of the axon). 
# 
# Each of these more specialized approaches to investigating brain tissue requires a specialized processing method. In both cases, the processing is specific to a given voxel, as is the characteristic that is to be inferred from looking at these measures.  For fMRI, the temporal structure of the **BOLD** signal must be inferred from the changes observed between sampling time points (i.e. slices in the fMRI data object's 4th dimension).  For dMRI the axonal structure must be inferred from a multitude of measurements (taken at various angular orientations) of water's diffusion propensity.  Interestingly though, in order to explore connective characteristics of the white matter, this derived model of diffusion propensity must be used as the foundation for the generation of another model which attempts to encapsulate the gross axonal structure of the white matter.
# 
# 

# Given that we are attempting to use these brain images for research, it seems that we would want these to be of the highest resolution possble so that we can see the brain's constiuent components in in fine detail.  Given our previous look at nifti data stuctures, we know that the resolution is actually fairly coarse (~ 1mm^3).  But just for the sake of argument, lets think about how many voxels would it take to represent the brain on a cellular level.  
# 
# **What sort of information would we need to make an informed estimate about this?**
# 
# Well, first we would need an estimate of how many neurons are in the cerebral cortex. Herculano-Houzel notes in a 2009 review (https://doi.org/10.3389/neuro.09.031.2009) that a good estimate of this number is actually a recent development, and that most numbers cited were unsubstantiated.  The number provided by Herculano-Houzel is **16 billion** neurons in the cerebral cortex (though **69 billion** appear to be located in the cerebellum), and approximately **85 billion non-neuronal cells**
# 
# 

# In[ ]:





# In[1]:


#preloading and processing
import nibabel as nib
import numpy as np
t1Path='/Users/plab/Documents/JupyerData/proj-5c50b6f12daf2e0032f880eb/sub-100206/dt-neuro-anat-t1w.tag-acpc_aligned.tag-brain_extracted.id-5c57072befbc2800526291bb/t1.nii.gz'
img = nib.load(t1Path)
print('Voxel dimensions for T1 (in mm)')
voxelDims=img.header.get_zooms()
print(voxelDims)
print('')

volData = img.get_fdata()
unwrappedData=np.ndarray.flatten(volData)

def largeVal(n):
    return n>0

result=map(largeVal,unwrappedData)
largeBool=list(result)
largeNum=sum(largeBool)
print('Number of non zero (data containing) voxels')
print(largeNum)


# In[2]:


#lets assume all cells are layed out in a latice matrix (i.e. they are all orthogonal to each other and they can thus be represented as a matrix.)
print('Estimated number neurons')
#citation
neuronNum=100000000000
print(neuronNum)
print('')

print('Estimated number of glia')
gliaNum=neuronNum*10
print(gliaNum)
print('')




#neuronBodySize=25*10^-6
#gliaBodySize=15*10^-6

#neuronVolume=[neuronBodySize^3]*neuronNum
#gliaVolume=[gliaBodySize^3]*gliaNum

totalCellNum=neuronNum+gliaNum

print('Number of cells per voxel (estimate)')
cellPerVox=totalCellNum/largeNum
print(cellPerVox)


print('Number of cells per cubic mm (estimate)')
cellPerMM=cellPerVox/(voxelDims[0]*voxelDims[1]*voxelDims[2])
print(cellPerMM)
print('')

axonNum=neuronNum

print('Current data storage usage for T1')
import os
statinfo = os.stat(t1Path)
T1bytes=statinfo.st_size
print(f'{T1bytes} bytes' )
T1gigabytes=T1bytes/1073741824
print(f'{T1gigabytes} gigabytes' )
print('')

print('Storage for a ')
perCellT1bytes=cellPerVox*largeNum*8
print(f'{percellT1bytes} bytes' )
perCellT1gigabytes=perCellT1bytes/1073741824
print(f'{perCellT1gigabytes} gigabytes' )




# In[ ]:




