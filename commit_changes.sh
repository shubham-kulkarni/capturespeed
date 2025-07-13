#!/bin/bash


TODAY=$(date '+%Y-%m-%d')

cd /home/pi/capturespeed
git add *
git commit -m "AutoCommit: $TODAY [extra-Test]"
git push

