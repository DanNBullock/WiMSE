# A second segmentation - categorical segmentation

In the previous chapter we introduced the fundamental operation of digital white matter segmentation:  the application of an inclusion (or exclusion) ROI.  Indeed, at their heart, all segmentations (insofar as they constitute segmentations) are composed of some finite number of applications of these operations.  We began with the hopefully intuitive case of a planar ROI, which was used to (in essence) assess the traversal of streamlines across a certain coordinate threshold.  After also demonstrating applications of _modified_ planar ROIs (i.e. partial planar ROIs), we then demonstrated the use of ROI intersection using a sphere.  These are both quite common uses of ROIs for white matter segmentation, however they are by no means _exhaustive_ of the tools available to segmenters.  Indeed, in keeping with the recurrent theme of repurposing existing tools and resources, one of our most powerful abilities turns out to be using anatomical parcellations (from structural data, e.g. [Freesurfer](https://surfer.nmr.mgh.harvard.edu/) to perform white matter segmentation.  In fact, our first consideration of a segmentation, was technically an "anatomically based segmentation" in that the parcellation we used to generate the connectome/segmentation was composed of anatomical labels.  Let's consider the conceptual underpinnings of anatomical segmentations a bit more before we perform our second segmentation.

## Using grey matter parcellations with white matter tractograms

One thing that we should note about anatomically-based segmentations from the outset centers on the notion of **biological plausibility**, which was discussed broadly in a previous chapter.  Specifically, we should think back to what most existing anatomical parcellations are:  grey matter segmentations.  This means that the areas that are being labeled are typically where neuronal cell bodies (and not mid to long-range myelinated axons) are located.  As such, if we take our tractome at face value, and assume that it is a _valid, accurate, and biologically plausible_ model of white matter anatomy and trajectory, we won't typically find streamlines traversing these labeled volumes unless they also terminate there.  Streamlines are therefore expected to course through anatomical volumes corresponding to white matter before they ultimately land in an area corresponding to a grey matter label.  Recent tractography generation methods, like [mrtrix 3's "Anatomically-Constrained Tractography (ACT)"](https://mrtrix.readthedocs.io/en/latest/quantitative_structural_connectivity/act.html) ([Tournier et al., 2019](https://doi.org/10.1016/j.neuroimage.2019.116137)), build this into their tractography generation models, in order to generate higher quality tractomes in the first place.  Previously (i.e. mrtrix 2) and/or with other tractography generation algorithms, this criteria was not implemented, and so streamlines could terminate in or traverse through biologically implausible areas.  Thus, the assessment of streamline termination areas can provide useful information about the anatomical characteristics of streamlines and the white matter components they putatively model.

To reiterate, the possibility of using streamline termination areas to label streamlines should seem familiar to you--this was the method we used in the "A first segmentation" chapter.   There, we used a [dipy connectome generation method](https://dipy.org/documentation/1.0.0./examples_built/streamline_tools/) which is algorithmically predicated upon the labeling (or, alternatively, segmenting/categorizing) of streamlines based upon their trminal nodes.  In fact, the failure to generate a connectome using terminations, and to instead consider instances of traversal as an edge measure, could theoretically result in more connections than your tractome has streamlines (and can thus also serve as a good sanity check) as well as potentially implausible connectivity profiles.  Explicitly put:  a streamline's traversal arbitrarily close to a particular label (which may or may not, itself, occupy a biologically implausible volume of the relevant atlas) _is not_ sufficient evidence for connectivity.  More generally though, it's worth noting that connectome generation methods are, generally speaking, _necessarily_ agnostic to the atlases/parcellations that they are applied to.  In order to be maximally useful to network investigators, their algorithms typically reflect a minimal number of assumptions such that they simply iterate over labels and note which streamlines terminate "in" (i.e. "sufficiently near") which areas.  This is not at all an inherently bad feature of connectome generation methods, but rather this is to point out that the resulting categories / connective structures may not always correspond to intuitive or interpretable types.  However, if we leverage our anatomical knowledge _before_ applying a parcellation-agnostic white matter segmentation of this sort, we can generate a segmentation that:

-  1.  Results in intuitive streamline categories
-  2.  Is, in essence, generalizable beyond the specific input grey matter parcellation used to generate it (in that any number of grey matter parcellations could be used to produce this segmentation)
-  3.  Proves to be _immensely_ useful when segmenting more specific white matter anatomy structures.

How can we achieve this?  By performing a gross anatomical category segmentation of the white matter.

## A gross-anatomy categorical segmentation of white matter

The term [gross anatomy](https://en.wikipedia.org/wiki/Gross_anatomy) corresponds to the study of anatomical features which are macroscopically evident.  In the case of performing a categorical, gross anatomical segmentation of white matter this means dividing up the white matter in accordance with its connectivity between gross anatomical brain structures.

Typically, parcellations and atlases of the cortex (and subcortex) divide regions up into established and well studied areas (e.g. [Brodmann's areas](https://en.wikipedia.org/wiki/Brodmann_area)).  However, we needn't rely on such fine grained parcellations of the brain in order to begin the process of dividing up white matter structures into useful subcomponents.  Instead, we can simply consider more general structures like the frontal, parietal, occipital, and temporal lobes, along with other higher order structure groupings (e.g. the thalamus, midbrain, etc.).

Let's begin the process of implementing this segmentation by assigning the regions of the ["Destrieux" 2009 atlas](https://dx.doi.org/10.1016%2Fj.neuroimage.2010.06.010) to these gross anatomical categories.  Luckily, this work has been done previously for a [brainlife app](https://doi.org/10.25663/brainlife.app.249) / [wma_tools product](https://github.com/DanNBullock/wma_tools/blob/master/Segmentations/bsc_streamlineCategoryPriors_v7.m).  First we'll (exhaustively, in that we'll do it for all labels) establish the meaningful label categories we are interested in (e.g. as found specifically [here](https://github.com/DanNBullock/WiMSE/blob/master/exampleData/GrossAnatomyLookup.csv)).  Then we will relabel the atlas in accordance with these groupings, in much the same way we renumbered atlas labels in the chapter "How to interpret a volumetric brain segmentation".

#debatable:
#Planum temporale
#fusiform gyrus
#oc-temp_med_and_Lingual

#this code ensures that we can navigate the WiMSE repo across multiple systems
import subprocess
import os
import pandas as pd
#get top directory path of the current git repository, under the presumption that 
#the notebook was launched from within the repo directory
gitRepoPath=subprocess.check_output(['git', 'rev-parse', '--show-toplevel']).decode('ascii').strip()

#move to the top of the directory
os.chdir(gitRepoPath)

import nibabel as nib
import numpy as np

grossAnatomyPath=os.path.join(gitRepoPath,'exampleData','GrossAnatomyLookup.csv')

grossAnatTable=pd.read_csv(grossAnatomyPath)

grossAnatTable.head(20)

#load the atlas
atlasPath=os.path.join(gitRepoPath,'exampleData','parc.nii.gz')
#load it as an object
atlasImg = nib.load(atlasPath)

#get and copy the data
relabeledAtlas=atlasImg.get_fdata().copy()

#get the labels to iterate over
uniqueAtlasEntries=np.unique(atlasImg.get_fdata()).astype(int)

#merge gross anat with hemisphere info
grossAnatTable['full_grossNames'] = grossAnatTable['Hemi'].str.cat(grossAnatTable['GrossAnat'],sep="_")

#get the unique gross anat + hemi names
grossAnatList=grossAnatTable['full_grossNames'].unique()

#iterate across unique label entries
for iLabels in range(len(uniqueAtlasEntries)):
    #print(np.isin(grossAnatTable['GrossAnat'].loc[grossAnatTable['#No.']==uniqueAtlasEntries[iLabels]],grossAnatList))
    #replace the current uniqueAtlasEntries value with the label corresponding to the gross anat category
    currentLabelReNum=np.where(np.isin(grossAnatList,grossAnatTable['full_grossNames'].loc[grossAnatTable['#No.']==uniqueAtlasEntries[iLabels]]))
    relabeledAtlas[relabeledAtlas==uniqueAtlasEntries[iLabels]]=currentLabelReNum[0]

grossAnatNifti=nib.Nifti1Image(relabeledAtlas, atlasImg.affine, atlasImg.header)  

### A quick look at the gross anatomy atlas

Now that we have relabeled the atlas, let's take a quick look at it using a NiFTI viewing widget.

Overall the gross anatomical relabeling seems suitable.  Due to the coarseness of the DK2009 parcellation in some cases it is difficult to place a label cleanly in a particular lobe (this is noticeably true for temporo-parietal and temporo-occipital labels). Other parcellations can be used to generate this same general sort of result, and may ultimately result in better lobe masks.

After viewing the gross anatomy parcellation, we'll move on to performing the white matter segmentation and then viewing the outputs.

from niwidgets import NiftiWidget
#plot it
atlas_widget = NiftiWidget(grossAnatNifti)
atlas_widget.nifti_plotter(colormap='nipy_spectral')

# load the tractography file into the streamsObjIN variable
smallTractogramPath=os.path.join(gitRepoPath,'exampleData','smallTractogram.tck')
streamsObjIN=nib.streamlines.load(smallTractogramPath)

from dipy.tracking import utils
#segment tractome into connectivity matrix from parcellation
M, grouping=utils.connectivity_matrix(streamsObjIN.tractogram.streamlines, grossAnatNifti.affine, \
                        label_volume=grossAnatNifti.get_fdata().astype(int), 
                        return_mapping=True,
                        mapping_as_streamlines=False)

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
    sw.plot(display_fraction=1, width=1000, height=1000, style=style, percentile=0)

def plotTract(tractIn):
    import numpy as np
    from dipy.viz import window, actor
    renderer = window.Scene()
    stream_actor = actor.line(tractIn)
    #renderer.set_camera(position=(-176.42, 118.52, 128.20),
    #               focal_point=(113.30, 128.31, 76.56),
    #                view_up=(0.18, 0.00, 0.98))
    %matplotlib inline
    renderer.add(stream_actor)
    
    window.show(renderer, size=(600, 600), reset_camera=True)

def updateFunction(regionIndex1,regionIndex2):
    currentRenumberIndex1=regionIndex1    
    currentRenumberIndex2=regionIndex2   
 
    
    #check to make sure this pairing is actually in the connections
    if np.logical_or((currentRenumberIndex1,currentRenumberIndex2) in grouping.keys(),(currentRenumberIndex1,currentRenumberIndex2) in grouping.keys()): 
        #if they are both there do it (dipy method may preclude this)
        if np.logical_and((currentRenumberIndex1,currentRenumberIndex2) in grouping.keys(),(currentRenumberIndex1,currentRenumberIndex2) in grouping.keys()): 
            currentIndexes=np.concatenate((np.asarray(grouping[currentRenumberIndex1,currentRenumberIndex2]),np.asarray(grouping[currentRenumberIndex2,currentRenumberIndex1]))).astype(int)
        elif (currentRenumberIndex1,currentRenumberIndex2) in grouping.keys():
            currentIndexes=grouping[currentRenumberIndex1,currentRenumberIndex2]
        elif (currentRenumberIndex2,currentRenumberIndex1) in grouping.keys():
            currentIndexes=grouping[currentRenumberIndex2,currentRenumberIndex1]
        #there are no other potential cases
        subTractogram=extractSubTractogram(sourceTractogram,currentIndexes)
        %matplotlib inline
        plotParcellationConnectionWidget(subTractogram.streamlines)
    else:
        print('connection not present')

dropDownList=list(zip(grossAnatList, range(len(grossAnatList))))

from ipywidgets import interact, interactive, fixed, interact_manual
from ipywidgets import Dropdown

#establish interactivity
interact(updateFunction, 
         regionIndex1=Dropdown(options=dropDownList, value=19, description="region1"), 
         regionIndex2=Dropdown(options=dropDownList, value=24, description="region2"),
        )

## What's a categorical segmentation good for?

Now that we have generated a gross-anatomy categorical segmentation you may find yourself asking "Why did we do this?" or "What can this be used for?".  As it turns out there are a number of potential applications for a gross-anatomy categorical segmentation like this.  We'll start with some of the more general uses first


### Biological plausibility check

Thinking back to our earlier conceptual discussion of segmentations, this constitutes a "complete" segmentation.  This is because each streamline is **necessarily** assigned a category.  As such this allows us to obtain a broad overview of the characteristics of the input tractome and the streamlines that constitute it.  For example, if one were concerned with the general biological plausibility of their tractome, this segmentation (and visualization) can be used to look at streamlines that terminate in biologically implausible areas (i.e. ventricles, white matter, and "unknown").  As such, the larger the proportion of streamlines that fall into these categories, the more one should be concerned about the quality of the tractography.  The relative number of streamlines in particular categories can also be useful for assessing the input tractome in other ways as well.

### Candidate viability check

Perhaps one of the key insights that this guide endeavors to impart upon users is that **even the best segmentation algorithm can't find what isn't there**.  If the input tractome doesn't contain amongst its many candidate features (e.g. streamlines) some semblance of the structure of interest, then no amount of clever criteria application will be able to extract it.  But what's a quick way to check if the source of your problem is the tractome or the segmentation?  By looking at a categorical segmentation and the general category that the structure would be associated with, it's possible to get a good sense of whether there arent even streamlines there to be segmented, or if your specific segmentation implementation is missing it.  As an example of how to perform this check, consider the case in which either you or a downstream segmentation consumer notices that the [inferior fronto-occipital fasciculus (IFOF)](https://en.wikipedia.org/wiki/Occipitofrontal_fasciculus) derived from a segmentation looks particularly small or impoverished.  To determine whether the issue is the tractography or the segmentation, all one needs to do is look at the "occipital to frontal" (or vice versa) category and see whether there are long range streamlines running along the inferior of the tractome.  If they are there, but not in the segmented IFOF, this suggests that the segmentation is at fault.  If they are not visible in the general category, or if there are very few of them, this suggests that the tractography is at fault.  Below you will find a non-exhaustive table of some major white matter structures and the categories they are associated with:

(taken from the [brainlife.io](https://brainlife.io/docs/) [categorical segmentation app](https://doi.org/10.25663/brainlife.app.249) [readme](https://github.com/brainlife/app-streamlineCategorySegmentation/edit/2.0/README.md))

| **Tract Name** | **Corresponding Category** |
| --- | --- |
| Arcuate | Fronto-temporal |
| VOF (vertical occipital fasciculus) | Occipital-occipital |
| TP-SPL (temporo parietal connection) | Temporal-parietal |
| MdLF (middle longitudinal fasciculus)   | Temporo-parietal |
| Aslant | Frontal-frontal |
| CST (cortico spinal tract) | Spinal-frontal |
| SLF (superior longitudinal fasciculus) | Frontal-parietal |
| ILF (inferior longitudinal fasciculus) | Occipital-temporal |
| IFOF (inferior fronto-occipital fasciculus) | Frontal-occipital |
| pArc (posterior arcuate) | Temporal-parietal |
| Uncinate | Frontal-temporal | 

The ability to associate these general categories with major structures hints at another use.

### Quick first step for segmentations

In cases where you are attempting to segment a relatively large tractome (i.e. more than 250,000 streamlines) and your segmentation tools include the relevant algorithmic speed-ups (as is the case with [wma_tools](https://github.com/DanNBullock/wma_tools) and [wma_pyTools](https://github.com/DanNBullock/wma_pyTools/blob/c562c634afab571f1716960957e580593a8136ff/WMA_pyFuncs.py)), the earlier in the sementation algorithm for a given structure that you drastically reduce the number of streamlines you are considering, the faster your segmentation will process.  This is due to the number of distance computations that need to be performed by ROI criteria applications (as discussed in previous ROI chapters).  As such, applying a category criteria is relatively generous (in that it doesn't really impose that stringent of a criteria) and efficient method for reducing the number of streamlines you are considering.  Although specifying termination regions up front may seem objectionable to some, its worth noting that (1) we aren't imposing particularly specific requirements of the streamlines given how general the gross anatomical areas are (2) in keeping with the table above (and the fact that we have to take streamlines _at face value_ and not modify or embellish) established tracts are _definitionally required_ to terminate in certain regions.

## Next steps using anatomy information

Having considered some initial ways to use anatomical information by applying a gross-anatomy categorical segmentation, we can now move on to thinking about more advanced and finer-grained applications using anatomical information in white matter segmentation.