#!/usr/bin/env python
# coding: utf-8

# # Groundwork for an anatomically based segmentation
# 
# (in a real sense, the order in which you apply segmentation logic doesn't really matter, so long as it is properly formatted.  However, from a cognitive point of view, starting with broad, guarenteed characteristics, and work towards refining the segmentation.  Theoretically you could incude a potentially infinite number of criteria.  However, we are attempting to create segmentations in an efficient (with repect to labor) and comprehensible (with respect to transparency) fashion.  As such, the big to small method works best.  Moreover, the more reliable your input tractography is (i.e. more anatomically plausible) the fewer additional criteria you will need to ensure a quality segmentation.  This is because with lower quality tractography inputs there are more and more "edge cases" of streamlines engaging in biologically implausible trajectories.  Past a certian level of specificity, it is rare to find oneself attempting to to separate two anatomically distinct (and thus putatively distinct, insofar as anatomical separability is both the limit and guide to our segmentation efforts).
# ##  Overarching theme: Start big, then move to small
# 
# ### Leveraging a coarse categorical segmentation
# 
# 
