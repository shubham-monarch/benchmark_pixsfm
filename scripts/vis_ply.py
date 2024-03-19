#!/usr/bin/env python3  

import open3d as o3d

# Load the point clouds
pcd1 = o3d.io.read_point_cloud("/home/skumar/benchmark_pixSFM/ply/svo_pink.ply")
pcd2 = o3d.io.read_point_cloud("/home/skumar/benchmark_pixSFM/ply/sfm_yellow.ply")

# Visualize the point clouds
#o3d.visualization.draw_geometries([pcd1, pcd2])