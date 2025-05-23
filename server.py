from mcp.server.fastmcp import FastMCP
from app import (
    get_article_text,
    summarize_text,
    get_pdf_url_from_unpaywall
)

mcp = FastMCP("doi-summary-mcp")

# Unpaywall için e-mail adresin (zorunlu)
UNPAYWALL_EMAIL = "genceraliemre@gmail.com"

@mcp.tool()
async def summarize_doi(doi: str) -> str:
    """
    DOI girilerek makale özeti alınır.
    - Önce Unpaywall'dan PDF varsa indirip tam metinden özetler.
    - Yoksa başlık ve özetten özet çıkarır.
    """
    try:
        pdf_url = get_pdf_url_from_unpaywall(doi, UNPAYWALL_EMAIL)
        if pdf_url:
            return f"Açık erişimli PDF bulundu:\n{pdf_url}\n\n(Not: PDF içeriği özetleme henüz eklenmedi.)"
        
        # PDF yoksa metadata üzerinden özetle
        text = get_article_text(doi)
        if "bulunamadı" in text:
            return "Makale erişimi sağlanamadı."
        return summarize_text(text)

    except Exception as e:
        return f"Bir hata oluştu: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="stdio")
