#!/bin/bash
wget -O inventario.csv https://www.depau.es/webservices/prestashop/968a9338-5e52-49b4-e895-a5779de8dacb/csv -q
if [ -n "$1" ]
  then
    wget -O images.csv https://www.depau.es/webservices/tarifa_personalizada/968a9338-5e52-49b4-e895-a5779de8dacb/csv -q
fi
python tratar_csv.py
