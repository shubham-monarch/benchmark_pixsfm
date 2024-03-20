#!/usr/bin/env python3

from pathlib import Path    
import pycolmap
import sys
import numpy as np
import os
import cv2 

sys.path.append("/home/skumar/colmap/scripts/python")
from read_write_model import read_images_binary

images = Path('pixsfm_dataset/')

fx = 1093.2768
fy = 1093.2768
cx = 964.989
cy = 569.276

def get_camera_matrix(fx, fy, cx, cy):
    return np.array([[fx,0 , cx], [0, fy, cy], [0 , 0, 1]]).astype(np.float64)

def compute_cam_extrinsics(img):
    from read_write_model import qvec2rotmat
    R = qvec2rotmat(img.qvec)
    t = img.tvec.reshape(3,-1)
    R_t = np.concatenate((R,t), axis = 1)
    #R_t = np.vstack([np.array([0,0,0,1]), R_t])
    return R_t    #  4 * 4 matrix

def compute_projection_matrix(K, R_t):
    return np.dot(K, R_t)    

def HasPointPositiveDepth(proj_matrix, point3D):
    return np.dot(proj_matrix[2], point3D) >= np.finfo(float).eps

''' SFM MODEL '''

print("Processing SFM MODEL ...")
sfm_input_path = Path("dense_reconstruction/output")
print(f"sfm_input_path: {sfm_input_path}")

sfm_model = pycolmap.Reconstruction()
sfm_model.read_binary(sfm_input_path.as_posix())

sfm_images_path = sfm_input_path / "images.bin"
sfm_images_dict = read_images_binary(sfm_images_path)

left_img = sfm_images_dict[13]
left_K = get_camera_matrix(fx,fy,cx,cy)
left_Rt = compute_cam_extrinsics(left_img)
left_P = compute_projection_matrix(left_K, left_Rt)


from read_write_model import read_points3D_binary
sfm_points_path = sfm_input_path / "points3D.bin"
sfm_points_dict = read_points3D_binary(sfm_points_path)

sfm_X = np.array([value.xyz for value in sfm_points_dict.values()])
ones = np.ones((sfm_X.shape[0], 1))
sfm_X = np.hstack((sfm_X, ones)) #homogenezing sfm_X

sfm_x = np.dot(left_P, sfm_X.T).T #projecting to camera

sfm_x_filtered = sfm_x[sfm_x[:, 2] >= 0]  #filtering points with negative depth

sfm_x = sfm_x_filtered[:, :2] / sfm_x_filtered[:, 2:] #dehomogenizing

#sfm_x = sfm_x[sfm_x[:, 0] < 1080 and sfm_x[:,1] < 1920]
#sfm_x = svo_x[(svo_x[:, 0] < 1080) & (svo_x[:, 1] < 1920)]

sfm_x = sfm_x[(sfm_x[:, 0] < 1080) & (sfm_x[:, 1] < 1920)]

print(f"sfm_x.shape: {sfm_x.shape}")

''' SVO MODEL '''

print("Processing SVO MODEL ...")

svo_input_path = Path("svo_output/frame_20/pointcloud/pointcloud.ply")
svo_model = pycolmap.Reconstruction()
svo_ply = svo_model.import_PLY(svo_input_path.as_posix())

svo_X = np.array([point.xyz for id, point in svo_model.points3D.items()])

#ones = np.ones((svo_X.shape[0], 1))
#svo_X = np.hstack((svo_X, ones)) #homogenizing svo_X
svo_x = np.dot(left_K, svo_X.T).T #projecting to camera

svo_x_filtered = svo_x[svo_x[:, 2] >= 0] #filtering points with negative depth
svo_x = svo_x_filtered[:, :2] / svo_x_filtered[:, 2:] #dehomogenizing

svo_x = svo_x[(svo_x[:, 0] < 1080) & (svo_x[:, 1] < 1920)]

print(f"svo_x.shape: {svo_x.shape}")

''' PLOTTING POINTS ON LEFT IMAGE'''

left_image_name = sfm_images_dict[13].name
left_image_path = os.path.join(images, Path(left_image_name))

print(f"left_image_path: {left_image_path}")


image_ = cv2.imread(left_image_path)
image_scaled_ = cv2.resize(image_, (800,800))       
for x,y in sfm_x: 
    #cv2.circle(image_scaled_, (int(x), int(y)), radius=1, color=(255, 0, 0), thickness=1)
    pass

for x,y in svo_x: 
    cv2.circle(image_scaled_, (int(x), int(y)), radius=1, color=(0, 255, 255), thickness=1)
    #pass

cv2.imshow('left_image', image_scaled_)
cv2.waitKey(0)
cv2.destroyAllWindows()
