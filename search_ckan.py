import requests

def search(mots_cles, ckan_url='https://dev.data.gouv.bj'):
    """
    Recherche des datasets en lien avec une liste de mots-clés sur une instance CKAN.

    Args:
        mots_cles (list[str]): Liste de mots-clés à rechercher.
        ckan_url (str): URL de base de l'instance CKAN (par défaut : https://dev.data.gouv.bj).

    Returns:
        list[dict]: Liste de dictionnaires contenant titre, description, url de chaque dataset.

    """


    api_search = f"{ckan_url}/api/3/action/package_search"
    datasets_trouves = {}

     

    for mot in mots_cles:
        try:
            params = {'q': mot, 'rows': 100}
            response = requests.get(api_search, params=params)
            data = response.json()

            if data.get('success'):
                for ds in data['result']['results']:
                    datasets_trouves[ds['id']] = {
                        'title': ds.get('title') or ds.get('name'),
                        'description': ds.get('notes', 'Pas de description'),
                        'url': f"{ckan_url}/dataset/{ds['name']}"
                    }
        except Exception as e:
            print(f"Erreur lors de la recherche avec le mot-clé '{mot}' : {e}")


    return list(datasets_trouves.values())



#print(search(['agriculture', 'économie',]))

'''mots = ['aliments', 'faim']
resultats = search(mots)

for dataset in resultats:
    print(f"Titre       : {dataset['title']}")
    print(f"Description : {dataset['description'][:200]}...")
    print(f"Lien        : {dataset['url']}")
    print("-" * 80)'''
