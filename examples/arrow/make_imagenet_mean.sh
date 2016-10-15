#!/usr/bin/env sh
# Compute the mean image from the imagenet training lmdb
# N.B. this is available in data/ilsvrc12

EXAMPLE=examples/arrow
DATA=data/arrow
TOOLS=build/tools

$TOOLS/compute_image_mean $EXAMPLE/arrow_train_lmdb \
  $DATA/arrow_mean.binaryproto

echo "Done."
