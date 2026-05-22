from django import forms

class ResearchCallForm(forms.Form):
    PROGRAMMES = [
        ('', '--- Sélectionner un programme ---'),
        ('Horizon', 'Horizon'),
        ('ERC-', 'European Research Council (ERC)'),
        ('MSCA', 'Marie Sklodowska-Curie Actions'),
        ('EIT', 'European Institute of Innovation and Technology (EIT)'),
        ('EU Innovation Fund', 'EU Innovation Fund'),
        ('ESA', 'European Space Agency (ESA)'),
        ('COST', 'COST (European Cooperation in Science and Technology)'),
        ('CEF', 'Connecting Europe Facility (CEF)'),
        ('LIFE', 'LIFE Programme'),
        ('EU4Health', 'EU4Health'),
        ('Digital', 'Digital Europe Programme'),
        ('Interreg', 'Interreg'),
        ('SMEs', 'SMEs Instrument'),
        ('Erasmus', 'Erasmus+'),
        ('Erasmus', 'Erasmus Mundus'),
        ('InvestEU', 'InvestEU'),
        ('ESF', 'European Social Fund (ESF)'),
        ('Cohesion', 'Cohesion Fund'),
        ('Eureka', 'Eureka'),
        ('Eurostars', 'Eurostars'),
        ('EU-ASEAN', 'EU-ASEAN Collaboration Programme'),
    ]
    
    KEYWORDS = [
        ('', '--- Sélectionner un ou plusieurs mots-clés ---'),
        ('Bio', 'Bio'),
        ('Biological', 'Biological'),
        ('Chemical', 'Chemical'),
        ('Communication', 'Communications'),
        ('Device', 'Devices'),
        ('Energy', 'Energy'),
        ('Green', 'Green'),
        ('HPC', 'High Performance Computing (HPC)'),
        ('Hydrogen', 'Hydrogen'),
        ('Internet of Things', 'IoT (Internet of Things)'),
        ('Innovation', 'Innovation'),
        ('Logistic', 'Logistic'),
        ('Materials', 'Materials'),
        ('Medical', 'Medical'),
        ('Micro', 'Micro Technologies'),
        ('Nano', 'Nano Technologies'),
        ('Nanoelectronics', 'Nanoelectronics'),
        ('Network', 'Networks'),
        ('Quantum', 'Quantum'),
        ('Robotics', 'Robotics'),
        ('Renewable', 'Renewable'),
        ('Security', 'Security'),
        ('Smart', 'Smart'),
        ('Sustainable', 'Sustainable'),
        ('System', 'System'),
        ('Threat', 'Threats'),
        ('Transport', 'Transport'),
        ('Radiological', 'Radiological'),
]

    # Recherche textuelle
    search_query = forms.CharField(
        required=False, 
        label="Search Engine",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search by keyword, title, description...'})
    )

    # Programme de financement
    programme = forms.ChoiceField(choices=PROGRAMMES, required=False, label="Programme", widget=forms.Select(attrs={'class': 'form-control'}))
    
    # Domaines (Mots-clés)
    keywords = forms.MultipleChoiceField(
        choices=KEYWORDS, 
        required=False, 
        label="Domains",
        widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '8'})
    )
