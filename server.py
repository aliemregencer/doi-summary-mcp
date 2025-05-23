from mcp.server.fastmcp import FastMCP
from app import (
    get_article_text,
    get_pdf_url_from_unpaywall,
    extract_text_from_pdf_url,
    summarize_text
)

mcp = FastMCP("doi-summary-mcp")

# Unpaywall için kullanılacak e-posta adresi (senin e-postanı yazabilirsin)
UNPAYWALL_EMAIL = "youremail@example.com"

@mcp.tool()
async def summarize_doi(doi: str) -> str:
    """
    DOI girilerek makale özeti alınır.
    Eğer açık erişimli PDF varsa onu kullanır.
    Yoksa başlık/abstract özetlenir.
    """
    try:
        pdf_url = get_pdf_url_from_unpaywall(doi, UNPAYWALL_EMAIL)
        if pdf_url:
            text = extract_text_from_pdf_url(pdf_url)
            if text:
                return summarize_text(text)

        # PDF bulunamazsa fallback: başlık ve abstract üzerinden özet
        meta = get_article_text(doi)
        if "bulunamadı" in meta:
            return "Makale erişimi sağlanamadı."

        return summarize_text(meta)
    except Exception as e:
        return f"Hata oluştu: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="stdio")
