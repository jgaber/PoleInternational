from ics import Calendar
import requests

# Télécharger le fichier .ics
url = 'https://ec.europa.eu/info/funding-tenders/opportunities/data/referenceData/grantTenders.ics'
response = requests.get(url)
response.raise_for_status()

# Charger le contenu du fichier .ics
calendar = Calendar(response.text)
def fetch_project_calls(programme=None, keywords_filter=None):
    filtered_calls = []
    
    # Vérification des événements dans le calendrier
    if not calendar.events:
        print("Aucun événement trouvé dans le calendrier.")  # Débogage pour vérifier les événements

    for event in calendar.events:
        description = (event.description or "").lower()  # Description de l'appel
        summary = (event.name or "").lower()  # Nom de l'appel (SUMMARY)
        
        # Debug: Afficher l'événement pour vérifier son contenu
        print(f"Event: {event.name}, Description: {event.description}")

        # Vérifier si un programme est spécifié et filtrer par programme
        if programme and programme.lower() not in summary:
            continue
        
        # Vérifier les mots-clés
        if keywords_filter:
            if not any(keyword.lower() in description or keyword.lower() in summary for keyword in keywords_filter):
                continue
        
        # Définir la variable `link` avant d'entrer dans la condition
        link = "Non spécifié"  # Valeur par défaut pour le lien

        # Vérifier si un lien est présent dans la description
        if "https://" in (event.description or ""):
            link_start = event.description.find("https://")
            link_end = event.description.find(" ", link_start)
            link = event.description[link_start:link_end if link_end != -1 else None]

        call_info = {
            "nom_de_lappel": event.name,
            "date_ouverture": event.begin.format('DD/MM/YYYY'),
            "date_limite": event.end.format('DD/MM/YYYY') if event.end else "Non spécifiée",
            "lien": link or "Non spécifié",
            "uid": event.uid,
        }
       
        # Debug: Afficher les informations du call pour vérifier les données
        print(f"Call info: {call_info}")
        
        filtered_calls.append(call_info)

    if not filtered_calls:
        print("Aucun appel de projet trouvé après filtrage.")

    return filtered_calls
