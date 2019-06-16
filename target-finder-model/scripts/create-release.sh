#!/bin/sh -e

cd $(dirname "$0")

yolo_weights_file="../target_finder_model/data/yolo3detector-train_final.weights"
clf_weights_file="../target_finder_model/data/preclf-train_final.weights"
yolo_cfg_file="../target_finder_model/data/yolo3detector-test.cfg"
clf_cfg_file="../target_finder_model/data/preclf-test.cfg"

# Check that the model files exist.
[ -f "$yolo_weights_file" ] || (>&2 echo "Missing Yolo Weights" && exit 1)
[ -f "$clf_weights_file" ] || (>&2 echo "Missing Clf Weights" && exit 1)
[ -f "$yolo_cfg_file" ] || (>&2 echo "Missing Yolo Cfg" && exit 1)
[ -f "$clf_cfg_file" ] || (>&2 echo "Missing Clf Cfg" && exit 1)

# Find the version number to release.
version=$(grep -o -e "'.*'" "../target_finder_model/version.py" | tr -d "'")

echo "Detected version ""$version"

tf_stage_dir="../release/staging/target-finder-model"
archive_name="target-finder-model-""$version"".tar.gz"

# Create the staging directory and the target-finder folder.
echo "Staging files"
mkdir -p "$tf_stage_dir""/target_finder_model/data/"
cp "$yolo_weights_file" "$tf_stage_dir""/target_finder_model/data/"
cp "$clf_weights_file" "$tf_stage_dir""/target_finder_model/data/"
cp "$yolo_cfg_file" "$tf_stage_dir""/target_finder_model/data/"
cp "$clf_cfg_file" "$tf_stage_dir""/target_finder_model/data/"

# Copy over python files.
mkdir -p "$tf_stage_dir""/target_finder_model"
find "../target_finder_model/" -name "*.py" -exec cp "{}" \
  "$tf_stage_dir/target_finder_model/" \;

# Copy over configuration and informational files.
cp ../README.md ../LICENSE \
  ../setup.py "$tf_stage_dir"

# Compress the directory.
echo "Creating archive"

cd "../release/staging"
tar -czvf "$archive_name" "target-finder-model"
mv "$archive_name" ..

echo "\033[32mCreated target-finder-model release" \
  "(""$archive_name"")\033[0m"

# Remove the staging directory.
echo "Removing staging files"
cd ..
rm -rf staging
