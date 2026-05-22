import spacy
from icalendar import Calendar
import requests

# Charger le modèle linguistique de spaCy pour l'anglais
nlp = spacy.load("en_core_web_sm")  # Utilisation d'un modèle plus léger

# Télécharger le fichier ICS depuis l'URL
def download_ics(url):
    response = requests.get(url)
    response.raise_for_status()  # Vérifie si la requête a réussi
    return response.text

# Fonction pour vérifier la similarité sémantique entre un programme et le résumé ou la description
def get_similarity(program, text):
    if not text:  # Si le texte est vide, retourner une similarité de 0
        return 0
    program_doc = nlp(program)
    text_doc = nlp(str(text))  # Convertir en str pour s'assurer que c'est du texte
    return program_doc.similarity(text_doc)

# Filtrer les appels en fonction de la similarité sémantique avec les programmes
def match_programs_by_similarity(summary, description, programs):
    matched_programs = []
    
    # Vérifier la similarité avec chaque programme
    for program, keywords in programs.items():
        similarity_summary = get_similarity(program, summary)
        similarity_description = get_similarity(program, description)

        if similarity_summary > 0.6 or similarity_description > 0.6:
            matched_programs.append(program)
    
    return matched_programs

# Analyser le fichier ICS et filtrer les appels de projet
def find_matching_calls(ics_data, programs, keywords):
    gcal = Calendar.from_ical(ics_data)
    matching_calls = []

    for component in gcal.walk():
        if component.name == "VEVENT":
            summary = str(component.get('SUMMARY', ''))
            description = str(component.get('DESCRIPTION', ''))

            # Vérification que le résumé et la description ne sont pas vides
            if not summary and not description:
                continue  # Ignore l'événement si les deux sont vides

            # Filtrer par programmes en utilisant la similarité NLP
            matched_programs = match_programs_by_similarity(summary, description, programs)

            # Filtrage des mots-clés dans la description ou le résumé
            matched_keywords = []
            for keyword in keywords:
                if keyword.lower() in summary.lower() or keyword.lower() in description.lower():
                    matched_keywords.append(keyword)

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
