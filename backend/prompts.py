def prompt_reconstruction(ocr_text):
    return f"""
Tu es un PROFESSEUR expérimenté.

Le texte suivant provient :
- d’une photo de cours
- écriture manuscrite OU tapée
- avec fautes OCR possibles

TA MISSION (TRÈS IMPORTANTE) :
1. Corriger UNIQUEMENT les erreurs évidentes
2. Reconstituer le cours TEL QU’IL EST
3. NE RIEN INVENTER
4. Garder le niveau scolaire d’origine
5. Respecter les termes scientifiques exacts
6. Structurer légèrement (paragraphes, titres si évidents)

⚠️ Si une phrase est ambiguë → garde la version la plus probable
⚠️ Ne complète JAMAIS un cours incomplet

Texte OCR :
<<<
{ocr_text}
>>>

Rends UNIQUEMENT le cours reconstruit.
"""

def prompt_fiche(cours):
    return f"""
Transforme ce cours en FICHE DE RÉVISION PÉDAGOGIQUE.

RÈGLES STRICTES :
- Titres courts et clairs
- Listes à puces
- MOTS-CLÉS IMPORTANTS EN MAJUSCULES
- Définitions simples
- Niveau collège / lycée
- Aucune information inventée

Structure idéale :
I. Notions clés
II. Définitions
III. Points à retenir

Cours :
{cours}
"""

def prompt_qcm(cours):
    return f"""
Crée un QCM DE QUALITÉ à partir du cours.

CONTRAINTES :
- 10 questions
- 4 choix (A, B, C, D)
- UNE seule bonne réponse
- Indique la réponse correcte
- Questions variées (définition, compréhension, application)
- Niveau collège / lycée

FORMAT STRICT :
Q1. ...
A) ...
B) ...
C) ...
D) ...
Réponse : X

Cours :
{cours}
"""

def prompt_flashcards(cours):
    return f"""
Transforme ce cours en FLASHCARDS efficaces.

RÈGLES :
- Questions TRÈS COURTES
- Réponses CLÉS
- Une notion par carte
- Pas de phrases longues

FORMAT STRICT :
Question : ...
Réponse : ...

Cours :
{cours}
"""

def get_prompt(type_prompt, cours):
    if type_prompt == 'fiche':
        return prompt_fiche(cours)
    elif type_prompt == 'qcm':
        return prompt_qcm(cours)
    elif type_prompt == 'flashcards':
        return prompt_flashcards(cours)
    return "Type de prompt inconnu"
