#!/usr/bin/env python 

import pycolmap  

model = pycolmap.Reconstruction()   
model.importPLYs("../ply/sfm_yellow.ply")

