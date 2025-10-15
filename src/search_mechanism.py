"""
Mecanismo de busca para dados na base
Requisitos:
    - Buscas simples (pelo menos um termo existente)
    - Or (satisfazer pelo menos uma condição)
    - And (satisfazer ambas as condições)
"""

import json
from consts import SearchParams
from collections import Counter

def load_json_data(path_file):
    with open(path_file, "r", encoding="utf-8") as file:
        return json.load(file)
    
def find_terms(tec, env):
    year_ocurrencies = load_json_data("src/terms-by-year-complete.json")
    founded_articles = {}

    for year, articles in year_ocurrencies.items():
        for id, article in articles.items():
            env_params = [k for k, v in article["env"].items() if v > 0 and k in env]
            tec_params = [k for k, v in article["tec"].items() if v > 0 and k in tec]

            if (len(env_params) != 0) and (len(tec_params) != 0):
                if not founded_articles.get(year):
                    founded_articles[year] = {}

                founded_articles[year][id] = [*tec_params, *env_params]

    return founded_articles
    

def find_complete_articles(tec, env):
    articles = find_terms(tec, env)
    complete_data = load_json_data("src/complete-unique-results-scopus.json")
    r = {}
    for year, art_ in articles.items():

        if not r.get(year):
            r[year] = {}

        for id, search_terms in art_.items():
            article = complete_data.get(id)
            r[year][id] = {
                "title": article.get("title"),
                "abstract": article.get("abstract"),
                "url": article.get("url"),
                "terms_founded": search_terms
            }

    return r


def year_term_tuples():
    """Tuples containing the combinations of technology and environment keywords grouped by year"""

    year_ocurencies = load_json_data("src/terms-by-year-complete.json")
    year_term_set = {}

    for year, articles in year_ocurencies.items():
        existing_terms = []
        for _, article in articles.items():
            internal = []

            for field_type in ["tec", "env"]:
                field_terms = sorted([k for k, v in article[field_type].items() if v > 0])

                internal.append(tuple(field_terms))

            existing_terms.append(internal)

        year_term_set[year] = dict(Counter(tuple(t) for t in existing_terms))

    return year_term_set


def find_terms_in_tuples(tec, env, years=[]):
    year_tuples = year_term_tuples()
    result = {}

    if len(years) > 0:
        available_years = years

    else:
        available_years = list(year_tuples.keys())

    for year, ts in year_tuples.items():
        if year not in available_years:
            continue

        for _tuple, count in ts.items():
            concat_terms = []
            for _t in _tuple:
                for t in _t:
                    concat_terms.append(t)

            tec_terms = [t for t in concat_terms if t in tec]
            env_terms = [t for t in concat_terms if t in env]

            if (len(tec_terms) > 0) and (len(env_terms) > 0):
                if result.get(_tuple):
                   result[_tuple] += count

                else:
                   result[_tuple] = count
    return result


def especific_tuple_by_terms(tec, env, years=[]):
    nested_tuple = tuple(
        tuple(sorted(t)) for t in [tec, env]
    )
    terms_tuples = find_terms_in_tuples(tec, env, years)

    c = 0
    for _tuple, count in terms_tuples.items():
        if _tuple == nested_tuple:
            c += count

    return {
        nested_tuple: c
    }
