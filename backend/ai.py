from flask import Blueprint, request, jsonify, session
from backend.prompts import get_prompt
from openai import OpenAI
import os

ai_bp = Blueprint('ai', __name__)
client = OpenAI(
    api_key=os.getenv('GROQ_API_KEY'),
    base_url="https://api.groq.com/openai/v1"
)

@ai_bp.before_request
def check_auth():
    if 'user_id' not in session:
        return jsonify({'error': 'Non autorisé'}), 401
    pass

@ai_bp.route('/fiche', methods=['POST'])
def fiche():
    data = request.get_json()
    password = data.get('password', '')
    if password != os.getenv('PASSWORD'):  # Utilise la variable d'env
        return jsonify({'error': 'Mot de passe incorrect'}), 401
    cours = data.get('cours', '')
    prompt = get_prompt('fiche', cours)
    response = client.chat.completions.create(
        model='llama3-70b-8192',
        messages=[{'role': 'user', 'content': prompt}],
        max_tokens=1000
    )
    result = response.choices[0].message.content.strip()
    return jsonify({'result': result})

@ai_bp.route('/qcm', methods=['POST'])
def qcm():
    data = request.get_json()
    password = data.get('password', '')
    if password != os.getenv('PASSWORD'):
        return jsonify({'error': 'Mot de passe incorrect'}), 401
    cours = data.get('cours', '')
    prompt = get_prompt('qcm', cours)
    response = client.chat.completions.create(
        model='llama3-70b-8192',
        messages=[{'role': 'user', 'content': prompt}],
        max_tokens=1000
    )
    result = response.choices[0].message.content.strip()
    return jsonify({'result': result})

@ai_bp.route('/flashcards', methods=['POST'])
def flashcards():
    data = request.get_json()
    password = data.get('password', '')
    if password != os.getenv('PASSWORD'):
        return jsonify({'error': 'Mot de passe incorrect'}), 401
    cours = data.get('cours', '')
    prompt = get_prompt('flashcards', cours)
    response = client.chat.completions.create(
        model='llama3-70b-8192',
        messages=[{'role': 'user', 'content': prompt}],
        max_tokens=1000
    )
    result = response.choices[0].message.content.strip()
    return jsonify({'result': result})