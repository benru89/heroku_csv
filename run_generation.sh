#!/bin/bash
wget -O inventario.csv https://www.depau.es/webservices/prestashop/968a9338-5e52-49b4-e895-a5779de8dacb/csv -q
if [ -n "$1" ] || [ ! -f "$NETLIFY_BUILD_BASE/cache/images.csv" ]
  then
    echo "download fresh images.csv"
    wget -O images.csv https://www.depau.es/webservices/tarifa_personalizada/968a9338-5e52-49b4-e895-a5779de8dacb/csv -q
    echo "copying images.csv to cache dir"
    echo "$NETLIFY_BUILD_BASE"
    echo "$NETLIFY_CACHE_DIR"
    cp images.csv $NETLIFY_BUILD_BASE/cache/images.csv
  else
    echo "copying images.csv from cache dir"
    cp $NETLIFY_BUILD_BASE/cache/images.csv images.csv
fi
echo "generate csv"
python tratar_csv.py
echo "success"
