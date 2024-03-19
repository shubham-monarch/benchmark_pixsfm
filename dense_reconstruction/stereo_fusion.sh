ROOT_DIR=$HOME/benchmark_pixSFM
IMAGE_PATH=$ROOT_DIR/pixsfm_dataset/
INPUT_PATH=$ROOT_DIR/rig_bundle_adjuster/output/
OUTPUT_PATH=$ROOT_DIR/dense_reconstruction/output/

COLMAP_EXE_PATH=/usr/local/bin


$COLMAP_EXE_PATH/colmap stereo_fusion \
  --workspace_path $OUTPUT_PATH\
  --workspace_format COLMAP \
  --input_type geometric \
  --output_type BIN \
  --output_path $OUTPUT_PATH
