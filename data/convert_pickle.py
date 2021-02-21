'''
converts the pickle file containing the paremeters of the task from .pickle into .npz format
'''

## Imports
import numpy as np
import pickle
import os

## go through all files/folders in current path
for name in os.listdir(os.getcwd()):
    ## check if file is a folder
    if os.path.isdir(os.path.join(os.getcwd(), name)):
        ## go inside that folder
        path = os.path.join(os.getcwd(), name)  
        ## search the .pickle file, open it
        with open(os.path.join(path,"parameters.pickle"), "rb") as the_file:
            parameters = pickle.load(the_file)
        ## save whole content as .npz file
        np.savez(os.path.join(path,"parameters.npz"), **parameters)