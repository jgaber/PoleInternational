import json
import os
from pathlib import Path
import sys
from django.shortcuts import render
from django.http import HttpResponse
from .forms_UE import ResearchCallForm  # Importer le formulaire EU

# Ajouter le chemin du script
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))

from t8 import fetch_project_calls  # Importer la fonction depuis t5.py

def home(request):
    return render(request, 'international/index.html')

def about(request):
    return render(request, 'international/about.html')

def projects(request):
    # Récupérer les appels de projet
    calls = fetch_project_calls()  # Appel de la fonction dans t5.py ou t3.py
    return render(request, 'international/projects.html', {'calls': calls})

def contact(request):
    return render(request, 'international/contact.html')


def eu_form(request):
    if request.method == 'POST':
        form = ResearchCallForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            programme = form.cleaned_data['programme']
            keywords = form.cleaned_data['keywords']
            search_query = form.cleaned_data.get('search_query', '')
            
            # Filtrer avec le nouveau champ de recherche
            filtered_calls = fetch_project_calls(programme, keywords, search_query)
            
            return render(request, 'international/projects.html', {'calls': filtered_calls, 'form': form, 'programme': programme})
    else:
        form = ResearchCallForm()
        all_calls = fetch_project_calls()
        return render(request, 'international/eu-form.html', {'form': form, 'calls': all_calls})

# Données pour les pages d'information externes
EXTERNAL_LINKS_DATA = {
    'cost-actions': {
        'title': 'EU COST Actions',
        'description': 'COST (European Cooperation in Science and Technology) is a funding organisation for research and innovation networks. Our Actions help connect research initiatives across Europe and beyond and enable scientists to grow their ideas by sharing them with their peers. This boosts their research, career and innovation.',
        'url': 'https://www.cost.eu/'
    },
    'eu-funding-portal': {
        'title': 'EU Funding & Tenders Portal',
        'description': 'The Funding & Tenders Portal is the single entry point (the Single Electronic Data Interchange Area) for applicants, contractors and experts in funding programmes and tenders managed by the European Commission and other EU bodies.',
        'url': 'https://ec.europa.eu/info/funding-tenders/opportunities/portal/screen/home'
    },
    'cnrs-call': {
        'title': 'CNRS Call for Proposals',
        'description': 'The CNRS (Centre National de la Recherche Scientifique) periodically launches calls for proposals to support international research collaboration. These calls enable researchers to establish new partnerships and strengthen existing scientific ties on a global scale.',
        'url': 'https://international.cnrs.fr/en/campagne-cnrs/'
    },
    'cooperation-toolkit': {
        'title': 'International Cooperation Toolkit',
        'description': 'The International Cooperation Toolkit provided by CNRS offers a comprehensive set of resources and guidelines for researchers looking to develop international collaborative projects. It covers administrative, legal, and strategic aspects of global scientific partnership.',
        'url': 'https://international.cnrs.fr/en/cooperer-a-l-international/'
    },
    'anr-prci': {
        'title': 'ANR - PRCI',
        'description': 'The ANR (Agence Nationale de la Recherche) International Collaborative Research Projects (PRCI) facilitate cooperation between French research teams and their international counterparts. This programme supports high-quality scientific projects across all disciplines.',
        'url': 'https://www.appelsprojetsrecherche.fr/'
    },
    'campus-france': {
        'title': 'Campus France - PHC',
        'description': 'The Hubert Curien Partnerships (PHC) managed by Campus France are a cornerstone of French international scientific cooperation. They provide funding for the mobility of researchers involved in joint research projects between France and partner countries.',
        'url': 'https://www.campusfrance.org/fr/phc'
    },
    'agence-auf': {
        'title': 'Agence AUF',
        'description': 'The Agence Universitaire de la Francophonie (AUF) supports academic and research institutions in the French-speaking world. Their calls for candidates focus on strengthening linguistic and cultural diversity while promoting high-level scientific research.',
        'url': 'https://www.auf.org/nouvelles/appels-a-candidatures/?type%5B0%5D=3'
    },
    'scholarships': {
        'title': 'Scholarships',
        'description': 'Access information on a wide range of scholarships supported by the European Educational and Culture Executive Agency (EACEA). These opportunities support excellence in education and promote international mobility for students and academics.',
        'url': 'https://www.eacea.ec.europa.eu/scholarships_en'
    },
    'short-term-mobility': {
        'title': 'Short-term Mobility',
        'description': 'COST Actions offer networking tools including Short-Term Scientific Missions (STSM). These are institutional visits aimed at supporting individual mobility, strengthening existing networks, and fostering collaboration between researchers.',
        'url': 'https://www.cost.eu/cost-actions-event/action-networking-tools/'
    },
}

def external_link_info(request, link_slug):
    data = EXTERNAL_LINKS_DATA.get(link_slug)
    if not data:
        # Fallback or 404
        return HttpResponse("Information not found.", status=404)
    return render(request, 'international/external_info.html', {'data': data})

def horizon_pillars_view(request):
    json_path = Path(__file__).resolve().parent / "scripts" / "horizon_europe_pillars_clusters.json"
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return render(request, "international/horizon_pillars.html", {"pillars": data})