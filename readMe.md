https://mybinder.org/v2/gh/DanNBullock/WiMSE/master

# Chapter Summaries 
 
## Building intuitions with digital images

[Why are we talking about JPEGs](https://github.com/DanNBullock/WiMSE/blob/master/notebooks/2.9999 %20%20Why%20are%20we%20talking%20about%20JPEGs.ipynb) % If this notebook is about the computational study of white matter, why are we taking about image data formats? In this chapter relationships between images, representations, and data objects are introduced. Across various data formats (e.g. digital photographs, T1 images, DWI, & tractography), we'll note analogous traits which will help us build intuitions as we progress through subsequent chapters.

[Intro to discretized image representation & maps](https://github.com/DanNBullock/WiMSE/blob/master/notebooks/3.%20% 20Intro%20to%20discretized%20image%20representation%20%26%20maps.ipynb)
In this chapter we begin our exploration of image data with an example that will likely be familiar to many readers: a digital photograph. We'll begin by looking at the how the data is arranged within the image data object, what its constituent data entries are, and how those features relate to the image we encounter on our screen.  We'll then move to an exploration of how the quantitive features of the image data can be leveraged to select certain sub-sections of the image via a process referred to as "masking"

[Aligning two images](https://github.com/DanNBullock/WiMSE/blob/master/notebooks/3.2% 20%20Aligning%20two%20images.ipynb)
In this chapter we build upon the previous chapter's introduction of masks by interactively attempting to overlay a mask derived from one image onto another image.  We also qualitatively assess how well the two images have been aligned. This will serve as a prelude to using the mask from one image to extract certain sub-sections from another image.

[Multi object maps in images](https://github.com/DanNBullock/WiMSE/blob/master/notebooks/3.5% 20Multi%20object%20maps%20in%20images.ipynb)
In this chapter we leverage our ability to align images to select pixels corresponding to US states from a satellite image of the continental United States.  This capability serves as a direct analogy to our ability to select portions of a NIfTI image via the use of a parcellation, which will be explored in later chapters.

[A consideration of jpegs and brain images](https://github.com/DanNBullock/WiMSE/blob/master/notebooks/3.999 %20A%20consideration%20of%20jpegs%20and%20brain%20images.ipynb)
In this chapter we reflect on our observations about digital images as we begin to transition to working with NIfTI data objects.

## Working with NIfTI data

[How to represent the brain's anatomy - as a volume](https://github.com/DanNBullock/WiMSE/blob/master/notebooks/4.%20 %20How%20to%20represent%20the%20brain's%20anatomy%20-%20as%20a%20volume.ipynb)
In this chapter we shift from a consideration of 2 dimensional, color digital photographs to MRI data stored in a NIfTI.  Although there are a number of conceptual similarities between these data modalities, there are also a number of important distinctions which we consider here.  We also take a look at the affine information contained within the NIfTI header, and reflect on its relevance to aligning 2 dimensional images.

[A quick demonstration of linear affine transformations in 3-D](https://github.com/DanNBullock/WiMSE/blob/master/notebooks/5.1%20%20A%20quick%20demonstration%20of%20linear%20affine%20transformations%20in%203-D.ipynb)
In this chapter we consider very briefly how to implement linear transforms and rotations in 3 dimensions.  Given that there are [other, more detailed resources available](https://nipy.org/nibabel/coordinate_systems.html), this is primarily a hands on demonstration so that users can become familiar with the concept.

## White matter and tractography

[Highways of the brain](https://github.com/DanNBullock/WiMSE/blob/master/notebooks/6.5%20%20Highways%20of%20the%20brain.ipynb)
In this chapter we move on from our consideration of volumetric/NIfTI based neuroimaging data, and 




