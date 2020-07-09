#!/bin/bash
wget -O inventario.csv https://www.depau.es/webservices/prestashop/968a9338-5e52-49b4-e895-a5779de8dacb/csv 
if [ -n "$1" ] || [ ! -f "$NETLIFY_BUILD_BASE/cache/images.csv" ]
  then
    wget -O images.csv https://www.depau.es/webservices/tarifa_personalizada/968a9338-5e52-49b4-e895-a5779de8dacb/csv 
    echo "copying images.csv to cache dir"
    echo "$NETLIFY_BUILD_BASE"
    echo "$NETLIFY_CACHE_DIR"
    cp images.csv $NETLIFY_BUILD_BASE/cache/images.csv
fi
python tratar_csv.py
