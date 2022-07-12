#!/bin/bash

THREADS=64

rm -rf data
mkdir data

for ((i=0;i<$THREADS;i++)); do
	node clip_vods.js $i $THREADS &
done

wait
