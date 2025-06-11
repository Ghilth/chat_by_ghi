# main.py
import time
from generate_key_words import generate_key_words
from search_ckan import search

def get_datasets_response(user_input: str) -> dict:
    """
    Prend une requête utilisateur et renvoie un dict de la forme :
    {
      "status": "ok"|"hors_sujet"|"error",
      "message": str,           # en cas d'erreur ou hors_sujet
      "keywords": list[str],    # mots-clés utilisés (si status == ok)
      "datasets": list[dict]    # liste des datasets (si status == ok)
    }
    """
    if not user_input or not user_input.strip():
        return {"status": "error", "message": "Requête vide."}

    # 1) Génération des mots-clés
    try:
        result = generate_key_words(user_input)
    except Exception as e:
        return {"status": "error", "message": "Problème de connexion, veuillez réessayez ultérieurement"}

    # 2) Hors sujet
    if result["status"] != "ok":
        return {
            "status": "hors_sujet",
            "message": result.get("message", "Requête non liée aux datasets.")}
                                                                                                                                                                                                                                                                                                                                                                              
 # 3) Recherche CKAN
    try:
        datasets = search(result["keywords"])
    except Exception as e:
        return {"status": "error", "message": f"Erreur CKAN : {e}"}

    # 4) OK
    return {
        "status": "ok",
        "keywords": result["keywords"],
        "datasets": datasets
    }

                                                                                                                                                                                            

# Si tu veux toujours un script CLI pour tester :
if __name__ == "__main__":
    import json
    user_input = input("Entrez votre requête : ")
    response = get_datasets_response(user_input)
    print(json.dumps(response, ensure_ascii=False, indent=2))
