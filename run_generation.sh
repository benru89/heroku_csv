#!/bin/bash
wget -O inventario.csv https://www.depau.es/webservices/prestashop/968a9338-5e52-49b4-e895-a5779de8dacb/csv
python tratar_csv.py
mv inventario_gen.csv hello/static/inventario.csv
