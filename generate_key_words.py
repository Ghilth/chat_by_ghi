from mistralai import Mistral
import os
import re


def call_mistral(messages: list[dict], temperature: float = 0.3) -> str:
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise EnvironmentError("La variable d'environnement MISTRAL_API_KEY est manquante.")

    client = Mistral(api_key=api_key)
    try:
        response = client.chat.complete(
            model="mistral-large-latest",
            messages=messages,
            temperature=temperature  # ← ici on fixe la température
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise RuntimeError(f"Erreur lors de l'appel à Mistral : {e}")

    

def extract_keywords_from_response(text: str) -> list[str]:
    segments = re.split(r'[;\n]+', text)
    keywords = []

    for segment in segments:
        segment = segment.strip()
        # 1) Format “clé : a, b, c”
        if ':' in segment:
            _, vals = segment.split(':', 1)
            for kw in vals.split(','):
                clean = kw.strip().lower()
                clean = re.sub(r'[\*\.\s]+$', '', clean)
                if clean:
                    keywords.append(clean)
            continue

        # 2) Liste numérotée “1. mot-clé”
        m = re.match(r'^\d+\.\s*(.+)$', segment)
        if m:
            clean = m.group(1).strip().lower()
            clean = re.sub(r'[\*\.\s]+$', '', clean)
            if clean:
                keywords.append(clean)

    # 3) Déduplication
    seen = set()
    final = []
    for kw in keywords:
        if kw not in seen:
            seen.add(kw)
            final.append(kw)
    return final



def generate_key_words(user_input: str) -> dict:
    """
    Prend une phrase utilisateur en entrée, interagit avec le LLM,
    et retourne :
    - status: "ok" si des mots-clés sont extraits, sinon "hors_sujet"
    - keywords: liste de mots-clés ou message de recadrage
    """
    system_prompt = (
        """Tu es un Afiavi, assistant spécialisé pour aider les utilisateurs à trouver des datasets sur la plateforme opendata du Bénin.
        Garde toujours le focus sur cette tâche. Si l'utilisateur pose,une question hors sujet, recadre-le poliment. Lorsque la demande
        concerne des données, génère une liste de mots-clés en français et en anglais."""
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]


    response_text = call_mistral(messages)
    keywords = extract_keywords_from_response(response_text)

    if keywords:
        return {"status": "ok", "keywords": keywords}
    else:
        return {"status": "hors_sujet", "message": response_text}




#print(generate_key_words("Données eau"))

