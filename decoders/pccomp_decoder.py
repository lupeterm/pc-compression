#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
###################################################################
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.

copyright (c) 2020, Peter Szutor

@author: Peter Szutor, Hungary, szppaks@gmail.com
Created on Wed Feb 26 17:23:24 2020
###################################################################



Octree-based lossy point-cloud compression with open3d and numpy
Average compressing rate (depends on octreee depth setting parameter): 0.012 - 0.1   


Input formats: You can get a list of supported formats from : http://www.open3d.org/docs/release/tutorial/Basic/file_io.html#point-cloud
               (xyz,pts,ply,pcd)

Usage:

Dependencies: Open3D, Numpy  (You can install theese modules:  pip install open3d, pip install numpy)    

Compress a point cloud:

octreezip(<filename>,<depth>) -> <result>
<filename>: (str) Point Cloud file name. Saved file name: [filename without ext]_ocz.npz  (Yes, it's a numpy array file)
<depth>   : (str) Octree depth. You can try 11-16 for best result. Bigger depht results higher precision and bigger compressed file size.
<result>  : (str) If the compressing was success you get: "Compressed into:[comp.file name] | Storing resolution:0.003445". Storing resolution means the precision.
                  The PC file is missing or bad: "PC is empty, bad, or missing"
                  Other error: "Error: [error message]"


Uncompressing:
octreeunzip(<filename>) -> <result>
<filename>: (str) Zipped Point Cloud file name (npz). Saved file name: [filename].xyz  (standard XYZ text file)
<result>  : (str) If the compressing was success you get: "Saved: [filename].xyz"
                  Other error: "Error: [error message]"
"""
import numpy as np
import os


def d1halfing_fast(pmin, pmax, pdepht):
    return np.linspace(pmin, pmax, 2 ** int(pdepht) + 1)


def octreeunzip(pfilename: str, save: bool, ret: bool):
    try:
        pc = np.load(pfilename)
        pcpoints = pc["points"]
        pcparams = pc["params"]
        pdepht = pcparams[0]
        minx = pcparams[1]
        maxx = pcparams[2]
        miny = pcparams[3]
        maxy = pcparams[4]
        minz = pcparams[5]
        maxz = pcparams[6]
        xletra = d1halfing_fast(minx, maxx, pdepht)
        yletra = d1halfing_fast(miny, maxy, pdepht)
        zletra = d1halfing_fast(minz, maxz, pdepht)
        occodex = (pcpoints / (2 ** (pdepht * 2))).astype(int)
        occodey = ((pcpoints - occodex * (2 ** (pdepht * 2))) / (2**pdepht)).astype(int)
        occodez = (
            pcpoints - occodex * (2 ** (pdepht * 2)) - occodey * (2**pdepht)
        ).astype(int)
        koorx = xletra[occodex]
        koory = yletra[occodey]
        koorz = zletra[occodez]
        points = np.array([koorx, koory, koorz]).T
        if save:
            np.savetxt(os.path.splitext(pfilename)[0] + ".xyz", points, fmt="%.4f")
        if ret:
            return points
        retmessage = "Saved:" + os.path.splitext(pfilename)[0] + ".xyz"
    except Exception as e:
        retmessage = "Error:" + str(e)
    return retmessage
