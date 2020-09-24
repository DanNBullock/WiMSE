#!/usr/bin/env python
# coding: utf-8

# In[1]:


#from the WMQL website:"Import the freesurfer label definitions from the Desikan atlas (Desikan et al 2006)"
#You're actually importing the full FS look up table: https://surfer.nmr.mgh.harvard.edu/fswiki/FsTutorial/AnatomicalROI/FreeSurferColorLUT
#The FreeSurfer.qry contents are listed at https://github.com/demianw/tract_querier/blob/master/tract_querier/data/FreeSurfer.qry
#import FreeSurfer.qry

#lets leverage the matlab implementation from wma_tools found at:
#https://github.com/DanNBullock/wma_tools/blob/master/bsc_streamlineCategoryPriors_v6.m

#https://github.com/DanNBullock/wma_tools/blob/a0c430694a1e39d1975dac372347733c7cd69d0e/bsc_streamlineCategoryPriors_v6.m#L35
#subcortical.side |= (
#        (Thalamus_Proper.side or Caudate.side or Putamen.side or
#         Pallidum.side or Hippocampus.side or Amygdala.side or
#         Insula.side or Operculum.side or Accumbens_area.side
#         Substancia_Nigra.side)  
#     )

#https://github.com/DanNBullock/wma_tools/blob/a0c430694a1e39d1975dac372347733c7cd69d0e/bsc_streamlineCategoryPriors_v6.m#L36
#spine |= (
#        (Brain_Stem or VentralDC.left or VentralDC.right)  
#     )

#https://github.com/DanNBullock/wma_tools/blob/a0c430694a1e39d1975dac372347733c7cd69d0e/bsc_streamlineCategoryPriors_v6.m#L37
#cerebellum.side |= (
#        (Cerebellum_White_Matter.side or Cerebellum_Cortex.side)  
#     )

#https://github.com/DanNBullock/wma_tools/blob/a0c430694a1e39d1975dac372347733c7cd69d0e/bsc_streamlineCategoryPriors_v6.m#L38
#ventricles|= (
#        (choroid_plexus.left or choroid_plexus.right or 
#         Lateral_Ventricle.left or Lateral_Ventricle.right 
#         third_Ventricle or fourth_Ventricle  or CSF
#         Inf_Lat_Vent.left or Inf_Lat_Vent.right
#         vessel.left or vessel.right or
#         fifth_Ventricle or non_WM_hypointensities or
#         non_WM_hypointensities.left or non_WM_hypointensities.right)  
#     )

#https://github.com/DanNBullock/wma_tools/blob/a0c430694a1e39d1975dac372347733c7cd69d0e/bsc_streamlineCategoryPriors_v6.m#L39
#whiteMatter.side |= (
#        (Cerebral_White_Matter.side)  
#     )

