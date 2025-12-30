import requests, os

def extract_text(file):
    res = requests.post(
        "https://api.ocr.space/parse/image",
        files={"file": file},
        data={"apikey": os.getenv("OCR_API_KEY")}
    )
    return res.json()["ParsedResults"][0]["ParsedText"]
