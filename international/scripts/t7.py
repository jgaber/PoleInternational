from icalendar import Calendar
import requests

# Télécharger le fichier ICS depuis l'URL
def download_ics(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

# Analyser le fichier ICS et filtrer les appels de projet
def find_matching_calls(ics_data, programs, keywords):
    gcal = Calendar.from_ical(ics_data)
    matching_calls = []

    for component in gcal.walk():
        if component.name == "VEVENT":
            summary = str(component.get('SUMMARY', ''))
            description = str(component.get('DESCRIPTION', ''))

            # Filtrage des mots-clés dans la description ou le résumé
            matched_keywords = []
            for keyword in keywords:
                if keyword.lower() in summary.lower() or keyword.lower() in description.lower():
                    matched_keywords.append(keyword)

            # Filtrer par programmes (ex: "Horizon", "ERC", etc.)
            matched_programs = []
            for program, program_keywords in programs.items():
                if any(keyword.lower() in summary.lower() or keyword.lower() in description.lower() for keyword in program_keywords):
                    matched_programs.append(program)

            # Ajouter les appels qui correspondent aux programmes ou mots-clés
            if matched_programs or matched_keywords:
                matching_calls.append({
                    'summary': summary,
                    'description': description,
                    'programs': matched_programs,
                    'keywords': matched_keywords
                })

    return matching_calls

# Fonction principale pour récupérer les appels de projet avec les paramètres
def fetch_project_calls(programme=None, keywords_filter=None):
    # Liste des programmes avec des mots-clés associés
    program_keywords = {
        'Horizon': ['research', 'innovation', 'technology'],
        'Green Deal': ['energy', 'climate', 'sustainable', 'green'],
        'ERC': ['fundamental research', 'science', 'research council'],
        'MSCA': ['mobility', 'research', 'fellowships'],
        'EIT': ['innovation', 'technology', 'entrepreneurship'],
        'EU Innovation Fund': ['energy', 'climate', 'sustainability'],
        'ESA': ['space', 'exploration', 'satellites'],
        'COST': ['science', 'collaboration', 'research'],
        'LIFE': ['environment', 'climate', 'nature'],
        'EU4Health': ['health', 'well-being'],
        'Digital Europe Programme': ['digital', 'transformation', 'technology'],
        'Interreg': ['cooperation', 'cross-border', 'territory'],
        'SME Instrument': ['innovation', 'SMEs', 'startups'],
        'Erasmus+': ['education', 'mobility', 'students'],
        'Erasmus Mundus': ['higher education', 'global', 'international'],
        'InvestEU': ['investment', 'finance'],
        'ESF': ['social inclusion', 'employment', 'equality'],
        'Cohesion Fund': ['economic cohesion', 'regions'],
        'Eureka': ['innovation', 'collaboration', 'R&D'],
        'Eurostars': ['innovation', 'R&D', 'startups'],
        'EU-ASEAN': ['cooperation', 'international', 'Asia'],
    }

    # Si des filtres sont appliqués par l'utilisateur
    if not programme:
        programme = ""  # Par défaut, ne pas filtrer par programme
    if not keywords_filter:
        keywords_filter = []  # Par défaut, ne pas filtrer par mots-clés

    # Récupérer le fichier ICS
    ics_url = 'https://ec.europa.eu/info/funding-tenders/opportunities/data/referenceData/grantTenders.ics'
    ics_data = download_ics(ics_url)

    # Filtrer les appels de projet en fonction des programmes et mots-clés
    matching_calls = find_matching_calls(ics_data, program_keywords, keywords_filter)

    return matching_calls
