# Building bridges from the familiar to the unfamiliar

## But... why JPEGs?

Although the title of this collection of interactive lessons is WiMSE (White Matter Segmentation Education), and presumably you are here to learn about neuroscience, our first several lessons will have us exploring JPEGs rather than brain images.  **Why is that**?

### Building intuitions from the familiar

Although our ultimate goal will be to develop an intuitive understanding of how to conduct digital investigations of white matter anatomy, it will be helpful to begin with an example of a data structure that everyone (at least, denizens of our modern digital era) is familiar with.  This is where JPEGs come in.  [JPEGs (Joint Photographic Experts Group)](https://jpeg.org/jpeg/) are a standardized two dimensional (2D) digital image format that we typically encounter dozens of times a day as we browse the internet.  There are other image formats (PNG, for example), but JPEG is perhaps the most famous for images.  As such, we will begin exploring concepts related to structured data representation (and in particular, *image* representation) using JPEGs.  We will use JPEGs to establish a number of analogies to the primary image type used in neuroimaging research, the [NIfTI (Neuroimaging Informatics Technology Initiative)](https://nifti.nimh.nih.gov/).  Research has shown that analogies and metaphors are particularly helpful when learning new concepts ([Duit, R., 1991](https://psycnet.apa.org/doi/10.1002/sce.3730750606)).  Indeed, in many cases the comparisons we make will be more akin to logical extensions than metaphors.  Regardless, it is **not** expected that individuals using this lesson set are particularly familiar with the NIfTI data format, and so several non-technical features of this data type will be  discussed to help build this understanding.

### A reassurance to the initiated

For more experienced users though, our upcoming discussion of the NIfTI format may seem out of place.   NIfTI data objects aren't used to store connectivity data, which is the essence of white matter (and the key feature that data formats for white matter attempt to capture).  While this is true, it is necessary to discuss NIfTI data structures for two important reasons:  (1)  The difficulties in segmenting white matter structures (in connectivity-centric data formats) are well highlighted by comparison to the process of segmentation volumetric structures (in NIfTI/volumetric-type formats) and (2) A good white matter segmentation method (e.g. White Matter Query Language (WMQL) ([Wassermann et al., 2013](https://doi.org/10.1007/978-3-642-40811-3_81) or [WMA_Tools](https://github.com/DanNBullock/wma_tools)) can make extensive use of information stored in or derived from NIfTI files (for example, [FreeSurfer](https://surfer.nmr.mgh.harvard.edu/) ([Fischl 2012](https://doi.org/10.1016/j.neuroimage.2012.01.021)) parcellations ([Desikan et al. 2006](https://doi.org/10.1016/j.neuroimage.2006.01.021), [Fischl et al,. 2004](https://doi.org/10.1093/cercor/bhg087)).  Thus, our consideration of white matter segmentation will begin with digital images, proceed to NIfTI-type images (in this case T1 images), and then move on to the topics of tractography and segmentation.

## The big picture - A philosophy to segmentation

Below you'll find a table that provides an outline of the overarching analogies between the various data formats that we will encounter in the following lessons.  As we proceed through the chapters we'll repeatedly find ourselves investigating concepts with relatively familiar types of data (even for those who don't do much programming or data processing), and then seeing how those same concepts can be applied to relatively unfamiliar types of data.  At various points we will return to a consideration of this table and reflect on what it is about the current data type/object.  

###  The analogy table

|   | **Digital Photography** | **Structural Brain Imaging (T1)** | **Diffusion Imaging (DWI)** | **Tractography** |
| --- | --- | --- | --- | --- |
| _Data Token_ | digital photo image | structural brain image (T1)| diffusion image (DWI) | tractogram |
| _Object represented_ | visual scene | cranium / brain | cranium / brain | white matter of brain |
| _Source system_ | camera | MRI scanner | MRI scanner | Mathematical model  | 
| _Source phenomena_ | reflected light | water / magnetic properties | water movement | orientation interpolation |
| _Property of interest_ | topography | volumetric occupancy | tissue structure | putative axon collection traversal |
| _File extension_ | .jpg, .png ... | .nifti, nii.gz | (dwi) .nifti, nii.gz | .fg, .trk, .tck |
| _Metadata_ | exif | header | header | varies by format |
| _Data size_ | 100s kb - 1s MB | ~2.5 - 5 MB | 50 MB - 1.5 GB |500 MB - 10 GB |
| _Data dimensionality_ | &quot;2D&quot;(3 RGB layers) | 3D | 4D |1D nested? |
| _Data &quot;atoms&quot;_ | pixels | voxels | voxel-angle | vectors (streamlines) |
| _Data &quot;atom&quot; content_ | integer | float |float | ordered float sequence (nodes) |
|_Implicit features of interest_ |  object differences  |  tissue differences  |  tissue differences   |  gross white matter / informational connectivity |
|_Implicit categories_ |  ordinary, everyday objects  |  brain regions  |  brain regions  |  tracts and information streams |
|_Atom-object correspondence_  |  isometric visual angle unit  |  sub volume of brain  |  sub volume of brain, measured from a specific angle  |  (putative)  axon collection traversal |


### Defining terms in the analogy table

| **Term** | **Rough definition** | **Source or representation characteristic** | 
| --- | --- | --- |
| _Data Token_ | A particular instance of a data type | Representation |
| _Object represented_ | The (real world) thing which the _Data Token_ contains information about | Source |
| _Source system_ | The technological/methodological system used to generate the data contained within a  _Data Token_  | Representation  | 
| _Source phenomena_ | The general kind of quantitative property of the _Source system_ makes measurements of  | Source |
| _Property of interest_ | The more qualitative feature of the _Object represented_ that the _Source system_ is understood to capture (via the _Source phenomena_ proxy | Source |
| _File extension_ | File extensions typically associated  | Representation |
| _Metadata_ | Method for storing information about the manner in which the information was derived | Representation | 
| _Data size_ | Typical size of the associated _Data Token_ | Representation |
| _Data dimensionality_ | The dimensionality of the _Data Token_ | Representation |
| _Data &quot;atoms&quot;_ | The atomistic data components composing the _Data Token_ | Representation |
| _Data &quot;atom&quot; content_ | The specific content/format of the _Data &quot;atoms&quot;_ |  Representation |
|_Implicit features of interest_ | The (implicit) feature of the _Object represented_ that the _Data Token_ is supposed to faithfully capture.  Failure to capture these features would constitute a fundamental failure for the _Data Token_. | Source |
|_Implicit categories_ | Theoretically, the kinds of categorical delineations that could/would be made using effective leveraging of information about the _Implicit features of interest_ | Source |
|_Atom-object correspondence_  | The "real world" entities that the _Data &quot;atoms&quot;_ are supposed to correspond to | Source |

## A demonstration of the strength of the analogy

A good deal of time and effort has been taken to present and characterize the analogy between the various imaging modalities we will consider.  This is because the analogy is taken to be both (1) fundamental and (2) strong.  To demonstrate the strength of this analogy, we'll next make use of what is, in essence, a ["Mad Lib"](https://en.wikipedia.org/wiki/Mad_Libs).  Specifically, because of how well these modalities align with one another, and how carefully the characteristics have been operationalized, it will be shown that it is possible to generate a standard description of all modalities, that has the specifics of each modality populated from the table above.  Despite being "form generated" in this sense, it will nonetheless be found to be both informative and insightful.  

After running the code block below, use the slider to slide between the columns of the analogy table to read a comprehensive characterization of the relevant features of each particular imaging modality.

#this code ensures that we can navigate the WiMSE repo across multiple systems
import subprocess
import os
#get top directory path of the current git repository, under the presumption that 
#the notebook was launched from within the repo directory
gitRepoPath=subprocess.check_output(['git', 'rev-parse', '--show-toplevel']).decode('ascii').strip()

#move to the top of the directory
os.chdir(gitRepoPath)

import pandas as pd

#get the path to the saved csv version of the analogy table
analogyTablePath=os.path.join(gitRepoPath,'exampleData','analogyTable.csv')

analogyTable=pd.read_csv(analogyTablePath, sep='\t',header=None)

analogyTable.loc[:,1]

#establish a bolding and coloring method up front
#taken from https://stackoverflow.com/questions/8924173/how-do-i-print-bold-text-in-python
class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

columnIndex=0
#update the printout     
#def generateAnalogyMadlib(columnIndex):

#create bold-green and double-end text holder variables to make the following lines shorter
BG= color.BOLD + color.PURPLE + color.UNDERLINE
DE= color.END + color.END + color.END

#create function for madlib generation
def generateMadlib(currentColumn):

    #doing it this way to (1) save space later and (2) incase the table changes around later
    #inelegant, but transparent
    #will cause problems if the entries in the first column of the saved analogies table csv is altered
    curModality=BG + analogyTable.loc[analogyTable[0]=='General imaging modality',currentColumn].iloc[0] + DE
    curDToken=BG + analogyTable.loc[analogyTable[0]=='Data token',currentColumn].iloc[0] + DE
    curObjectR=BG + analogyTable.loc[analogyTable[0]=='Object represented',currentColumn].iloc[0] + DE
    curSourceSys=BG + analogyTable.loc[analogyTable[0]=='Source system',currentColumn].iloc[0] + DE
    curSourcePhe=BG + analogyTable.loc[analogyTable[0]=='Source phenomena',currentColumn].iloc[0] + DE
    curPropOfInt=BG + analogyTable.loc[analogyTable[0]=='Property of interest',currentColumn].iloc[0] + DE
    curFileExt=BG + analogyTable.loc[analogyTable[0]=='File extension',currentColumn].iloc[0] + DE
    curMetaDat=BG + analogyTable.loc[analogyTable[0]=='Metadata',currentColumn].iloc[0] + DE
    curDataSz=BG + analogyTable.loc[analogyTable[0]=='Data size',currentColumn].iloc[0] + DE
    curDataDim=BG + analogyTable.loc[analogyTable[0]=='Data dimensionality',currentColumn].iloc[0] + DE
    curDataAtm=BG + analogyTable.loc[analogyTable[0]=='Data atom',currentColumn].iloc[0] + DE
    curDataAtmCont=BG + analogyTable.loc[analogyTable[0]=='Data atom content',currentColumn].iloc[0] + DE
    curImpInt=BG + analogyTable.loc[analogyTable[0]=='Implicit features of interest',currentColumn].iloc[0] + DE
    curImpCat=BG + analogyTable.loc[analogyTable[0]=='Implicit categories',currentColumn].iloc[0] + DE
    curAtmObjCorr=BG + analogyTable.loc[analogyTable[0]=='Atom-object correspondence',currentColumn].iloc[0] + DE

    #need to play with wraparound settings for this
    textToPrint='A fill-in-the-blank description of ' + curModality + ' :\n\n' + \
        'When we engage in research using ' + curModality + ' we are interested in learning more about a particular ' + curObjectR + \
        '.  However, in order to study the given ' + curObjectR + ' effectively, we need to preserve information (i.e. observations) about it for later analysis.' + \
        '  In the case of ' + curModality + ' we typically use a(n) ' + curSourceSys + ' to obtain data about [a] ' +curObjectR +'. It is worth noting though, that our decision to use a '  + curSourceSys + \
        ' is based upon (1) the availability of viable alternatives and (2) the general property of the ' + curObjectR + ' (e.g. ' + curPropOfInt + ')' + \
        ' that we are interested in, or whatever more specific goals we may have.  Indeed, the kinds of scientific questions we can ask about ' + curObjectR + 's ' + \
        ' (or  ' +curImpInt+ ', or even ' + curImpCat + ') using ' + curModality + \
        ' are delimited by the technical limitations of the ' + curSourceSys + 's used,' + \
        ' and so to then, are the general kinds of things that end up getting studied/characterized using '+ curModality + \
        '.  Resulting chicken-or-the-egg conundrums and streetlight effects notwithstanding, the ability to develop insights about '  + curObjectR + 's ' + \
        'using information about ' + curPropOfInt + ' derived from ' + curSourcePhe + ' has, in practice, proven to be useful for identifying ' + curImpInt + \
        ', and (by extension) ' + curImpCat + ', both in specific ' + curObjectR +'s and in ' + curObjectR + 's generally.' + \
        '  Let\'s briefly consider how the data objects used in ' + curModality + ' facilitate this.\n\n' + \
        '  The scientific utility of '  + curModality + ' is underwritten by our ability to store, access, and modify information ' + \
        'contained within the standard data object used in this discipline, the ' + curDToken + '.' + \
        '  In each of these data objects information that was produced by a '+ curSourceSys +' measuring ' + curSourcePhe + ' is stored in a structured fashion.' + \
        '  Specifically, in the case of a '  + curDToken + ', that information is stored in a ' + curDataDim + ' structure ' + \
        'wherein each ' + curDataAtm + ' contains a ' + curDataAtmCont + '.  Each of these ' + curDataAtm + 's stores information about ' + curSourcePhe + \
        ' as measured by the source ' + curSourceSys + ' and, in doing so, represents a(n) ' + curAtmObjCorr + '.' + \
        '  Typically, a ' + curDToken + ' contains a(n) ' + curMetaDat + ' component which stores information about the source ' + curSourceSys + \
        ' or other information relevant to (but not derivable from) the data object itself.  These files/data objects are typically associated with file extensions like ' + \
         curFileExt + ' and are about ' + curDataSz + ' in size, which can give you some sense of ' + \
        'the number of ' + curDataAtmCont + 's the object contains.'
    
    #add brackets for the 0, i.e. label column, case
    if currentColumn==0:
        textToPrint=textToPrint.replace(BG,'['+BG)
        textToPrint=textToPrint.replace(DE,']'+DE)

    print(textToPrint)

from ipywidgets import interact, interactive, fixed, interact_manual
from ipywidgets import IntSlider    

#establish interactivity
interact(generateMadlib, currentColumn=IntSlider(min=0, max=4, step=1,continuous_update=False))

## What to make of the Madlib

What you should take from the above paragraphs is that the move to make use of comparisons between the modalities is well founded and that the specific features that have been associated across the modalities are justifiably related.  This has been done to support the practice of leveraging insights from one of these modalities to help us learn about another modality.

## At the heart of it all

Overall, what this guide is designed to do is to take an individual who is presumed to have little familiarity with white matter or white matter segmentations and bring them to a point where they have mastered the "[meta-ontology](https://en.wikipedia.org/wiki/Meta-ontology)" associated with the practice of white matter segmentation. In essence, "mastery of the meta-ontology" is the state an expert in any given field has achieved when they possess a deep familiarity with the various approaches and frameworks (which may potentially be mutually inconsistent) particular to their field _and_ the systematically structured relations between those approaches.  Achieving this is obviously no easy feat.  The strategy of this lesson set is to reinforce users' intuitions regarding ontological systems _that they are already implicitly experts of_ , and use those as a bridge to understanding a topic that was initially utterly mysterious (i.e. digital white matter segmentation).

We are beginning with digital photographs because the kinds of "implicit features of interest" and "implicit categories" that one encounters in this domain are the things that our brains are hardwired to pickout--we are all natural masters of this ability.  As it was posed above, the digital photography example was roughly related to the field of [machine-vision](https://en.wikipedia.org/wiki/Machine_vision), but at its heart that field (machine-vision) is attempting to replicate the inherent capability of the visual system using the framework provided.  As complex as that field of research is, we are all experts at this process, and not only identify a massive range of objects in the world, but we can also switch between frameworks and approaches for identifying and categorizing them.  Unfortunately, there are no innate human cognitive systems (specific) for segmenting white matter.  Nonetheless, our goal with this guide is to help you, the user, become familiar with the processes, contexts, and discussion of digital white matter segmentation, in much the same way that you are capable of identifying objects in the world.  Rather than rely on your intuitions though, we'll be doing this systematically, and going through the principled approach for doing this. Before embarking on our journey though, we should probably take this opportunity to cash out what is meant by an ontology or meta-ontology.  These concepts will become quite important as we consider some of the more abstract fundamentals of white matter segmentation.

### What's a meta-ontology?  For that matter, what's an ontology?

For our purposes here, we are considering the notion of an ontology in the sense used by [information science](https://en.wikipedia.org/wiki/Ontology_(information_science)).  Fundamental to the process of segmentation (and thus to this guide) is the identification and delineation of differences within members of a larger set.  Repeatedly, we will find that our main curiosity is *how ought we go about systematically assigning particular entities we encounter to (presumably) meaningful and useful categories*.  There can be no answer to this question without the the provision or specification of an *ontology*.  Quite simply: we can't separate objects if we don't know the kinds of categories they can be separated into.

For us, in the following lesson sets, the "provision or specification of an ontology" will entail the (either explicit or implicit) [operationalization](https://en.wikipedia.org/wiki/Operationalization) of certain components that are common to all ontologies in a fashion that is specific to the current ontology.  Those components are outlined in the following table ([adapted from wikipedia](https://en.wikipedia.org/wiki/Ontology_components)):

| **Ontology component** | **Rough definition** | 
| --- | --- |
| _Individuals_ | Those entities which "exist" and are submitted for assignment to "Classes" | 
| _Classes_ | Meaningful/non-arbitrary groupings of _Individuals_ (e.g. labels, categories, etc. |
| _Attributes_ | Properties or characteristics that _Individuals_ or _Classes_ can have | 
| _Relations_ | Those manners or dimensions with which _Individuals_ and _Classes_ can be compared or related | 

This is, admittedly, a very abstract preview of how we will be making use of ontologies throughout our lessons.  Interestingly though, the structured analogy provided in the analogy table _already provides_ specifications for several characteristics.  As it turns out, by decomposing the salient characteristics of the imaging modalities we'll be considering, we appear to have "carved nature at its joints" (to borrow from Plato) and thereby aligned those modalities along their ontologically salient dimensions.

| **Ontology component** | **Rough definition** | **Modality Representation Characteristic** | **Modality Source Characteristic** 
| --- | --- |  --- | --- |
| _Individuals_ | Those entities which "exist" and are submitted for assignment to _Classes_ | _Data &quot;atoms&quot;_  | Atom-object correspondence |
| _Classes_ | The various meaningful/non-arbitrary groupings available for _Individuals_ (e.g. labels, categories, etc.) | **Labeling schemas / segmentations** |_Implicit categories_ |
| _Attributes_ | Properties or characteristics that _Individuals_ or _Classes_ can have | _Data &quot;atom&quot; content_ | [causal properties] |
| _Relations_ | Those manners or dimensions with which _Individuals_ and _Classes_ can be compared or related | [for us to characterize/discover]  |_Implicit features of interest_ |

Thus, any time we apply a segmentation what we'll be doing is systematically providing rules based on _Relations_ using the _Attributes_ (i.e. quantitative characteristics) of the various _Individuals_ in order to determine which _Classes_ the _Individuals_ belong to.  

### A second insight from the analogy framework: the role of representation

The decomposition in the earlier analogy table also offers another interesting insight.  Each data modality we are considering is a way of systematically _representing_ something in the world.  Because the relations of the various aspects of the data modalities is preserved by the structure of the analogy posed, it may also be possible to provide a general account of how each of the relevant characteristics from the analogy table helps to instantiate a representation relation with the associated data object.  This may seem like an abstract concern, but (for reasons that will become apparent throughout this endeavor) it is extremely important to clearly and from the outset nail down what it means for the categories and objects we identify in our data to "represent" things in the world.  Fundamentally, the data objects we will be dealing with are not _actually_ what we are concerned with, but rather we are concerned with the things they represent (hopefully, accurately).

Explicitly, each _Data Token_ is taken to represent a "real thing in the world" (i.e. _Object represented_ ).  That _Data Token_ is generated by the _Source system_ , which systematically measures the _Source phenomena_ , one of several _Attributes_ possessed by the _Object represented_ . The _Data Token_ preserves information related to the _Property of interest_ that can be used to ascribe the desired _Classes_ to the _Individuals_ of the _Data Token_ .  Because the _Data Token_ "preserves the relevant information" (and in doing so, instantiates the representation relation with the "real thing in the world"), the _Classes_ ascribed to the _Data Token_'s _Individuals_ can be back-mapped back on to the _Object represented_.

The above paragraph also just so happens to highlight (quite abstractly) why we care about the various image modalities covered by the analogy table.

##  Why we care about image representations generally... and specifically

Inherent in the account of representation above is the fact that we can computationally leverage digital images (in any of their various forms) to label their individual components in accordance with whatever goals we may have.  Indeed, this is precisely what our brains do in order to help us interact with the world: they carve the world (visual and otherwise experienced) into categories and particular instances of relevant categories so that we can make use of that information to guide our behavior.  However, digital images and the algorithms we apply to them increasingly (as our computational and algorithmic technologies advance) have three distinct advantages:  their formal reliability, their processing speed, and their transparency (at least in the case of non [black box](https://en.wikipedia.org/wiki/Black_box) algorithms).  So long as we can formulate a sensible set of formal rules to apply to the elements of digital images, we can apply those rules with great speed and reliability.  In doing so we can obtain far more nuanced categorizations that we are able to when using our natural sensory capabilities.  But therein lies the rub: "So long as we can formulate a sensible set of formal rules"--how can we do this?  This is the challenge at the heart of our difficulties with image labeling algorithms generally, and our specific goal of performing white matter segmentations.

Because we are using computational approaches, our ability to pose formal rules is fairly decent.  Indeed, there are those who have formalized computational languages _specific_ to white matter segmentation (i.e. [WMQL: White Matter Query Language](https://dx.doi.org/10.1007%2Fs00429-015-1179-4)) to develop the ability to pose formal white matter segmentation rules as robustly as possible.  However, it has yet to be proven that any particular of these approaches is sufficiently versatile to delineate _any specific white matter structure_ we could possibly be interested in.  It could be that there are some structures--known or unknown--that existing methods are simply insufficient for delineating or segmenting.  To use a linguistic analogy, this would be as if a language lacked the formal ability to pose certain [propositions](https://en.wikipedia.org/wiki/Proposition).  Moreover, in the case of white matter, we're probably being further hindered by simply _not knowing_ the full range of structures that a formal white matter language would need to be able to express.   To get at the crux of the matter though, "white matter segmentaton codes/languages" (as a broad category) are merely the provision of a [syntax](https://en.wikipedia.org/wiki/Syntax) for describing white matter, and syntax (a formal system of rules for making well formed expressions) alone isn't enough if our goal is to systematically link our _Data Tokens_ to "objects in the world" and thereby be useful and valid representations.  What they lack is a [semantics](https://en.wikipedia.org/wiki/Semantics) for describing white matter--a systematic method for mapping meaning (and therefore representation) to the various components of our data of interest.  It isn't at all immediately clear how one could go about this, but this lesson set, as a whole, is designed to begin to work towards this.

## A rough attempt at a semantics for digital white matter

Traditionally, one of the greatest challenges for naturalistic accounts of representation of mental content was finding a compelling account of the link between the somewhat ineffable notion of [mental content](https://plato.stanford.edu/entries/content-causal/) and its ostensible relationship with objects in the world.  One of the more prevalent theories offered was that of [teleosemantics](https://plato.stanford.edu/entries/content-teleological/) which endeavored to explain the phenomenon of mental representation in terms of inferred functions or purposes.  This paradigm is subject to various forms of rebuttal due to the limitations of our ability to infer the "true" function of a given entity possessing representational properties.  However, this isn't the case for digital models of white matter.  The "mental content" (that is, the information we are trying to link with objects in the world) that we are dealing with is simply formalized data structures.  Because we (as a field) have developed the imaging devices and the algorithms that transduce the measurements of the world into data objects and derivative models thereof, we don't need to infer the structure of the process which resulted in the "information token" (i.e. representation).  Rather, what we need is a clear, comprehensive, and compelling account of the processes which reliably give rise to valid models of coherent white matter tracts.

Our task with this guide is to provide a robust account of how we can systematically modify and transform the representational elements available to us in tractograms in such a way that we can carve digital models of white matter into what we take to be the meaningful subcomponents of the white matter.  This means identifying, observing, and describing the elementary methods used to compose, describe, and delineate a given white matter structure from amongst the other candidate components (i.e. streamlines) of a tractogram.  To do this we will need to consider _all_ of the information that we can make use of--both explicit and implicit--from our various available data objects, and what steps we can take to select a specific and coherent structure of interest.

## The grand insight

The overarching insight that this guide will instill, both within the context of digital white matter segmentation and within the context of representation more generally, is somewhat counterintuitive.  **In practice, the way we form a representation is by applying a (potentially large and complicated) sequence of _exclusion_ conditions to some set of candidates**.  Intuitively, we might expect that we would be trying to identify the "essential features" of our category of interest, but that's not really a viable tactic, from a practical standpoint.  Instead, what we'll see is that what we're actually doing with white matter segmentation  is applying an (ideally finite) set of rules to a data object to _exclude_ everything _except_ the specific class (or token) we are interested in.  In providing a semantics--a systematic account of how to link a data token to a  "real world" category--we will be providing a comprehensive ) account of the tactics that can be used to eliminate data/representation elements that are inconsistent with salient properties of the "real world" class.  This is what is entailed by a semantics of white matter, and hopefully it is what you will find contained in the following chapters.