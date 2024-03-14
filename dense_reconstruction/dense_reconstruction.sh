ROOT_DIR=$HOME/benchmark_pixSFM
IMAGE_PATH=$ROOT_DIR/pixsfm_dataset/
INPUT_PATH=$ROOT_DIR/rig_bundle_adjuster/output/
OUTPUT_PATH=$ROOT_DIR/dense_reconstruction/output/

COLMAP_EXE_PATH=/usr/local/bin

rm -rf $OUTPUT_PATH
mkdir -p $OUTPUT_PATH

$COLMAP_EXE_PATH/colmap image_undistorter \
	--image_path $IMAGE_PATH \
	--input_path $INPUT_PATH \
	--output_path $OUTPUT_PATH


# You must set $COLMAP_EXE_PATH to 
# the directory containing the COLMAP executables.
$COLMAP_EXE_PATH/colmap patch_match_stereo \
  --workspace_path $OUTPUT_PATH
  --workspace_format COLMAP \
  --PatchMatchStereo.max_image_size 2000 \
  --PatchMatchStereo.geom_consistency true

$COLMAP_EXE_PATH/colmap stereo_fusion \
  --workspace_path $OUTPUT_PATH\
  --workspace_format COLMAP \
  --input_type geometric \
  --output_path $OUTPUT_PATH/fused.ply
