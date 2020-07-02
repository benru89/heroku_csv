#!/bin/bash

source /var/www/vhosts/pclideres.com/miniconda2/etc/profile.d/conda.sh
conda activate excel
touch test1
python test1.py
