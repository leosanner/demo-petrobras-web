class SearchParams:
    def __init__(self):
        self.tec = search_keywords["technologies"]
        self.environment = search_keywords["environment"]
        self.tec_var = variations["tec"]
        self.env_var = variations["environment"]

repo_endpoints = {
    'sciencedirect': 'https://www.sciencedirect.com/search',
    'elsevier': 'https://api.elsevier.com/content/search/scopus'
}

environment = [
    "Impact Assessment",
    "Environmental Impact Assessment",
    "Environmental Licensing",
    "Environmental Monitoring",
    "Environmental Big Data",
    "Environmental Modeling",
    "Environmental Internet of Things",
    "Digital Environmental Governance",
    "Digital EIA",
    "Strategic Environmental Assessment",
    "Social Impact Assessment",
    "ESG Risk Management",
]

technologies = [
    "Internet of Things",
    "Machine Learning",
    "Deep Learning",
    "Geoprocessing",
    "Remote Sensing",
    "Technological Innovation",
    "Digital Technologies",
    "Artificial Intelligence",
    "Data Science",
    "Digital Transformation",
    "Reinforcement Learning",
    "Data Visualization",
    "Natural Language Processing",
    "Prediction Analytics",
    "Digital Twins",
    "Augmented Reality",
]

search_keywords = {
    "environment": environment,
    "technologies": technologies
}

tec_vars = [
    "Digital Twin",
    "Digital Technology",
    "Internet of Thing",
    ]

env_vars = [
    "Environment IoT",
    "Environments IoT",
    "Impacts Assessment",
    "Environmental Modelling",
]


variations = {
    "environment": env_vars,
    "tec": tec_vars
}