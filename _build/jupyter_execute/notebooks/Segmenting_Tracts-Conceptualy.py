#!/usr/bin/env python
# coding: utf-8

# # Segmenting Tracts - Conceptualy
# 
# 
# ## What do you mean by "segmentation"
# 
# Its worth reflecting on what what we mean when we talk about "segmentation".  In a certian sense we're using this term way as people in the neuroscience would use "mapping" (though we aren't using _any_ functional information).  Specifically, in either case we are discussing a rule based process for assigning identities to the discrete elements of a composite object.  There's a slight ambiguity in this though, in that its possible we could be referring to a particular segmentation process (in the sense of a method) or we could be using it to refer to a specific resultant product (in the sense of of what the method returns or obtains).  This may seem pedantic, but there are real consequences to this distinction.  For example, if someone were to say "This segmentation is faulty" they could mean quite different things.  In one case they may be indicating that _a particular ouput_ of a segmentation process was not consistent with what was intended or expected.  In another case they may mean that there is something systematically wrong with the process itself and the segmentation method fails to acheive its putative goals.  In subsequent discussions we will endeavor to make our intended meaning clear.  Beyond "faulty" though, there are other important conceptual characteristics we might wish to ascribe to segmentations.
# 
# ## A conceptual framework for segmentations
# 
# As we will later see, there are many different kinds of segmentations, any of which could be preferable depending on one's goals.  In order to help navigate these options it will be useful provide a conceptual framework.  This framework should be thought of as an extension of topics from the opening "Bridges" chapter, with the topics discussed here being specific to digital white matter segmentations.
# 
# ### Complete and incomplete segmentation methods
# 
# When we describe a segmentation process (i.e. a set of rules) as being either "complete" or "incomplete" what we are considering is whether or not the rule process results in a _meaningful_ identity ascription for each constituitive element.  As such, in the case of a complete segmentation, after the end of the application of the segmentation algorithm, each streamline will have received a label ascription.   Notably, labeling an element as "Unknown" or "Unlabeled" would not constitute a meaningful designations, and so segmentation methods which result in this would be considered "incomplete".
# 
# #### An interesting edge case: a single criteria
# 
# One intersting case to consider is a "segmentation" consisting of a single boolean criteria evaluation.  As an explict example of this, one could consider the implementation of a "segmentation" which simply checked to see if if *any* part of a streamline occured left (or right) of the midline.  Thus a streamline either would meet this criteria (and feature some part of itself on the pertinant side) or it would not meet this criteria (and would be constrained to the "other" side).  Arguably this would constitute a meaningful identity ascription, because the information returned from this assesment is just as capable of being useful when used directly (to assess *any* traversal of the relevant side) or indirectly as a negation (to assess containment on the other side). Thus, "both" category ascriptions (true and false) in this case are informative.  Indeed this is true of all singleton logical segmentation operations because of the inherent utility and informativeness of simply negating the outcome.  We will see why this doesn't work for composite logical operations when we consider incomplete segmentations.
# 
# #### Examples of complete segmentation methods
# 
# What are some examples of complete segmentations?  The process used in the "A first segmentation" chapter was complete.  This is because each streamline was assigned a label (via the termination of its two endpoints).  For this reason, the algorithms underlying most structural connectomes contitute complete segmentations (under the assumption that all streamlines are accounted for in the resultant matrix/datastructure).  Likewise, any standard masking operation would be a complete (though extremely basic) segmentation, in that the elements would either be labled as having the desired trait present or not present.  An example of this in a tractome would be selecting all streamlines longer than 50 millimeters.  Alternatively, you could select (via a method we won't go into yet) streamlines which cross some specific spatial plane in the brain.  This latter example is extremely important and ends up being one of the fundamental steps of many popular segmentations.  Note that, in such a case, no element (in this case, streamlines) fails to be assessed--either it does meet criteria for crossing the plane or it does not.  A potentially unintuitive example of a complete segmentation method would be an algorithm that clusters streamlines by their distance from one another.  This would result in labeled groupings of streamlines based on the similarity of their shape and traversal paths.  This is precisely the logic behind [dipy's RecoBundles](https://www.dipy.org/documentation/1.0.0./examples_built/bundle_extraction/).  If these are examples of complete segmentations, what are examples of incomplete segmentations?
# 
# #### Examples of incomplete segmentations
# 
# If a complete segmentation is one in which each streamline receives an identity ascription, then an incomplete segmentation is one in which each streamline **does not** receive a (meaningful) identity ascription.  It is quite possible for a segmentation algorithm to iterate across several sub-algorithms--each designed to segment a particular white matter structure--but for there to be some number of streamlines which do not meet the criteria for **any** of those sub-algorithms.  Thus, in these cases, some subset of a tractogram's streamlines will be assigned to one of N explicit identities (eg. "structure/tract 1", "structure/tract 2", "strcuture/tract 3", etc) while the remaining streamlines go "unassigned".  This is quite similar to how many voxels in volumetric parcellations are not assigned an explicit identity and are clumped together in an "unknown/unassigned" category (typically represented in the data structure with a 0).  From a signal detection persepctive, there are, in essence, _two_ possible characterizations for any particular of these remaining streamlines:
# 
#     - 1.  The segmentation algorithm **failed** and did not assign this streamline to a specific identity **when it should have**.
#     - 2 . The segmentation algorithm **succeeded** and did not assign this streamline to a specific identity because it **did not** meet **any** of the criteria for identity ascription.
#     
# The distinction between complete and incomplete segmentations highlights the role played by "white matter ontologies" which we will consider next.
#     
# ### Segmentations are predicated upon ontologies
# 
# In that a segmentation algorithm's goal is to return a systematic mapping between the input enitity (in this case, a white matter tractogram) and (for the temporary lack of a better description) "a list of the relevant things there are", segmentation algorithms are deeply rooted in the notion of an associated ontology.  Here, by ontology, we  mean the term in the [information science sense](https://en.wikipedia.org/wiki/Ontology_(information_science)).  Of particular interest to us (as segmenters) are the ontology sub-components of "individuals", "classes", "attributes", and "rules".  First and foremost are the individuals.  For us, these are the individual entities  Any given segmentation algorithm is predicated upon the specification of a set of 
# 
# 
# 
# ### A segmentation product is the result of a tripartite interaction
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# # Why segment a tract
# 
# 
# ##  Track Vs Tract
# 
# ## White Matter tract Vs Streamline Tract
# 
# ## unanswered questions
# 
# ### How many uncharacterized / undiscovered tracts are there?
# ### What characterizes white matter that *is* part of a tract and what characterizes white mattter that *isn't* part of a tract?
# ### Are all parts of the white matter part of a tract?
# 

# In[ ]:




