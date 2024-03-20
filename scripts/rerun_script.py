#!/usr/bin/env python3

import rerun as rr
import numpy as np
from plyfile import PlyData

rr.init("rerun_example_my_data", spawn=True)

# Read the PLY file
plydata_sfm = PlyData.read('/home/skumar/benchmark_pixSFM/ply/sfm_in_camera_frame_orange.ply')
plydata_svo = PlyData.read('/home/skumar/benchmark_pixSFM/ply/svo_yellow.ply')
#plydata_sfm_in_camera_frame = PlyData.read('/home/skumar/benchmark_pixSsFM/ply/sfm_yellow_old.ply')
#plydata_svo = PlyData.read('/home/skumar/benchmark_pixSFM/svo_output/frame_20/pointcloud/pointcloud.ply')

# Extract the vertex data
v1 = plydata_sfm['vertex'].data
v2 = plydata_svo['vertex'].data
#v3 = plydata_sfm_in_camera_frame['vertex'].data

# Extract the positions
p1 = np.vstack([v1['x'], v1['y'], v1['z']]).T
p2 = np.vstack([v2['x'], v2['y'], v2['z']]).T
#p3 = np.vstack([v3['x'], v3['y'], v3['z']]).T


'''
mx_x_p2 = np.max([np.max(p2[:, 0])])
mn_x_p2 = np.min([np.min(p2[:, 0])])

mx_y_p2 = np.max([np.max(p2[:, 1])])
mn_y_p2 = np.min([np.min(p2[:, 1])])

mx_z_p2 = np.max([np.max(p2[:, 2])])
mn_z_p2 = np.min([np.min(p2[:, 2])])


print(f"mx_x: {mx_x_p2}, mn_x: {mn_x_p2}\nmx_y: {mx_y_p2}, mn_y: {mn_y_p2}\nmx_z: {mx_z_p2}, mn_z: {mn_z_p2}")
'''

# Extract the colors
c1 = np.vstack([v1['red'], v1['green'], v1['blue']]).astype(np.uint8).T
c2 = np.vstack([v2['red'], v2['green'], v2['blue']]).astype(np.uint8).T
#c3 = np.vstack([v3['red'], v3['green'], v3['blue']]).astype(np.uint8).T

rr.log("sfm",rr.Points3D(p1, colors=c1, radii=0.01))
rr.log("svo",rr.Points3D(p2, colors=c2, radii=0.01  ))

