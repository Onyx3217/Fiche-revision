import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

API_URL = "https://api.groq.com/openai/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

@app.route("/")
def home():
    return "HelpUs API en ligne ✅"

@app.route("/fiche", methods=["POST"])
def generer_fiche():
    data = request.get_json()
    cours = data.get("cours", "")

    if not cours.strip():
        return jsonify({"error": "Cours manquant"}), 400

    prompt = f"""
Tu es un assistant pédagogique.

Transforme le texte suivant en une FICHE DE RÉVISION CLAIRE et STRUCTURÉE,
quel que soit le sujet (histoire, langues, sciences, etc.).

Contraintes :
- Titres courts
- Listes à puces
- Phrases simples
- MOTS IMPORTANTS en MAJUSCULES
- Pas de blabla inutile

Structure :

📌 Idées essentielles
📌 Notions importantes
📌 Points clés à retenir
📌 Questions de révision (5 à 8 avec réponses)

Texte :
{cours}
"""

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.4,
        "max_tokens": 700
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload)
    result = response.json()

    fiche = result["choices"][0]["message"]["content"]
    return jsonify({"fiche": fiche})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
