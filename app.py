import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

app = Flask(__name__)
CORS(app)

# 🔑 Clé API Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

API_URL = "https://api.groq.com/openai/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

print("GROQ_API_KEY chargée :", GROQ_API_KEY is not None)


@app.route("/fiche", methods=["POST"])
def generer_fiche():
    data = request.get_json()
    cours = data.get("cours", "")

    if not cours.strip():
        return jsonify({"error": "Cours manquant"}), 400

    # 🧠 Prompt optimisé pour fiche de révision
    prompt = f"""
Tu es un assistant pédagogique.

Transforme le texte suivant en une FICHE DE RÉVISION CLAIRE et STRUCTURÉE,
quel que soit le sujet (histoire, langues, sciences, etc.).

Contraintes OBLIGATOIRES :
- Utilise des TITRES courts
- Utilise surtout des LISTES À PUCE
- Explique avec des PHRASES SIMPLES
- Mets les MOTS IMPORTANTS en majuscules
- Pas de texte inutile

Structure OBLIGATOIRE :

📌 Idées essentielles
- ...

📌 Notions / concepts importants
- ...

📌 Points clés à retenir
- ...

📌 Questions de révision
- 5 à 8 questions courtes avec leurs réponses

Texte à transformer :
{cours}
"""

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.4,
        "max_tokens": 700
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        print("GROQ status :", response.status_code)
        print("GROQ réponse :", response.text)

        response.raise_for_status()
        result = response.json()

        fiche = result["choices"][0]["message"]["content"]
        return jsonify({"fiche": fiche})

    except Exception as e:
        return jsonify({
            "error": "Erreur API Groq",
            "details": str(e),
            "api_response": getattr(e.response, "text", None)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
