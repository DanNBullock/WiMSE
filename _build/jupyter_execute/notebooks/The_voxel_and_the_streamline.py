#!/usr/bin/env python
# coding: utf-8

# # The voxel and the streamline
# 
# In our earlier chapters we considered the manner in which a particular voxel of a T1 NIfTI image represented some quantative feature of the measured volume/brain.  Representing white matter is somewhat different though.  The key features of white matter that we'd like to capture with our representation are (minimally) its connectivity and its traversal.  In this chapter we'll look at how our data representation of white matter acheives this. 

# ## What's in a streamline?
# 
# Before moving into a discussion of **how** our model of white matter anatomy is generated, we should consider an essential difference between the data representation of the T1 and the data reprsentation of white matter (i.e. tractography):
# 
# T1 images and other NIfTI data objects represent the brain with voxel-value pairings, such that each volume of represented space is associated with a quantative measure of that space.  As an arbitrary example, within some spatial frame of reference (i.e. scanner space, ACPC space, etc) a measured volume represented in the nifti image's data field at coordinate (128,120, 80) could have value of 125.32.  Relatedly, this is in much the same fashion that the 2 dimensional images that we discussed previously represent each area of depicted space with a value (or in the case of a standard color image, 3 values corresponding to RGB values).  Our most common method for representing white matter, which we refer to as "[Tractography](https://en.wikipedia.org/wiki/Tractography)", **does not** operate in this fashion.  To see why lets refer back to the table that was provided just before we began our consideration of digital photography.
# 
# |   | **Digital Photography** | **Structural Brain Imaging (T1)** | **Diffusion Imaging (DWI)** | **Tractography** |
# | --- | --- | --- | --- | --- |
# | _Data Token_ | digital photo image | structural brain image (T1)| diffusion image (DWI) | tractogram |
# | _Object represented_ | visual scene | cranium / brain | cranium / brain | white matter of brain |
# | _Source system_ | camera | MRI scanner | MRI scanner | Mathematical model  | 
# | _Source phenomena_ | reflected light | water / magnetic properties | water movement | orientation interpolation |
# | _Property of interest_ | topography | volumetric occupancy | tissue structure | putative axon collection traversal |
# | _File extension_ | .jpg, .png ... | .nifti, nii.gz | (dwi) .nifti, nii.gz | .fg, .trk, .tck |
# | _Metadata_ | exif | header | header | varies by format |
# | _Data size_ | 100s kb - 1s MB | ~2.5 - 5 MB | 50 MB - 1.5 GB |500 MB - 10 GB |
# | _Data dimensionality_ | &quot;2D&quot;(3 RGB layers) | 3D | 4D |1D nested? |
# | _Data &quot;atoms&quot;_ | pixels | voxels | voxel-angle |vectors (streamlines) |
# | _Data &quot;atom&quot; content_ | integer | float |float |ordered float sequence (nodes) |
# 
# 
# Note that the data "atoms" of tractography are **streamlines**.  The term **streamline** is borrowed from the field of [fluid dynamics](https://en.wikipedia.org/wiki/Fluid_dynamics), where it has a [disipline-specific connotation](https://en.wikipedia.org/wiki/Streamlines,_streaklines,_and_pathlines).  In the field(s) of white matter anatomy and tractography though, it has quite another meaning:
# 
# In this context, a streamline is an ordered sequence of nodes (roughly in line with the [graph theoretic](https://en.wikipedia.org/wiki/Graph_theory) sense of ["node"](https://en.wikipedia.org/wiki/Vertex_(graph_theory)) in 3 dimensional space.  The specific numerical values describing the positions of the nodes are, like the specification of the anterior or posterior comissure in a NIfTI affine, referenced to a specific coordinate scheme (typically the source DWI scan).  Although there are a finite number of these nodes in any given streamline, they should nonetheless be understood as represnting a **smooth** and **continuous** path through the white matter of a corresponding brain. This path **should not** be interpreted as representing a **single** axon.  The scans whose data we are basing our streamline models off of can not resolve details as fine as single axons, nor can our models realistically generate the number streamlines that would be necessary to do this.  As such, it would be better to interpret a streamline as "our best guess as to the path of traversal for a collection of axons continuously oriented in the same direction". The specifics of how these guesses are generated fom DWI scan data are discussed elsewhere (within the context of tractography generation algorithms), but for now this description is sufficient to begin considering *how* streamlines and collections of streamlines represent the brain's white matter.  
# 
# **Lets consider how the data constituting a streamline is arranged**

# In[1]:


import nibabel as nib
import numpy as np
import os
#this code ensures that we can navigate the WiMSE repo across multiple systems
import subprocess
#get top directory path of the current git repository, under the presumption that 
#the notebook was launched from within the repo directory
gitRepoPath=subprocess.check_output(['git', 'rev-parse', '--show-toplevel']).decode('ascii').strip()

#move to the top of the directory
os.chdir(gitRepoPath)

# load a tractography file with a single streamline in it
streamsObjIN=nib.streamlines.load(os.path.join(gitRepoPath,'exampleData','singleStream.tck'))

# determine the number of streamlines
print(list(np.shape(streamsObjIN.tractogram.streamlines)))


# Above, we have loaded a .tck file ("singleStream.tck") and then printed out the dimensions of the object storing streamlines.  We see that it is 1 by 142 by 3.  This indicates that there is 1 streamline with 142 nodes, and there are X, Y, and Z coordinates for each of these nodes.  This is a fairly unique tractography file, in that it only has one streamline in it.  Typically, a tractography file will contain many more streamlines than this.  Indeed, in the case of a tractography file that is representing an entire brain's white matter, it will likely have millions of streamlines.  For now though, we'll focus on just one streamline to get a sense of what a streamline is, data-wise.  Let's look at its contents more closely.

# In[2]:


print(streamsObjIN.tractogram.streamlines[0])


# In the above output we see the X, Y, and Z coordinates for each node (across each row).
# 
# ### What are some observations we can make?
# 
# Working with the assumption that these are ACPC-based coordinates (which is reasonable, given that negative values are not possible in an [image-space coordinate system](https://www.slicer.org/wiki/Coordinate_systems#Image_coordinate_system)), we can infer severeal positional characteristics of our streamline by noting the sign of the node coordinates, which are all negative.  That all of these coordinates are negative indicates that this streamline is located in the left hemisphere (from the X coordinates), in the posterior of the brain (from the Y coordinates), and in the inferior portion of the brain (from the Z coordinates).  Additionally, by looking at the relative sequencing and variability of the coordinates, we can further infer that this is an anterior-posterior oriented (i.e. primarily along the Y axis) tract due to the orderly progression of coordinate values in the second column.
# 
# In order to learn more about this streamline we'll need to perform more rigorous assesments of its quantative characteristics.

# In[3]:


import numpy as np

# compute the distance between the respective X Y and Z coordinates of each node
nodeDimDiffs=np.diff(streamsObjIN.tractogram.streamlines[0],axis=0)

#treat each of these as the side of a 3 dimensional triangle, and, as we
#did in the chapter with satellite ocean masking, hypotenuse
#compute elementwise square
elementWiseSquares=np.square(nodeDimDiffs)

#compute the sum for each row (i.e. node distance)
rowSquareSums=np.sum(elementWiseSquares,axis=1)

#compute the square root of these values
#NOTE: these are the internode distances
rowRootSquareSums=(np.sqrt(rowSquareSums))
print('internode distances')
print(rowRootSquareSums)
print('\n average internode distance')
print(np.mean(rowRootSquareSums))
print('\n standard deviation of internode distances')
print(np.std(rowRootSquareSums))
print('\n total distance traversed by streamline (in mm)')
print(np.sum(rowRootSquareSums))

#now, for the sake of some more advanced characterization of the streamline,
#lets also consider it's displacement
#get first and last en
endpoint1=streamsObjIN.tractogram.streamlines[0][1,:]
endpoint2=streamsObjIN.tractogram.streamlines[0][-1,:]
#obtain the difference between these points
firstLastNodeDimDiff=np.subtract(endpoint1,endpoint2)
#compute the hypotenuse between these points
streamlineDisplacement=np.sqrt(np.sum(np.square(firstLastNodeDimDiff)))
print('\n total displacement of streamline (in mm)')
print(streamlineDisplacement)


# Above we can observe a number of quantative features of our streamline.  
# 
# By looking at the collection of internode distances we can get a sense of the regularity of the node spacing for this streamline.  They all appear to be about .125 mm apart, as indicated by the average internode distance and the extremely low standard deviation for this value.  This is attributable to the method by which most tractography is generated.  Specifically, many tractography generation algorithms feature a parameter which defines the internode distance (often referred to as "step size").  This value is particularly small (i.e. fine grained) considering that the voxel size for our data source (dMRI) is likely between 1.5 and 2 mm.  this means that many of the same nodes are based on the same data reading and so the implied precision of this streamline likely exceeds the actual precision of our source data.  It's also worth noting that not all streamlines or tractograms have evenly spaced nodes.  Some algorithms or methods resample streamlines in such a way that areas with sharper curvatures (e.g. more change) have more nodes, and straighter portions have fewer nodes.  As we'll note in later lessons, this could have unintended consequences when performing other analyses.
# 
# Another set of features worth considering are the total traversal distance and total displacement of the streamline.  The total traversal distance value is, essentially, the "length" of the streamline.  Were we to treat the streamline as though it were a wire, it would be the total length of wire needed to form the streamline.  Alternatively, the total displacement value of the streamline is the distance between its first and last node.  There are several things to note about the relation between these values.  First and foremost, the total displacement is *necessarily* less than or equal to distance traversed.  In the case of a perfectly straight line, these two values would be equal, but any amount of curvature or deviation leads to the length being longer than the displacement.  As a consequence of this, the relative ratio of these two values can also give you a sense of how curved and/or "efficient" the streamline is.  If the displacement is much smaller than the distance traveled, it suggests that the streamline is very curved and that the endpoints are quite close to one another (at least relative to the total path-length traversed by the streamline).  Conversely, if the two are closer in value, this suggests that the streamline is relatively straight and does not curve much as it traverses the brain.
# 
# Thus far we have looked at a single streamline, but in order model the entirety of the brain's white matter, we need many of these streamlines.  In many cases our streamline models contain several million streamlines, and this number increases as the computational resources available to our field improves.  In the next chapter we'll look at a whole brain tractogram to get a sense of what individual streamlines come to form when they are amalgamated into a tractogram structure.  In the end, what we'll find is that we need a way to limit our consideration of the tractogram to meaningful subsets of streamlines.  In making this observation we'll set the stage for our first attempt at a white matter parcellation/segmentation.

# In[ ]:




