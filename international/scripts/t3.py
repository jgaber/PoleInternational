from ics import Calendar
import requests

def fetch_project_calls():
    # Télécharger le fichier .ics
    url = 'https://ec.europa.eu/info/funding-tenders/opportunities/data/referenceData/grantTenders.ics'
    response = requests.get(url)
    response.raise_for_status()  # Vérifie si la requête a réussi

    # Charger le contenu du fichier .ics
    calendar = Calendar(response.text)

    # Filtrer les appels du programme HORIZON
    horizon_programs = []

    for event in calendar.events:
        description = (event.description or "").lower()  # Description de l'appel
        summary = (event.name or "").lower()  # Nom de l'appel (SUMMARY)
        if "horizon" in description or "horizon" in summary:  # Vérifier si "HORIZON" est mentionné
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
            horizon_programs.append(call_info)

    return horizon_programs
