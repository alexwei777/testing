#!/usr/bin/env python
# coding: utf-8

# In[1]:


from nd2reader import ND2Reader
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import os


# In[1]:



# In[2]:


path_of_the_directory = 'output'
paths = Path(path_of_the_directory).glob('**/*.nd2')
files = [str(x) for x in paths if x.is_file()]
files.sort()


# In[3]:


# Extract channel 0 and 2. Write to tif file.
for file in files:
    nd2 = ND2Reader(file)
    
    temp = nd2.get_frame_2D(c=0, z=1)
    name = os.path.splitext(file)[0] + '_c0.tif'
    cv.imwrite(name, temp)
    
    temp = nd2.get_frame_2D(c=2, z=1)
    name = os.path.splitext(file)[0] + '_c2.tif'
    cv.imwrite(name, temp)


# In[4]:


import cellprofiler_core.pipeline
import cellprofiler_core.preferences
import cellprofiler_core.utilities.java

cellprofiler_core.preferences.set_headless()


# In[5]:


# Set the output directory
current_dir = Path().absolute()
cellprofiler_core.preferences.set_default_output_directory(f"{current_dir}/output")


# In[6]:


cellprofiler_core.utilities.java.start_java()


# In[7]:


# Run cell pipeline.
file_list = list(Path(path_of_the_directory).absolute().glob('*c0.tif'))
cell_files = [file.as_uri() for file in file_list]
cell_pipeline = cellprofiler_core.pipeline.Pipeline()
cell_pipeline.load("cell.cppipe")
cell_pipeline.read_file_list(cell_files)
cell_output = cell_pipeline.run()


# In[8]:


# Run NEC pipeline.
file_list = list(Path(path_of_the_directory).absolute().glob('*c2.tif'))
NEC_files = [file.as_uri() for file in file_list]
NEC_pipeline = cellprofiler_core.pipeline.Pipeline()
NEC_pipeline.load("NEC.cppipe")
NEC_pipeline.read_file_list(NEC_files)
NEC_output = NEC_pipeline.run()


# In[8]:


# # Sanity check.
# cell_output.get_measurement_columns()
# cell_pipeline.modules()


# In[9]:


cellprofiler_core.utilities.java.stop_java()

