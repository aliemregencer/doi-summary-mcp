import requests
import os
from dotenv import load_dotenv

load_dotenv()  # .env dosyasını yükle

# OpenAI API Key ortam değişkeninden al
API_KEY = os.getenv("OPENAI_API_KEY")

def get_article_text(doi: str) -> str:
    """
    DOI üzerinden makale bilgisi çeker (başlık ve özet varsa).
    """
    headers = {
        "Accept": "application/vnd.citationstyles.csl+json"
    }
    url = f"https://doi.org/{doi}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        title = data.get("title", "")
        abstract = data.get("abstract", "")
        if abstract:
            return f"Title: {title}\nAbstract: {abstract}"
        else:
            return f"Title: {title}\nNo abstract found."
    else:
        return "Makale bulunamadı veya erişilemedi."

def summarize_text(text: str) -> str:
    """
    OpenAI API kullanarak metni özetler.
    """
    endpoint = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are an academic assistant."},
            {"role": "user", "content": f"Şu metni akademik ve öz şekilde özetle:\n\n{text}"}
        ]
    }

    response = requests.post(endpoint, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        return f"OpenAI Hatası: {response.status_code}\n{response.text}"
    
def get_pdf_url_from_unpaywall(doi: str, email: str) -> str:
    """
    Unpaywall üzerinden DOI için varsa açık erişim PDF URL'sini getirir.
    """
    url = f"https://api.unpaywall.org/v2/{doi}?email={email}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            location = data.get("best_oa_location", {})
            pdf_url = location.get("url_for_pdf")
            return pdf_url  # None olabilir
        else:
            return None
    except Exception as e:
        return None

