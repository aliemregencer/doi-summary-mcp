import requests
import os
import fitz  # PyMuPDF
from dotenv import load_dotenv

load_dotenv()

# OpenAI API Key
API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

def get_article_text(doi: str) -> str:
    """
    DOI üzerinden başlık ve abstract çeker.
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

def get_pdf_url_from_unpaywall(doi: str, email: str) -> str:
    """
    Unpaywall üzerinden açık erişimli PDF linki alır.
    """
    url = f"https://api.unpaywall.org/v2/{doi}?email={email}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        oa_location = data.get("best_oa_location")
        if oa_location and oa_location.get("url_for_pdf"):
            return oa_location["url_for_pdf"]
    return None

def extract_text_from_pdf_url(pdf_url: str) -> str:
    """
    PDF URL'sinden indirilen dosyadan metin çıkarır.
    """
    response = requests.get(pdf_url)
    with open("temp.pdf", "wb") as f:
        f.write(response.content)

    text = ""
    doc = fitz.open("temp.pdf")
    for page in doc:
        text += page.get_text()
    doc.close()

    return text.strip()

def extract_text_from_uploaded_pdf(file_path: str) -> str:
    """
    Kullanıcının yüklediği PDF dosyasından metin çıkarır.
    """
    text = ""
    doc = fitz.open(file_path)
    for page in doc:
        text += page.get_text()
    doc.close()
    return text.strip()

def summarize_text(text: str) -> str:
    """
    OpenAI ile metni özetler.
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
            {"role": "user", "content": f"Şu metni akademik bir dille kısa ve öz şekilde özetle:\n\n{text}"}
        ]
    }

    response = requests.post(endpoint, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        return f"OpenAI Hatası: {response.status_code}\n{response.text}"
