from ics import Calendar
import requests

# Télécharger le fichier .ics
url = 'https://ec.europa.eu/info/funding-tenders/opportunities/data/referenceData/grantTenders.ics'
response = requests.get(url)
response.raise_for_status()

# Charger le contenu du fichier .ics
calendar = Calendar(response.text)

# Liste des mots-clés correspondant aux domaines de recherche de Femto-ST
keywords = [
    "photonics", "nano", "quantum", "artificial intelligence", "robotics",
    "embedded systems", "renewable energy", "hydrogen", "IoT", "sensors", 
    "actuators", "smart materials", "bioengineering", "medical devices", 
    "mems", "nanomaterials", "energy harvesting", "intelligent systems", 
    "high performance computing", "machine learning", "data science", 
    "telecommunications", "6G", "cognitive networks", "sustainable development"
]

# Filtrer les appels en fonction des mots-clés
filtered_calls = []

for event in calendar.events:
    description = (event.description or "").lower()  # Description de l'appel
    summary = (event.name or "").lower()  # Nom de l'appel (SUMMARY)

    # Vérifier si un mot-clé est mentionné dans la description ou le nom de l'appel
    if any(keyword in description or keyword in summary for keyword in keywords):
        link = None
        if "https://" in (event.description or ""):
            link_start = event.description.find("https://")
            link_end = event.description.find(" ", link_start)
            link = event.description[link_start:link_end if link_end != -1 else None]

        call_info = {
            "Nom de l'appel": event.name,
            "Date d'ouverture": event.begin.format('DD/MM/YYYY'),
            "Date limite": event.end.format('DD/MM/YYYY') if event.end else "Non spécifiée",
            "Lien": link or "Non spécifié",
            "UID": event.uid,
        }
        filtered_calls.append(call_info)

# Afficher les résultats
if filtered_calls:
    for call in filtered_calls:
        print(f"Nom de l'appel : {call['Nom de l\'appel']}")
        print(f"Date d'ouverture : {call['Date d\'ouverture']}")
        print(f"Date limite : {call['Date limite']}")
        print(f"Lien : {call['Lien']}")
        print(f"UID : {call['UID']}")
        print("-" * 40)
else:
    print("Aucun appel trouvé pour les mots-clés recherchés.")
