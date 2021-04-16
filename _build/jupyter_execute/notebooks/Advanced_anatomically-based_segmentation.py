# Advanced anatomically-based segmentation

Now that we have established how to use ROIs and anatomical information _independently_ of one another, it's time to leverage these capabilities in conjunction with one another.  To begin, we'll start by reflecting on our ability to extract labeled volumes of a parcellation as an ROI.

## The first step: extracting a given ROI

Below, we'll demonstrate essentially the same widget and capability as we observed in the "ROIs_as_tools" chapter.  This will allow you to familiarize yourself with the various anatomical labels featured in the [DK2009 atlas](https://doi.org/10.1016/j.neuroimage.2010.06.010) and their locations in the example brain.

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
import numpy as np

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

#establish path to t1
t1Path=os.path.join(gitRepoPath,'exampleData','t1.nii.gz')   

#import the data
t1img = nib.load(t1Path)
#done to establish bounds of image in acpc space
fullMask = nib.nifti1.Nifti1Image(np.ones(t1img.get_fdata().shape), t1img.affine, t1img.header)
#pass full mask to boundary function
t1DimBounds=WMA_pyFuncs.returnMaskBoundingBoxVoxelIndexes(fullMask)
#convert the coords to subject space in order set max min values for interactive visualization
convertedBoundCoords=nib.affines.apply_affine(t1img.affine,t1DimBounds)

#load up the tractogram ahead of time
smallTractogramPath=os.path.join(gitRepoPath,'exampleData','smallTractogram.tck')
streamsObjIN=nib.streamlines.load(smallTractogramPath)

#get tractogram from the Tck holder
sourceTractogram=streamsObjIN.tractogram

def rotateAndPlotWrapper(roiNum,xCoord,yCoord,zCoord):
    from nilearn import plotting
    import nibabel as nib
    import numpy as np
    
    anatomicalROI=WMA_pyFuncs.multiROIrequestToMask(atlasImg,roiNum)
    
    %matplotlib inline
    plotting.plot_roi(roi_img=WMA_pyFuncs.alignROItoReference(anatomicalROI,t1img), bg_img=t1img, cut_coords=[xCoord,yCoord,zCoord])
    
from ipywidgets import Dropdown
from ipywidgets import interact, interactive, fixed, interact_manual
from ipywidgets import IntSlider

interact(rotateAndPlotWrapper, \
    roiNum=Dropdown(options=dropDownList, value=2, description="anatomicalLabel"), \
    xCoord=IntSlider(min=np.min(convertedBoundCoords[:,0].astype(int)), max=np.max(convertedBoundCoords[:,0].astype(int)), step=1,continuous_update=False),  \
    yCoord=IntSlider(min=np.min(convertedBoundCoords[:,1].astype(int)), max=np.max(convertedBoundCoords[:,1].astype(int)), step=1,continuous_update=False), \
    zCoord=IntSlider(min=np.min(convertedBoundCoords[:,2].astype(int)), max=np.max(convertedBoundCoords[:,2].astype(int)), step=1,continuous_update=False))

## Translation errors

In previous chapters you may have noticed that we often selected locations for our ROIs (in particular planar ROIs) by referring to nearby, reference anatomical structures.  Despite this, even though we were choosing where to planar the planar ROIs in relation to these structures, we were nonetheless manually entering coordinates (based on trial and error or our best guesses).  This is less than ideal for several reasons.

First of all, it is difficult to communicate and have intuitions about these coordinates.  In the previous examples we were using ACPC coordinates which specify the millimeter offset from the [anterior commisure](https://en.wikipedia.org/wiki/Anterior_commissure).  This  is nice because it is subject specific and the units themselves are quite familiar.  Alternatively, in some of the literature, [MNI coordinates](https://neuroimage.usc.edu/brainstorm/CoordinateSystems#MNI_coordinates) are used, which has the benefit of being standardized, but necessarily incurs an additional source of spatial error (due to the requisite translations to or from this spatial standard) on top of all the many other sources of error in this field.  This hints at a second trouble as well.

If we're going to leave other investigators to their own devices on how to implement an interpretation of the relative anatomical description of a tract, then we have compounded the number of opportunities for "noise" to be added to our segmentation specification.  In doing so we make our segmentation less reliable overall.  But what if we didn't have to do this?  What if, instead, we were able to _directly_ use those anatomical structures to define our regions of interest?  How could we do that?

Lets try that.  Below, you'll be able to select a anatomical structure **and** which of its borders to use to generate a planar ROI.  Of particular note should be the potential utility of subcortical structures in providing planar ROIs for our future white matter segmentations.

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
import numpy as np

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
portionList=list(['posterior','anterior','caudal','rostral', 'medial','lateral','left', 'right','inferior','superior'])

#establish path to t1
t1Path=os.path.join(gitRepoPath,'exampleData','t1.nii.gz')   

#import the data
t1img = nib.load(t1Path)
#done to establish bounds of image in acpc space
fullMask = nib.nifti1.Nifti1Image(np.ones(t1img.get_fdata().shape), t1img.affine, t1img.header)
#pass full mask to boundary function
t1DimBounds=WMA_pyFuncs.returnMaskBoundingBoxVoxelIndexes(fullMask)
#convert the coords to subject space in order set max min values for interactive visualization
convertedBoundCoords=nib.affines.apply_affine(t1img.affine,t1DimBounds)


def anatomyPlanePlotWrapper(roiNum,relativeBorder,xCoord,yCoord,zCoord):
    from nilearn import plotting
    import nibabel as nib
    import numpy as np
    
    anatomicalROI=WMA_pyFuncs.multiROIrequestToMask(atlasImg,roiNum)
    
    borderPlane=WMA_pyFuncs.planeAtMaskBorder(anatomicalROI,relativeBorder)
    
    %matplotlib inline
    plotting.plot_roi(roi_img=borderPlane, bg_img=t1img, cut_coords=[xCoord,yCoord,zCoord])
    
from ipywidgets import Dropdown
from ipywidgets import interact, interactive, fixed, interact_manual
from ipywidgets import IntSlider

interact(anatomyPlanePlotWrapper, \
    roiNum=Dropdown(options=dropDownList, value=10, description="anatomicalLabel"), \
    relativeBorder=Dropdown(options=portionList, value='superior', description="labelBound"), \
    xCoord=IntSlider(min=np.min(convertedBoundCoords[:,0].astype(int)), max=np.max(convertedBoundCoords[:,0].astype(int)), step=1,continuous_update=False), \
    yCoord=IntSlider(min=np.min(convertedBoundCoords[:,1].astype(int)), max=np.max(convertedBoundCoords[:,1].astype(int)), step=1,continuous_update=False), \
    zCoord=IntSlider(min=np.min(convertedBoundCoords[:,2].astype(int)), max=np.max(convertedBoundCoords[:,2].astype(int)), step=1,continuous_update=False))

## But wait, there's more!

At this point we _could_ demonstrate the use of these full planar, anatomically defined ROIs to apply a single segmentation criteria (e.g. "intersect" or "not intersect" with the plane).  However, in practice, the segmentations resulting from the application of a single, anatomically defined, full planar ROI are not qualitatively different from previous applications of comparable, manually placed ROIs.  While previously, we were manually specifying where to place the planar ROI using (via selection of an ACPC coordinate), by using anatomically defined ROIs, were specifying a coordinate _implicitly_ by selecting a given border of an anatomical region (i.e. superior, lateral, anterior, etc.).  The true practical utility (and complexity) comes from modifying anatomically defined ROIs _using other anatomically defined ROIs_ (as we shall see next) and using multiple such ROIs to compose a segmentation algorithm for a full tract (as we shall see in the next chapter).

As a warning, the interface may get a bit complicated here, but this is to be expected for advanced, anatomically-based segmentations.  After defining your modified planar ROI, we'll use it as a segmentation criterion.

portionList=list(['posterior','anterior','caudal','rostral', 'medial','lateral','left', 'right','inferior','superior'])

def anatomyPlanePlotWrapper(primaryRoiNum,relativeBorder,cutRoiNum,cutBorder,keepPortion, xCoord,yCoord,zCoord):
    from nilearn import plotting
    import nibabel as nib
    import numpy as np
    

    borderPlane=WMA_pyFuncs.planarROIFromAtlasLabelBorder(atlasImg,primaryRoiNum, relativeBorder)
    
    cutPlane=WMA_pyFuncs.planarROIFromAtlasLabelBorder(atlasImg,cutRoiNum, cutBorder)
    
    outPlane=WMA_pyFuncs.sliceROIwithPlane(borderPlane,cutPlane,keepPortion)
    
    %matplotlib inline
    plotting.plot_roi(roi_img=outPlane, bg_img=t1img, cut_coords=[xCoord,yCoord,zCoord])
    
from ipywidgets import Dropdown
from ipywidgets import interact, interactive, fixed, interact_manual
from ipywidgets import IntSlider

primaryRoiNum=Dropdown(options=dropDownList, value=10, description="primaryStruc")
relativeBorder=Dropdown(options=portionList, value=portionList[9], description="brimaryStrucBorder")
cutRoiNum=Dropdown(options=dropDownList, value=255, description="cutRefStruc")
cutBorder=Dropdown(options=portionList, value=portionList[1], description="cutRefStrucBorder")
keepPortion=Dropdown(options=portionList, value=portionList[1], description="portion2keep")

interact(anatomyPlanePlotWrapper, \
    primaryRoiNum=primaryRoiNum, \
    relativeBorder=relativeBorder, \
    cutRoiNum = cutRoiNum, \
    cutBorder= cutBorder, \
    keepPortion=keepPortion, \
    xCoord=IntSlider(min=np.min(convertedBoundCoords[:,0].astype(int)), max=np.max(convertedBoundCoords[:,0].astype(int)), step=1,continuous_update=False), \
    yCoord=IntSlider(min=np.min(convertedBoundCoords[:,1].astype(int)), max=np.max(convertedBoundCoords[:,1].astype(int)), step=1,continuous_update=False), \
    zCoord=IntSlider(min=np.min(convertedBoundCoords[:,2].astype(int)), max=np.max(convertedBoundCoords[:,2].astype(int)), step=1,continuous_update=False))

#Segmentation application:  Segments the tractogram using the previously generated ROI

#create initial border plane
borderPlane=WMA_pyFuncs.planarROIFromAtlasLabelBorder(atlasImg,primaryRoiNum.value, relativeBorder.value)
#create cut plane
cutPlane=WMA_pyFuncs.planarROIFromAtlasLabelBorder(atlasImg,cutRoiNum.value, cutBorder.value)
#cut the intitial border plane with the cut plane
outPlane=WMA_pyFuncs.sliceROIwithPlane(borderPlane,cutPlane,keepPortion.value)
 
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
streamBool=WMA_pyFuncs.applyNiftiCriteriaToTract(sourceTractogram.streamlines, outPlane, True , 'any')
    
streamsToPlot=extractSubTractogram(sourceTractogram,np.where(streamBool)[0])
    
plotSegmentedStreamsWidget(streamsToPlot.streamlines)

## Using other anatomical features of tracts

In the above sections (and indeed in previous chapters) we have been making extensive use of planar ROIs in our segmentation demonstrations.  Additionally, in the chapter covering categorical segmentations, we demonstrated the ability to use endpoint termination areas (implicitly, via [DIPY's connectome generation method](https://dipy.org/documentation/1.0.0./examples_built/streamline_tools/)).  While these are both commonly used methods for segmenting tracts, there are other anatomical features of tracts that can be leveraged.

### Loose endpoint criteria

While it is possible to segment streamlines by applying a criteria specifying which labels their endpoints are required to terminate in, it's also possible to apply less stringent criteria to the endpoints.  For example, it's possible to require that **both** endpoints be anterior to a particular anatomical feature.  Such a criterion would be useful for segmenting the [Uncinate Fasciculus](https://en.wikipedia.org/wiki/Uncinate_fasciculus).  Alternatively you could require that only one endpoint (or, indeed neither) be found positioned relative to some other anatomical structure.

This method is different from the application of a planar ROI because it does not rely on intersection to select streamlines.  All that it does is check to determine which of the endpoints meet the dimensional/anatomical criteria.  This method has the added benefit of having a **much** smaller computational footprint, as no extensive pointwise euclidean distance computations are calculated.

Below we'll use the same ROI as was created earlier. However, for this application, we will skip the cutting step and the primary anatomical border will be treated as a full planar ROI.

#seg via endpoint

#Segmentation application:  Segments the tractogram using the previously generated ROI

#create initial border plane
borderPlane=WMA_pyFuncs.planarROIFromAtlasLabelBorder(atlasImg,primaryRoiNum.value, relativeBorder.value)

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

#establish instruction list
instructionList=list(['one','both','neither'])  

#subset anatomical baoundaries to relevant options
boundsTable= WMA_pyFuncs.findMaxMinPlaneBound(borderPlane)
optionsHold=boundsTable['boundLabel'].loc[boundsTable['dimIndex']==boundsTable['dimIndex'].iloc[0]].tolist()
positionOptions=optionsHold[1:len(optionsHold)]

import numpy as np
import matplotlib.pyplot as plt  
def updateFunc (anatomyOption,endpointInstruction):
    #import widget
    from niwidgets import StreamlineWidget
    #set widget object
    #use the criteria application function to find the relevant streamlines

    print(boundsTable.loc[0])
    
    streamBool=WMA_pyFuncs.applyEndpointCriteria(sourceTractogram.streamlines, borderPlane,anatomyOption , endpointInstruction)
    
    streamsToPlot=extractSubTractogram(sourceTractogram,np.where(streamBool)[0])
    
    plotSegmentedStreamsWidget(streamsToPlot.streamlines)
    
interact(updateFunc, \
    anatomyOption=Dropdown(options=positionOptions, description="keepPortion"), \
    endpointInstruction=Dropdown(options=instructionList, value='both',description="whichEndpoints"))

### Midpoints and "necks"

In addition to utilizing endpoints as a criteria, we can also use the midpoints of tracts.  Traditionally, white matter tracts are understood to possess a "neck" which, as the idiom implies, is the point at which the cross-sectional area (considered perpendicular to the direction that the composite axons are traversing) reaches its minimum--a constriction point.  This anatomical feature is often described in both tractography and dissection-based characterizations of white matter tracts.  Although this feature isn't always found at the "midpoint" of the tract (i.e. the average middle node between streamline endpoints), it is typically _near_ the average midpoint of the tract.  As such, we can reasonably use this as a proxy for the neck, and subject this characteristic to criteria assessments in order to segment streamlines.

Below, we'll once more use the same planar ROI that was established earlier, but this time we'll consider the relative position requirement as applied to the midpoint.

#seg via endpoint

#Segmentation application:  Segments the tractogram using the previously generated ROI

#create initial border plane
borderPlane=WMA_pyFuncs.planarROIFromAtlasLabelBorder(atlasImg,primaryRoiNum.value, relativeBorder.value)

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


#subset anatomical baoundaries to relevant options
boundsTable= WMA_pyFuncs.findMaxMinPlaneBound(borderPlane)
optionsHold=boundsTable['boundLabel'].loc[boundsTable['dimIndex']==boundsTable['dimIndex'].iloc[0]].tolist()
positionOptions=optionsHold[1:len(optionsHold)]

import numpy as np
import matplotlib.pyplot as plt  
def updateFunc (anatomyOption):
    #import widget
    from niwidgets import StreamlineWidget
    #set widget object
    #use the criteria application function to find the relevant streamlines

    print(boundsTable.loc[0])
    
    streamBool=WMA_pyFuncs.applyMidpointCriteria(sourceTractogram.streamlines, borderPlane,anatomyOption)
    
    streamsToPlot=extractSubTractogram(sourceTractogram,np.where(streamBool)[0])
    
    plotSegmentedStreamsWidget(streamsToPlot.streamlines)
    
interact(updateFunc, \
    anatomyOption=Dropdown(options=positionOptions, description="keepPortion"))

## Closing discussion

In this chapter we demonstrated how to use the brain's anatomy to guide segmentation.  As we have noted before though, segmenting a coherent white matter structure typically takes the application of several criteria.  In the next two chapters we'll actually perform a segmentation for two such structures. We'll start with the [uncinate fasiciculus](https://en.wikipedia.org/wiki/Uncinate_fasciculus).