import pandas as pd
import json
import yaml
import unidecode


with open('precios/categories.yaml', encoding='iso-8859-1') as f:
    categories = yaml.safe_load(f)

fam_with_margin = {}
subfam_with_margin = {}

for category in categories:
    for familia in category["familias"]:
        nombre = unidecode.unidecode(
            familia["nombre"].lower().replace(" ", ""))
        if familia.get("rangos"):
            margen = familia["rangos"]
        else:
            margen = "-"
        fam_with_margin[nombre] = margen
        if familia.get("subfamilias"):
            for subfamilia in familia["subfamilias"]:
                subfam_name = unidecode.unidecode(
                    subfamilia["nombre"].lower().replace(" ", ""))
                if subfamilia.get("rangos"):
                    margen = subfamilia["rangos"]
                subfam_with_margin[subfam_name] = margen

categoryDict = {}
attrDict = {}


def createCategoryDict(categories):
    for category in categories:
        families = category["familias"]
        for family in families:
            family = unidecode.unidecode(
                family["nombre"].lower().replace(" ", ""))
            categoryDict[family] = unidecode.unidecode(
                category["categoria"].lower().replace(" ", ""))


def getCategoryFromFamily(family_name):
    return categoryDict.get(unidecode.unidecode(family_name.lower().replace(" ", "")), "none")


def getMarginForSubfamily(fam_subfam):
    familia = unidecode.unidecode(fam_subfam[0].lower().replace(" ", ''))
    subfamilia = unidecode.unidecode(fam_subfam[1].lower().replace(" ", ''))
    # primero busca en subfamilias
    margin = subfam_with_margin.get(subfamilia, "-")
    # sino en familias
    if margin == "-":
        margin = fam_with_margin.get(familia, 0)
    return margin


def calculatePrice(margin, price):
    if margin == 0:
        return 0
    if (margin.startswith("[")):
        margin = margin.replace("[", "")
        margin = margin.replace("]", "")
        list_marg = margin.split(",")
        for i, item in enumerate(list_marg):
            if (i == len(list_marg)-1):
                max_price = None
            else:
                max_price = float(list_marg[i+1].split(":")[0])
            min_price = float(item.split(":")[0])
            if price > min_price and (max_price is None or price < max_price):
                eff_margin = float(item.split(":")[1])
                return round(price + (price * (eff_margin/100.0)), 5)
    else:
        return round(price + (price * (int(margin)/100)), 2)


def createAttrDict(atributo):
    splitted = str(atributo).split(',')
    for pair in splitted:
        key = pair.split(':')[0]
        attrDict[key] = ""


def placeAttributes(row):
    splitted = str(row['Atributos']).split(',')
    for pair in splitted:
        if len(pair.split(':')) > 1:
            key = pair.split(':')[0]
            value = pair.split(':')[1]
            row['Att_'+str(key)] = value
    return row


df = pd.read_csv("inventario.csv", encoding='iso-8859-1',
                 quotechar='"', quoting=1, sep=";", index_col=False)


df_images = pd.read_csv("images.csv", encoding='iso-8859-1',
                        quotechar='"', quoting=1, sep=";", usecols=range(0, 25))

df_images.rename(columns={"ID": "Codigo"})
df['ID Articulo'] = df['ID Articulo'].astype(str)
df_images['ID'] = df_images['ID'].astype(str)

createCategoryDict(categories)

df['Categoria'] = df.apply(
    lambda row: getCategoryFromFamily(row["Familia"]), axis=1)

df['Margen'] = df.apply(
    lambda row: getMarginForSubfamily(row[["Familia", "Subfamilia"]]), axis=1)


df["PrecioConMar"] = df.apply(lambda row: calculatePrice(
    row["Margen"], row["PVD (Sin IVA) con Canon"]), axis=1)

df = df[df.Categoria != 'none']

df_images = df_images[['ID', 'Imagen1', 'Imagen2',
                       'Imagen3', 'Imagen4', 'Imagen5']]

df = df.merge(df_images, left_on='ID Articulo', right_on='ID', how='left')


df['Atributos'].apply(lambda x: createAttrDict(x))

for key in attrDict:
    if key != "nan":
        df['Att_'+str(key)] = ""

df = df.apply(lambda row: placeAttributes(row), axis=1)

df.to_csv('inventario_gen.csv',  quoting=1,
          quotechar='"', sep=";", encoding='iso-8859-1', decimal=',', float_format='%.3f')
