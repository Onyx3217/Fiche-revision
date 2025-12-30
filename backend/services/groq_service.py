import requests, os

def generate(text, mode):
    prompt = f"Génère un {mode} clair et structuré à partir du texte suivant :\n{text}"

    res = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.1-70b-versatile",
            "messages": [{"role": "user", "content": prompt}]
        }
    )

    return res.json()["choices"][0]["message"]["content"]
