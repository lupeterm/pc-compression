import os
from .time_it import metrics
from .Results import SingleResult
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
                  
                  
                  
Note by @lupeterm: Code was slightly modified for this evaluation
"""
import numpy as np
import open3d as o3d
from functools import partial
def d1halfing_fast(pmin,pmax,pdepht):
    return np.linspace(pmin,pmax,2**int(pdepht)+1)
                       
def octreecodes(ppoints,pdepht):
    minx=np.amin(ppoints[:,0])
    maxx=np.amax(ppoints[:,0])
    miny=np.amin(ppoints[:,1])
    maxy=np.amax(ppoints[:,1])
    minz=np.amin(ppoints[:,2])
    maxz=np.amax(ppoints[:,2])
    xletra=d1halfing_fast(minx,maxx,pdepht)
    yletra=d1halfing_fast(miny,maxy,pdepht)
    zletra=d1halfing_fast(minz,maxz,pdepht)
    otcodex=np.searchsorted(xletra,ppoints[:,0],side='right')-1
    otcodey=np.searchsorted(yletra,ppoints[:,1],side='right')-1
    otcodez=np.searchsorted(zletra,ppoints[:,2],side='right')-1
    ki=otcodex*(2**(pdepht*2))+otcodey*(2**pdepht)+otcodez
    return (ki,minx,maxx,miny,maxy,minz,maxz)

def octreezip(path_to_ply, output_file, depth):
    pcd = o3d.io.read_point_cloud(path_to_ply,format='auto')
    ppoints=np.asarray(pcd.points)
    if len(ppoints)>0:
        occ=octreecodes(ppoints,depth)
        occsorted=np.sort(occ[0])
        prec=np.amax(np.asarray([occ[2]-occ[1],occ[4]-occ[3],occ[6]-occ[5]])/(2**depth))
        paramarr=np.asarray([depth,occ[1],occ[2],occ[3],occ[4],occ[5],occ[6]]) #depth and boundary
        np.savez_compressed(file=output_file,points=occsorted,params=paramarr)
        print(f'Compressed into: {output_file} | Storing resolution:'+str(prec))
    else:
        retmessage='PC is empty, bad, or missing'

def octreeunzip(encoded_file, decoded_file):
    pc=np.load(encoded_file)
    pcpoints=pc['points']
    pcparams=pc['params']
    pdepht=(pcparams[0])
    minx=(pcparams[1])
    maxx=(pcparams[2])
    miny=(pcparams[3])
    maxy=(pcparams[4])
    minz=(pcparams[5])
    maxz=(pcparams[6])
    xletra=d1halfing_fast(minx,maxx,pdepht)
    yletra=d1halfing_fast(miny,maxy,pdepht)
    zletra=d1halfing_fast(minz,maxz,pdepht)    
    occodex=(pcpoints/(2**(pdepht*2))).astype(int)
    occodey=((pcpoints-occodex*(2**(pdepht*2)))/(2**pdepht)).astype(int)
    occodez=(pcpoints-occodex*(2**(pdepht*2))-occodey*(2**pdepht)).astype(int)
    koorx=xletra[occodex]
    koory=yletra[occodey]
    koorz=zletra[occodez]
    points=np.array([koorx,koory,koorz]).T
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    o3d.io.write_point_cloud(decoded_file, pcd)

    print(f'Decoded to {decoded_file}')


def pccomp(path_to_ply: str, output_folder_enc: str, output_folder_dec: str):
    assert path_to_ply.endswith(".ply")
    assert os.path.exists(path_to_ply)
    if not os.path.exists(output_folder_enc):
        os.mkdir(output_folder_enc)
    if not os.path.exists(output_folder_dec):
        os.mkdir(output_folder_dec)

    print(f"Running pccomp on {path_to_ply = }")
    _, f = path_to_ply.rsplit("/", 1)
    enc_file = os.path.join(output_folder_enc, f.replace(".ply", ".npz"))
    dec_file = os.path.join(output_folder_dec, f.replace(".npz", ".ply"))
    print(f"{enc_file=}, {dec_file=}")

    @metrics
    def pccomp_enc():
        octreezip(path_to_ply=path_to_ply,output_file=enc_file, depth=16) # 11-16 is recommended apparently

    @metrics
    def pccomp_dec():
        octreeunzip(encoded_file=enc_file, decoded_file=dec_file)

    duration_enc_ns = pccomp_enc()
    duration_dec_ns = pccomp_dec()
    enc_size = os.path.getsize(enc_file) * 8
    num_points = int(f.replace(".ply", "").rsplit("-")[1])
    bpp = enc_size / num_points
    print(f"{bpp =}")
    return SingleResult(
        file=f,
        bpp=bpp,
        time_enc_ns=duration_enc_ns, # type: ignore
        time_dec_ns=duration_dec_ns, # type: ignore
        enc_file_size_bits=enc_size,
        num_points=num_points,
    )
    
    
    