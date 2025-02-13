# White Matter Segmentation Education - WiMSE

This set of notebooks has been developed to provide a guide to performing digital segmentations of white matter.  The lessons contained here are designed for advanced undergraduates, advanced STEM students, or persons wanting to become more familiar with the process of the digital segmentation of white matter.  These lessons begin by building a strong foundation of intuitions based on everyday data representations.  Having established this, it moves towards neuroimaging-specific data formats and their use.  Finally, it moves to tractograms and segmentations, demonstrating basic concepts and characteristics, and even allowing users to perform some rudimentary interactive segmentations. 

## Chapter Summaries 

#### Building bridges from the familiar to the unfamiliar

In this introductory chapter we build the conceptual foundations for our endeavor with WiMSE.  We set out to explain the rationale behind expending a great deal of effort building intuitions and elaborating analogies.  Although this chapter covers a number of abstract concepts, the themes and topics that are discussed here will reappear throughout the subsequent chapters as we develop our segmentation skills.  By keeping this discussion in the back of our minds, we’ll be able to orient ourselves with the overarching endeavor even as we focus on the details of the particular lessons in front of us.
 
### Building intuitions with digital images

#### Intro to discretized image representation & maps

In this chapter we begin our exploration of image data with an example that will likely be familiar to many readers: a digital photograph. We'll begin by looking at how the data is arranged within the image data object, what its constituent data entries are, and how those features relate to the image we encounter on our screen.  We'll then move to an exploration of how the quantitative features of the image data can be leveraged to select certain sub-sections of the image via a process referred to as "masking"

#### Aligning two images

In this chapter we build upon the previous chapter's introduction of masks by interactively attempting to overlay a mask derived from one image onto another image.  We also qualitatively assess how well the two images have been aligned. This will serve as a prelude to using the mask from one image to extract certain sub-sections from another image.

#### Multi object maps in images

In this chapter we leverage our ability to align images to select pixels corresponding to US states from a satellite image of the continental United States.  This capability serves as a direct analogy to our ability to select portions of a NIfTI image via the use of a parcellation, which will be explored in later chapters.

#### A consideration of jpegs and brain images

In this chapter we reflect on our observations about digital images as we begin to transition to working with NIfTI data objects.

### Working with NIfTI data

#### How to represent the brain's anatomy - as a volume

In this chapter we shift from a consideration of 2 dimensional, color digital photographs to MRI data stored in a NIfTI.  Although there are a number of conceptual similarities between these data modalities, there are also a number of important distinctions which we consider here.  We also take a look at the affine information contained within the NIfTI header, and reflect on its relevance to aligning 2 dimensional images.

#### How to interpret a volumetric brain segmentation

In this chapter we reflect back on our previous encounters with 2-D parcellations, and expand this to 3-D parcellations.  Many of the same insights that we made in that lesson are repeated once more.  Now though, we are beginning to focus on how these methods are implemented in the special case of studying the brain.  

### White matter and tractography

#### The voxel and the streamline

In this chapter we take a look at the actual data characteristics of a streamline, the elementary component of a tractogram.  We look at a single streamline and demonstrate several mathematical characteristics that it has.  

#### The source tractogram

In this chapter we take a look at a whole brain tractoram.  And note its characteristics as an amalgam of component streamlines.  Our chief takeaway is that we'll need a systematic method to divide up the tractogram in order to extract any insights from it.

### Segmenting tractography

#### A first segmentation

In this chapter we introduce the notion of a tractoram segmentation.  We'll use a parcellation to determine what areas streamlines connect and assign them to tracts accordingly. We'll note that this is a viable way to divide up a tractogarm, but observe that there may be methods that pull out more anatomically coherent structures

#### Biological Plausibility for Tractograms

In this chapter we explore the notion of "Biological Plausibility" and consider its relevance to segmenting the brain.  We take a closer look at examples of how tractography and streamlines can manifest biologically implausible characteristics.  This provides us with a framework for thinking about the manner in which the model features that are streamlines are still accountable to the standards of biology. 

#### ROIs as tools

In this chapter we begin to consider the tools that we will primarily be using to interact with streamlines and tractograms:  Regions of Interest (ROIs).  Although we avoid the subject of specific formats, we nonetheless develop a keen understanding of ROIs' data-structure and tool-based characteristics.

#### Using ROIs as tools

With our understanding of ROIs firmly established, we next move on to actually making use of them to select streamlines.  Here we get our first taste of manual and interactive segmentation as we make use of both planar and spherical ROIs.  

#### A second segmentation - categorical segmentation

In this chapter we examine another approach to full-tractogram segmentation.  This time we use larger amalgams of areas than the previous chapter to form regions like the frontal, parietal, occipital, and temporal lobes.  We'll note that anatomically coherent structures begin to emerge from this approach, and consider how this could serve as a first step towards the segmentation of anatomically coherent white matter structures.

#### Advanced anatomically-based segmentation

In this chapter we being to learn some of the more arcane and specialized techniques associated with white matter segmentation.  These advanced techniques leverage many of the things we have learned in previous lessons, but here we see that the result can be more than the sum of the parts.  Indeed, with the right set-up we note that by adding the individual tools together, the process of segmentation actually gets easier (in a sense) rather than more complicated.

#### Example Segmentation: uncinate fasciculus

Having established and demonstrated our toolkit, we move on to our first segmentation demonstration:  the Uncinate Fasciculus.  In this chapter we discuss both the anatomy logic and the code logic that underlies the implementation of our segmentation.  In doing so, we provide our first example of a generalized segmentation framework.

#### Example Segmentation: inferior fronto-occipital fasciculus (IFOF)

Having segmented the Uncinate Fasciculus, we look to repeat our success with the inferior fronto-occipital fasciculus (IFOF).  We replicate the general structure and approach used in the previous chapter, thereby solidifying the general segmentation approach.

### Epilogue

#### Closing Thoughts

In this brief chapter we look back on the broad endeavor we have made throughout this lesson set.  Some themes are reflected upon, and we close by looking to our aspirations for the future.
