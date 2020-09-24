#!/usr/bin/env python
# coding: utf-8

# # The measurement, the object, and the modality - Whats in measured in diffusion imaging
# 
# **Extending the logic of a data structure** 
# 
# _Stretching a data object across another dimension_
# 
# Previously, when we discussed the data structure of a T1 we noted that it was a 3 dimensional data structure representing a 3 dimensional object.  Likewise we noted that jpeg imgaes were a 2 (ish, in the case of color) dimensional data represenetation.  In a manner of speaking, the 3-dimensional data structure is just an extension of the same data representation practice as the 2D image.  If we were able to go from 2 dimensional to 3 dimensional, can we go from 3 to 4?
# 
# Thinking back to a 2 dimensional image, it's possible to extend these objects across the temporal dimension to create an ordered sequence of images.  This could be something like a [Zoetrope](https://en.wikipedia.org/wiki/Zoetrope), or, perhaps more straighforwardly, a movie. In the case of MRI data, we could also extend this data object across the temporal dimension to obtain something like a 3 dimensional movie.  This is, in essence, the idea behind [fMRI](https://en.wikipedia.org/wiki/Functional_magnetic_resonance_imaging), though the activity we are viewing evolve over time with that imaging modality is [Blood-oxygen-level-dependent(BOLD)](https://en.wikipedia.org/wiki/Blood-oxygen-level-dependent_imaging#:~:text=Blood%2Doxygen%2Dlevel%2Ddependent%20imaging%2C%20or%20BOLD%2D,active%20at%20any%20given%20time.), rather than surface reflectance.  For now though, its enough to know that we can extend certian data types (i.e. digital photography images and MRI Volumes/NIFTIs) across the temporal dimenson.  But this isn't the *only* manner in which we can extend them.
# 
# **Rather than taking a sequence of images across time, what if we simply rotated the object in place?**
# 
# Let's consider this possibility in the case of 2D images and, for the sake of consistency with our previous examples, lets use the world as an example.  In this case, we'll pretend that we've placed a satellite in orbit around the equator *but* it's "stationary" such that Earth appears to be rotating at such a speed that it completes a full rotation every 24 hours.  In a sense, this is basically the same effect as rotating a stationary object in front of a camera.  As the world rotates, we take an image every so often until one full rotation has been made.  By doing this we have compiled a sequence of images that depict the same object from a number of angles.  Furthermore, this would allow us to make some decent inferences about the surface structure of the 3D object from the compilation of 2D images.
# 
# Lets go ahead and explore this notion by looking at the images from a gif depicting a rotating earth.  Run the next block of code, which contains some code needed to explore a gif, and then use the interactive slider in the subsequent block to rotate around the Earth and get a sense of how a sequence of 2D images can give you information about the structure of a 3D object.

# In[1]:


# this section of code is necessary in order to extract specific frames from a gif sequence
# go ahead and run it and move to the next section

import os
from PIL import Image
# directly from https://gist.github.com/almost/d2832d0998ad9dfec2cacef934e7d247
# Based on https://gist.github.com/BigglesZX/4016539 (but adapted to be a
# generator that yields frames instead of a function that saves out frames)

def analyseImage(im):
    '''
    Pre-process pass over the image to determine the mode (full or additive).
    Necessary as assessing single frames isn't reliable. Need to know the mode
    before processing all frames.
    '''
    results = {
        'size': im.size,
        'mode': 'full',
    }
    try:
        while True:
            if im.tile:
                tile = im.tile[0]
                update_region = tile[1]
                update_region_dimensions = update_region[2:]
                if update_region_dimensions != im.size:
                    results['mode'] = 'partial'
                    break
            im.seek(im.tell() + 1)
    except EOFError:
        pass
    im.seek(0)
    return results


def getFrames(im):
    '''
    Iterate the GIF, extracting each frame.
    '''
    mode = analyseImage(im)['mode']

    p = im.getpalette()
    last_frame = im.convert('RGBA')

    try:
        while True:
            '''
            If the GIF uses local colour tables, each frame will have its own palette.
            If not, we need to apply the global palette to the new frame.
            '''
            if not im.getpalette():
                im.putpalette(p)

            new_frame = Image.new('RGBA', im.size)

            '''
            Is this file a "partial"-mode GIF where frames update a region of a different size to the entire image?
            If so, we need to construct the new frame by pasting it on top of the preceding frames.
            '''
            if mode == 'partial':
                new_frame.paste(last_frame)

            new_frame.paste(im, (0,0), im.convert('RGBA'))
            yield new_frame

            last_frame = new_frame
            im.seek(im.tell() + 1)
    except EOFError:
        pass


def processImage(path):
    im = Image.open(path)
    for (i, frame) in enumerate(getFrames(im)):
        print("saving %s frame %d, %s %s" % (path, i, im.size, im.tile))
        frame.save('%s-%d.png' % (''.join(os.path.basename(path).split('.')[:-1]), i), 'PNG')


# In[2]:


from PIL import Image
from PIL import GifImagePlugin
from ipywidgets import interact, interactive, fixed, interact_manual
from ipywidgets import IntSlider
import itertools
import matplotlib
from matplotlib.pyplot import imshow
import numpy as np


#this code ensures that we can navigate the WiMSE repo across multiple systems
import subprocess
import os
#get top directory path of the current git repository, under the presumption that 
#the notebook was launched from within the repo directory
gitRepoPath=subprocess.check_output(['git', 'rev-parse', '--show-toplevel']).decode('ascii').strip()

#move to the top of the directory
os.chdir(gitRepoPath)

worldGif = Image.open(os.path.join(gitRepoPath,'images','Blue_Marble_rotating.gif'))

gifFrameNum=worldGif.n_frames

print(gifFrameNum/3)

framesGenerator=getFrames(worldGif)

def update(frameSelect):
    get_ipython().run_line_magic('matplotlib', 'inline')
    caughtFrame=next(itertools.islice(framesGenerator, frameSelect, None))
    imshow(np.asarray(caughtFrame))
    
    #imshow(caughtFrame)


frameSelect=IntSlider(min=1, max=gifFrameNum, step=1,continuous_update=False)    

interact(update, frameSelect=frameSelect)


# 

# In[ ]:




