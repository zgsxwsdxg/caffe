#!/usr/bin/env sh
# Compute the mean image from the imagenet training lmdb
# N.B. this is available in data/ilsvrc12

EXAMPLE=examples/form
DATA=data/form
TOOLS=build/tools

$TOOLS/compute_image_mean $EXAMPLE/form_train_lmdb \
  $DATA/form_mean.binaryproto

echo "Done."
