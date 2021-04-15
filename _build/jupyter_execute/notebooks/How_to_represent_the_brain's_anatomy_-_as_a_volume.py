# How to represent the brain's anatomy - as a volume

Not unlike the way that the satellite images of the previous chapters were a "picture" of the world, a [T1 image](https://en.wikipedia.org/wiki/Magnetic_resonance_imaging#T1_and_T2) can be thought of as a "picture" of a brain in a similar fashion.  The specifics of [the physics underlying this process](https://en.wikipedia.org/wiki/Physics_of_magnetic_resonance_imaging) are beyond the scope of this lesson book.  For now let us keep the analogy of the 2-D digital image in mind as we move into a consideration of the NIfTI itself.

Let's begin by loading it into memory and considering its data size.  Whereas previously we were working with .jpg and .png files, we will now be working with .nifti files, which are typically stored as .nii.gz, which corresponds to a compressed state.

#this code ensures that we can navigate the WiMSE repo across multiple systems
import subprocess
import os
#get top directory path of the current git repository, under the presumption that 
#the notebook was launched from within the repo directory
gitRepoPath=subprocess.check_output(['git', 'rev-parse', '--show-toplevel']).decode('ascii').strip()

#move to the top of the directory
os.chdir(gitRepoPath)

#set path to T1
t1Path=os.path.join(gitRepoPath,'exampleData','t1.nii.gz')
#obtain file information about the t1 file
T1fileinfo = os.stat(t1Path)

#print out some of the ifo
print('T1 size (in bytes)')
print(T1fileinfo.st_size)

The T1 NIfTI image we just loaded is about 3.6 MB in size, which is roughly close to a high resolution digital image file.  Given what we know about digital image (every pixel has 3 to 4 *integer* values which correspond to its color characteristics), we can get a rough sense about the number data entries contained within a NIfTI, and--by extension--the general amount of "information" (a complex topic we won't go into here) that a NIfTI image contains about volume of space it is represents.

Quite helpfully, the NIfTI data type features a "header" (described in detail [here](https://brainder.org/2012/09/23/the-nifti-file-format/) and [here](https://nifti.nimh.nih.gov/pub/dist/src/niftilib/nifti1.h))which contains a great deal of [metadata](https://en.wikipedia.org/wiki/Metadata) about the associated image data.  Think of it as being analogous to the [Exif](https://en.wikipedia.org/wiki/Exif) data of a typical digital image.

#begin process of loading file as a T1 nifti using nibabel
import nibabel as nib
#import the data
img = nib.load(t1Path)

#extract the header info
T1header = img.header
#print the output
print(T1header)  

That's a lot of information!

For now, we'll only briefly consider a few of these features, but we'll get to each of these as necessary as we proceed through the next set of lessons.

[**dim**](https://nifti.nimh.nih.gov/nifti-1/documentation/nifti1fields/nifti1fields_pages/dim.html/document_view):  This field displays the dimensions of the NIfTI image data object.  The first number (3, in this case) indicates the total number of dimensions occupied by the data.  The next several values (as many as indicated by the first number in this vector) correspond to the span of each of those dimensions.  Thus, in this case the first dimension spans 145 entries, the second spans 174 entries, and the third spans 145 entries.  

[**datatype**](https://nifti.nimh.nih.gov/nifti-1/documentation/nifti1fields/nifti1fields_pages/datatype.html):  This field corresponds to the [*type* of numerical data](https://en.wikipedia.org/wiki/Computer_number_format)  contained within each of the nifti image data object's entries.  Here we see that it is "float32".  This gives us two primary pieces of information: (1) we now know that the numerical entries are *not* integers or whole numbers (and thus they can adopt values *between* 1,2,3, etc.)  and (2) we now know that each of these entries [takes up about 4 bytes](https://en.wikipedia.org/wiki/Single-precision_floating-point_format).  

[**pixdim**](https://nifti.nimh.nih.gov/nifti-1/documentation/nifti1fields/nifti1fields_pages/pixdim.html/document_view):  Ignoring the initial (-1) and last four values in this field (1.8 0. 0. 0.), we see the numbers 1. 1. 1..   These indicate the size of the dimensions of real world space represented by the NIfTI image data object's entries.  In the case of the map from the previous chapter, this would have corresponded roughly to hundreds of square miles (though the exact quantity would be a complex issue, due to [projection issues](https://en.wikipedia.org/wiki/Map_projection)).  In this case, we see that each of these values is 1 millimeter, which means that the data in any entry of the NIfTI represents a 1 by 1 by 1 for a total of 1 cubic millimeter volume of space.  The fifth value (1) isn't particularly relevant to this particular nifti, as our nifti data object is only 3 dimensional.  If we were examining fMRI data, this value would indicate the time-step used for the data. 

Also, it's important to note that all three of the spatial dimension measures examined above are the same.  This need not be the case, and it could be that our voxels are actually representing units of space whose sides are not all equal.  In this case though, we can say that the voxels are "isometric", meaning that all faces are the same size.

[**qform_code**](https://nifti.nimh.nih.gov/nifti-1/documentation/nifti1fields/nifti1fields_pages/qsform.html):  This field specifies the orientation schema that will be detailed in subsequent fields.  In the previous lesson we considered the intersection of the [prime maridian](https://en.wikipedia.org/wiki/IERS_Reference_Meridian) and [equator](https://en.wikipedia.org/wiki/Equator),also known ["Null Island"](https://en.wikipedia.org/wiki/Null_Island), as the "origin" of the major orientation schema we used, and endeavored to overlay these locations when we aligned global satellite images.  But imagine that we instead used some other coordinate system to establish a different origin point.  Alternatively, what if we stopped using degrees as our unit of measure or that we flipped our labeling convention for east and west? In any of these cases, we would need to find a way to indicate what our reference frame was.  This need for specification of orientation system is reflected in the **qform_code** of the NIfTI header.  Here, we have some indicators ("mni" or "talarach", for example) that establish a common reference frame for orienting the image data.  "mni" and "talarach" respectively correspond to the standard Montreal Neurological Institute ([Collins et al., 1995](https://doi.org/10.1002/hbm.460030304)) and Talairach [Talairach and Tournoux, 1988](https://www.semanticscholar.org/paper/Co-Planar-Stereotaxic-Atlas-of-the-Human-Brain%3A-An-Talairach-Tournoux/f2c1ddf5c34a5899c5cbee5b5dc469f39ff9c21e) atlases.  These and other neuroimaging reference frames are well described elsewhere (e.g. [here](https://www.lead-dbs.org/about-the-mni-spaces/) and [here](http://www.fieldtriptoolbox.org/faq/how_are_the_different_head_and_mri_coordinate_systems_defined/).

[**qoffset_x, qoffset_y , qoffset_z**](https://nifti.nimh.nih.gov/nifti-1/documentation/nifti1fields/nifti1fields_pages/qsform.html) (see "METHOD 2"):  These numbers are the transforms necessary to align this image to the reference specified in "qform_code".  Referring back to our previous lessons, you can think of these numbers as the shift needed to align the political map with the geographic map. Now though, we have three dimensions (as opposed to two) and need to align each of them.  Typically our goals when aligning MRI images  are threefold:  (1) that the images share matching scales, (2) that the images exhibit the same orientation (e.g. top -> top, left -> left, etc.), and (3) that the images points share the same "origin".         

We have now looked at some important features of the [NIfTI header](https://nifti.nimh.nih.gov/pub/dist/src/niftilib/nifti1.h).  However, we haven't yet taken a look at the actual data component of a NIfTI, as we did with digital images in previous lessons.  Let's move forward and take a look at this now.

print('Data dimensions')
print('(How many data entries are spanned across each dimension)')
#extract data dimensions and store in DataDimensions variable
dataDimensions=img.shape
print(dataDimensions)

Here we are no longer indexing into the header, but we nonetheless see that the size of the image data is (182,218,182), which is consistent with the information we obtained from the "dim" field of the header.  In theory, the metadata contained should always be consistent with the actual data, but it is possible for these to become inconsistent due to improper file generation or manipulation.

It's also worth noting that the [nibabel](https://nipy.org/nibabel/) [python software package](https://doi.org/10.5281/zenodo.4295521) offers a number of methods for extracting *specific* information from the header.  For example, we can extract the information specific to the spatial dimensions of the image we are looking at.  This capability can be helpful when performing a series of computations or developing your own sets of functions.

print('Voxel dimensions for T1 (in mm)')
#extract dimensions and store in voxelDims variable
voxelDims=img.header.get_zooms()
print(voxelDims)

Here, we obtain a result that matches what we saw by looking at the entire header.  Now though we have stored this specific information in a variable.  Now, by taking the size of an individual voxel and the dimensions of the entire data block we can compute the amount of space that this NIfTI object represents. 

print('How much total space does this representation correspond to?')
print('')
print(f'{dataDimensions[0]*voxelDims[0]} mm by {dataDimensions[1]*voxelDims[1]} mm by {dataDimensions[2]*voxelDims[2]} mm' )

For those more comfortable with imperial measurements, this corresponds to a volume of space that is slightly more than half a foot wide (\~.6 feet), almost three quarters of a foot tall (\~.71 feet), and slightly more than half a foot deep (\~.6 feet).  This information gives us a sense of the gross scale of the data contained within a NIfTI.  But what about the data contained within a specific entry?  What's in a voxel?

Let's actually index into a specific voxel and see what information is stored there.  From the header, we know that it will be a float value, but we don't, as of yet, have a ballpark sense of what this value will be.  We'll just arbitrarily pick a value.

#extract the actual data into the variable data
data = img.get_fdata()
#arbitrarily index into the item the 96 X, 86 Y, 57 Z location and read it out
data[96,86,57]

235.0.  We don't really know what this number means, whether it is a lot or a little, or if it is unusual, but it at least gives us some sense of the kind of numbers this NIfTI object contains.  What about all of the others though?  How can we get a comprehensive and informative sense of those?  Let's take a hint from our digital image lessons and explore this NIfTI data by plotting a histogram of the data values for each voxel.  In a certain sense, we're lucky (relative to the digital image case) because we can plot a sensible histogram for this information, as there aren't 3 distinct color channels to worry about (which would make it difficult to interpret a histogram or set of histograms).  Additionally, we can get a sense of how many total voxels there are, how many are "non-zero" (in that they contain a measure distinct from zero), and what proportion of the total number of voxels this corresponds to. Let's do that now.

import matplotlib.pyplot as plt
import numpy as np
#necessary for plotting
%matplotlib inline
#transform data array for use
unwrappedData=np.ndarray.flatten(data)

print('Total number of voxels')
#compute total number of voxels via straightforward multiplication
voxTotal=dataDimensions[0]*dataDimensions[1]*dataDimensions[2]
print(voxTotal)
print('')

print('Minimum voxel value')
print(np.min(unwrappedData))
print('')

print('Maximum voxel value')
print(np.max(unwrappedData))
print('')

#set value at which to split the data
#Operating under the assumption that negative values are not viable
splitPoint=0

#define two functions for obtaining boolean vectors for numerical comparison
def smallVal(n): 
    return n<=splitPoint
def largeVal(n):
    return n>splitPoint

#apply the function to the unwrapped data
result=map(smallVal,unwrappedData)
#convert the output to a usable format 
smallBool=list(result)

#apply the function to the unwrapped data
result=map(largeVal,unwrappedData)
#convert the output to a usable format 
largeBool=list(result)

print('Number of voxel values less than or equal to zero')
print(sum(smallBool))
print('')

print('Number of voxel values greater than zero')
print(sum(largeBool))
print('')

print('Proportion of entries greater than zero (i.e. containing data)')
print(sum(largeBool)/voxTotal)
print('')

#perform plotting of zero/negative values
plt.subplot(1, 2, 1)
plt.hist(unwrappedData[smallBool], bins=40)
plt.xlabel('Voxel Data')
plt.ylabel('Number of Voxels')
plt.title('Distributon of voxel less than or equal to zero')
fig = plt.gcf()
fig.set_size_inches(18.5, 10.5)

#perform plotting of positive values
plt.subplot(1, 2, 2)
plt.hist(unwrappedData[largeBool], bins=400)
plt.xlabel('Voxel Data')
plt.ylabel('Number of Voxels')
plt.title('Distributon of voxel values greater than zero')

It seems that about a quarter of the voxels contain data that we would consider to be representative of the brain, with the assumption that "empty" voxels correspond to background and/or uninformative voxels.  Depending on whether or not this T1 has had the brain "extracted" (i.e. the brain isolated from the rest of the head, neck, and body, via a masking process, see [Boesen et al. 2004](https://doi.org/10.1016/j.neuroimage.2004.03.010) for more), this proportion may also include non-brain tissues.  Note how we had to split the histogram in two.  Had we not done this, the number of empty voxels would have overwhelmed the visualization and we wouldn't have been able to observe the distribution visible in the plot on the right due to the extreme number of values right below 0.

Now that we have a sense of the numerical variability of the data in this NIfTI, let's get a sense of how these values are laid out spatially.  Keep in mind that, just like a digital image wherein the i,j entry of the data array represents a portion of space that spatially adjacent to the i,j-1 (or i,j+1, or i+1,j etc.), the i,j,k entry of a NIfTI is spatially adjacent to the i,j,k+1 entry.  We can get a better sense of this by interacting with the NIfTI using a [niwidget](https://nipy.org/niwidgets/).

from niwidgets import NiftiWidget

t1Widget = NiftiWidget(t1Path)

t1Widget.nifti_plotter(colormap='gray')

Take a moment to shift through the NIfTI image plotted above.  If you want a more standard visualization, feel free to switch the colormap to gray.  **As a challenge, try and shift the x, y, and z sliders to cross at the [anterior commissure](https://en.wikipedia.org/wiki/Anterior_commissure), and take note of the coordinates of this point**.  Take note that the left, posterior, inferior corner is the 0 coordinate.  The coordinate shift that results in the anterior commissure being at (0,0,0) occurs after the previously qoffset information has been applied.  After this transform has been applied, locations in the left hemisphere are characterized by coordinates that have a negative first value (x coordinate).  This is because the image is oriented with respect to the [ACPC reference space](https://www.fieldtriptoolbox.org/faq/how_are_the_different_head_and_mri_coordinate_systems_defined/#details-on-the-acpc-coordinate-system). 

As an alternative to trying to find the anterior commissure manually, we can also use the information in the header (assuming its accurate) to compute its location in this image data.

print('T1 voxel resolution (in mm)')
print(img.header.get_zooms())
print('')

print('T1 voxel affine')
imgAff=img.affine
print(img.affine)
print('')

print('Coordinates of anterior commissure')
#force absolute value in order to perform the math correctly
imgSpatialTrans=np.abs([imgAff[0,3]/imgAff[0,0],imgAff[1,3]/imgAff[1,1],imgAff[2,3]/imgAff[2,2]])
print(imgSpatialTrans)
print('')

If you move the slider coordinates to the value specified under "Coordinates of anterior commissure", your crosshair should directly target the [anterior commissure](https://en.wikipedia.org/wiki/Anterior_commissure).  However, the signs of the numbers in this affine matrix suggest that something may be afoot.  Let's consider in a bit more detail what these numbers might be indicating.

Admittedly, the notion of a shift or transform gets a bit more complicated in three dimensions, where it is possible to have your data rotated or flipped along multiple dimensions.  With a standard 2-D image this would have been quite obvious upon inspection--you would notice if the world had been rotated 90% or flipped such that Russia was west of the US's "east" coast!  Although some of these changes are obvious in a NIfTI image (for example a 90 degree rotation), some are less obvious.  For example, as it turns out, **this brain data is flipped in its x axis!**. Because of this the right hemisphere data is stored in indexes smaller than the X coordinate of the anterior commissure (90) while the left hemisphere data is stored in indexes that are larger than the X coordinate of the anterior commissure.  This is contrary to standard orientation schemas.  Let's take a look at how we could come to know this by taking a look at the [affine transform matrix].(https://en.wikipedia.org/wiki/Affine_transformation) again.

print('T1 voxel affine')
imgAff=img.affine
print(img.affine)
print('')

You'll notice that the upper left hand value (-1.), which specifies the voxel resolution of the Y dimension, is negative.  This is as opposed to the values found for the Y and Z dimension resolutions, which are positive.  Considered in conjunction with the information in the first three rows for the rightmost column (the **qoffset_** information from the header), this indicates that a flip in the X dimension is present.  This is why the *np.abs* function was used earlier when computing the anterior commissure location (NOTE: this strategy will not work for all affine flip cases, but did work in this case).  For more detailed examinations and considerations of affine transforms for neuroimaging data consider looking at dipy's [documentation on the subject](https://www.dipy.org/documentation/1.0.0./examples_built/affine_registration_3d/).

Now that we have developed a good sense of the information stored in a T1 NIfTI image, move on to think about how tractography data is different from this.