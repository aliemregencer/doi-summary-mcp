from mcp.server.fastmcp import FastMCP
from app import (
    get_article_text,
    summarize_text,
    get_pdf_url_from_unpaywall,
    extract_text_from_pdf_url
)

mcp = FastMCP("doi-summary-mcp")

# Unpaywall için e-mail adresin
UNPAYWALL_EMAIL = "genceraliemre@gmail.com"

@mcp.tool()
async def summarize_doi(doi: str) -> str:
    """
    DOI girilerek makale özeti alınır.
    - Önce Unpaywall'dan PDF varsa indirip tam metinden özetler.
    - Yoksa başlık ve abstract'tan özet çıkarır.
    """
    try:
        # PDF varsa önce onu dene
        pdf_url = get_pdf_url_from_unpaywall(doi, UNPAYWALL_EMAIL)
        if pdf_url:
            try:
                full_text = extract_text_from_pdf_url(pdf_url)
                if not full_text.strip():
                    return "PDF bulundu ancak içerik çıkarılamadı."
                return summarize_text(full_text)
            except Exception as e:
                return f"PDF indirildi ancak işlenirken hata oluştu: {str(e)}"

        # PDF yoksa metadata fallback
        text = get_article_text(doi)
        if "bulunamadı" in text:
            return "Makale erişimi sağlanamadı."
        return summarize_text(text)

    except Exception as e:
        return f"Bir hata oluştu: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="stdio")
