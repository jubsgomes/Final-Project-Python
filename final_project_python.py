import csv

def load_translations(filepath):
    translations = {}
    try:
        translation_file = open(filepath, encoding="utf-8")
    except:
        print("Warning: Translation file '" + filepath + "' was not found.")
        print("The program will display data in French.")
        return translations

    for line in translation_file:
        line = line.strip()
        if line == "" or line.startswith("#"):
            continue
        if "=" in line:
            parts = line.split("=")
            french = parts[0].strip()
            english = parts[1].strip()
            translations[french] = english

    translation_file.close()
    return translations


def translate_value(value, translations):
    if value is None or value == "":
        return value
    value = str(value).strip()

    if ";" in value:
        parts = value.split(";")
        translated_parts = []
        for part in parts:
            part = part.strip()
            translated_parts.append(translations.get(part, part))
        return "; ".join(translated_parts)

    return translations.get(value, value)


def clean_cell(value): # This function cleans cell values if they are empty (None) or contain only spaces, and remove surrounding spaces when they're not empty
    if value is None:
        return None

    value = value.strip()

    if value == "":
        return None

    return value


def load_artists(filepath, translations):
    artists_list = []
    csv_file = open(filepath, encoding="utf-8-sig", newline="") # encoding="utf-8-sig" is here to handle an invisible BOM character that some programs add at the start of CSV files
    reader = csv.DictReader(csv_file) # csv.DictReader maps each row to a dictionary, using the first row as keys, so we just need to pick out the fields we need.

    for row in reader:

        artist = {
            "id": clean_cell(row["id"]),
            "nom": clean_cell(row["nom"]),
            "prenom": clean_cell(row["prenom"]),
            "genre": clean_cell(row["genre"]),
            "nationalites": clean_cell(row["nationalites"]),
            "anneeNaissance": clean_cell(row["anneeNaissance"]),
            "anneeDeces": clean_cell(row["anneeDeces"]),
            "peuplesAutochtones": clean_cell(row["peuplesAutochtones"])
        }

        artist["genre"] = translate_value(artist["genre"], translations)
        artist["nationalites"] = translate_value(artist["nationalites"], translations)
        artist["peuplesAutochtones"] = translate_value(artist["peuplesAutochtones"], translations)

        artists_list.append(artist)

    csv_file.close()
    return artists_list


def load_artworks(filepath, translations):
    artworks_list = []
    csv_file = open(filepath, encoding="utf-8-sig", newline="")
    reader = csv.DictReader(csv_file)

    for row in reader:
        artwork = {
            "artistesId": clean_cell(row["artistesId"]),
            "artistes": clean_cell(row["artistes"]),
            "titre": clean_cell(row["titre"]),
            "dateProduction": clean_cell(row["dateProduction"]),
            "lieuProduction": clean_cell(row["lieuProduction"]),
            "categorie": clean_cell(row["categorie"]),
            "departement": clean_cell(row["departement"])
        }

        artwork["categorie"] = translate_value(artwork["categorie"], translations)
        artwork["departement"] = translate_value(artwork["departement"], translations)

        artworks_list.append(artwork)

    csv_file.close()
    return artworks_list


translations  = load_translations("translations.txt")
artists = load_artists("artistes-mac.csv", translations)
artworks = load_artworks("oeuvres-mac.csv", translations)
public_domain = load_artworks("oeuvres-mac-domaine-public-canada.csv", translations)
