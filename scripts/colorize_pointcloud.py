#!/usr/bin/env python3

import pycolmap
import argparse
import numpy as np
from pathlib import Path
from tqdm import tqdm

colors_dict = {
    "red": np.array([255, 0, 0]),
    "green": np.array([0, 255, 0]),
    "blue": np.array([0, 0, 255]),
    "yellow": np.array([255, 255, 0]),
    "cyan": np.array([0, 255, 255]),
    "magenta": np.array([255, 0, 255]),
    "white": np.array([255, 255, 255]),
    "black": np.array([0, 0, 0]),
    "orange": np.array([255, 165, 0]),
    "purple": np.array([128, 0, 128]),
    "brown": np.array([165, 42, 42]),
    "gray": np.array([128, 128, 128]),
    "pink": np.array([255, 192, 203]),
    "lime": np.array([0, 255, 0]),
    "indigo": np.array([75, 0, 130])
}

def colorize_pointcloud(ply_path, color, name):
    
    ply_file_path = Path(ply_path)

    if ply_file_path.suffix != '.ply':
        raise ValueError(f"The file at {ply_file_path} is not a .PLY file.")
    
    if color not in colors_dict:
        raise ValueError(f"Color {color} not found in color dictionary")

    model = pycolmap.Reconstruction()
    model.importPLY(ply_file_path.as_posix())
    

    custom_color = colors_dict[color]
    for id, point in tqdm(model.points3D.items(s), desc="Colorizing points"):
        model.add_point3D(xyz = point.xyz, track = pycolmap.Track(), color = custom_color)

    output_ply_path =  "/home/skumar/benchmark_pixSFM/ply/" + name 
    model.exportPLY(output_ply_path.as_posix())


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Colorize pointcloud')
    parser.add_argument('--input_path', type=str, required = True, help='PLY file path')
    parser.add_argument('--color', type=str,  help='target color')
    parser.add_argument('--output_name', type=str, help='output PLY name')
    
    args = parser.parse_args()

    colorize_pointcloud(args.input_path, args.color, args.output_name)

