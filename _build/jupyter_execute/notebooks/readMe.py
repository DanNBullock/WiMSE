#!/usr/bin/env python
# coding: utf-8

# # White Matter Segmentation Education (WiMSE)
# 
# This set of notebooks has been developed to provide a guide to performing digital segmentations of white matter.  It's lessons are designed for advanced undergraduates, advanced STEM students, or persons wanting to become more familiar with the process of the digital segmentation of white matter.  These lessons begin by building a strong foundation of intuitions based on everyday data representations.  Having established this, it moves towards neuroimaging-specific data formats and their use.  Finally, it moves to tractograms and segmentations, demonstrating basic concepts and characteristics, and even allowing users to perform some rudamentary interactive segmentations. 
# 
# ## Chapter Summaries 
#  
# ### Building intuitions with digital images
# 
# #### Why are we talking about JPEGs
# 
# If this notebook is about the computational study of white matter, why are we taking about image data formats? In this chapter relationships between images, representations, and data objects are introduced. Across various data formats (e.g. digital photographs, T1 images, DWI, & tractography), we'll note analogous traits which will help us build intuitions as we progress through subsequent chapters.
# 
# #### Intro to discretized image representation & maps
# 
# In this chapter we begin our exploration of image data with an example that will likely be familiar to many readers: a digital photograph. We'll begin by looking at the how the data is arranged within the image data object, what its constituent data entries are, and how those features relate to the image we encounter on our screen.  We'll then move to an exploration of how the quantitive features of the image data can be leveraged to select certain sub-sections of the image via a process referred to as "masking"
# 
# #### Aligning two images
# 
# In this chapter we build upon the previous chapter's introduction of masks by interactively attempting to overlay a mask derived from one image onto another image.  We also qualitatively assess how well the two images have been aligned. This will serve as a prelude to using the mask from one image to extract certain sub-sections from another image.
# 
# #### Multi object maps in images
# 
# In this chapter we leverage our ability to align images to select pixels corresponding to US states from a satellite image of the continental United States.  This capability serves as a direct analogy to our ability to select portions of a NIfTI image via the use of a parcellation, which will be explored in later chapters.
# 
# #### A consideration of jpegs and brain images
# 
# In this chapter we reflect on our observations about digital images as we begin to transition to working with NIfTI data objects.
# 
# ### Working with NIfTI data
# 
# #### How to represent the brain's anatomy - as a volume
# 
# In this chapter we shift from a consideration of 2 dimensional, color digital photographs to MRI data stored in a NIfTI.  Although there are a number of conceptual similarities between these data modalities, there are also a number of important distinctions which we consider here.  We also take a look at the affine information contained within the NIfTI header, and reflect on its relevance to aligning 2 dimensional images.
# 
# #### A quick demonstration of linear affine transformations in 3-D
# 
# In this chapter we consider very briefly how to implement linear transforms and rotations in 3 dimensions.  Given that there are [other, more detailed resources available](https://nipy.org/nibabel/coordinate_systems.html), this is primarily a hands on demonstration so that users can become familiar with the concept.
# 
# ### White matter and tractography
# 
# #### Highways of the brain
# 
# In this chapter we move on from our consideration of volumetric/NIfTI based neuroimaging data and begin to consider white mater and tractography.  Here, we provide a brief introduction to relevant anatomical concepts related to white matter.  This is primarly a discussion of anatomy, and so no code interactivity is present.
# 
# #### The measurement, the object, and the modality - What's measured in diffusion imaging
# 
# In this chapter we introduce the Diffusion Weighted Imaging (DWI) scan.  Harkening back to our discussions of digital images, we use the concept of a GIF and taking photographs of a rotating object to help explain how a DWI scan captures information about the structure of the brain.
# 
# #### The voxel and the streamline 
# 
# In this chapter we take a look at the actual data characteristics of a streamline, the elementary component of a tractogram.  We look at a single streamline and demonstrate several mathematical characteristics that it has.  
# 
# #### The source tractogram
# 
# In this chapter we take a look at a whole brain tractoram.  And note its characteristics as an amalgum of component streamlines.  Our chief takeaway is that we'll need a systematic method to divide up the tractogram in order to extract any insights from it.
# 
# ### Segmenting tractography
# 
# #### A first segmentation
# 
# In this chapter we introduce the notion of a tractoram segmentation.  We'll use a parcellation to determine what areas streamlines connect an assign them to tracts accordingly. We'll note that this is a viable way to divide up a tractogarm, but observe that there may be methods that pull out more anatomically coherent structures
# 
# #### A categorical segmentation
# 
# In this chapter we examine another approach to tractogram segmentation.  This time we use larger amalgums of areas than the previous chapter to form regions like the frontal, parietal, occipital, and temporal lobes.  We'll note that anatomically coherent strucutres begin to emerge from this approach, and consider how this could serve as a first step towards the segmentation of anatomically coherent white matter structures.
# 

# In[ ]:




