import requests
from icalendar import Calendar

# Télécharger le fichier ICS depuis l'URL
url = 'https://ec.europa.eu/info/funding-tenders/opportunities/data/referenceData/grantTenders.ics'
response = requests.get(url)
response.raise_for_status()

# Charger le contenu du fichier ICS
calendar = Calendar.from_ical(response.text)

def fetch_project_calls(programme=None, keywords_filter=None, search_query=None):
    filtered_calls = []

    if not calendar.events:
        print("Aucun événement trouvé dans le calendrier.")

    for event in calendar.events:
        summary = (event.get('SUMMARY') or "").lower()
        description = (event.get('DESCRIPTION') or "").lower()
        link = (event.get('URL') or "").lower()
        
        full_text = f"{summary} {description} {link}"

        # Filtrage par programme
        if programme and programme.lower() not in full_text:
            continue

        # Filtrage par mots-clés (Domaines)
        if keywords_filter:
            # On enlève la chaîne vide si elle est présente
            active_keywords = [k for k in keywords_filter if k]
            if active_keywords:
                if not any(keyword.lower() in full_text for keyword in active_keywords):
                    continue

        # Filtrage par recherche textuelle
        if search_query:
            if search_query.lower() not in full_text:
                continue

        # Extraction du lien
        final_link = "Non spécifié"
        if "https://" in (event.get('DESCRIPTION') or ""):
            desc = event.get('DESCRIPTION')
            link_start = desc.find("https://")
            link_end = desc.find(" ", link_start)
            final_link = desc[link_start:link_end if link_end != -1 else None]
        elif event.get('URL'):
            final_link = event.get('URL')

        call_info = {
            "nom_de_lappel": event.get('SUMMARY') or "Sans titre",
            "date_ouverture": event.get('DTSTART').dt.strftime('%d/%m/%Y') if event.get('DTSTART') else "Non spécifiée",
            "date_limite": event.get('DTEND').dt.strftime('%d/%m/%Y') if event.get('DTEND') else "Non spécifiée",
            "lien": final_link,
            "uid": event.get('UID'),
        }

        filtered_calls.append(call_info)

    return filtered_calls
