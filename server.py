from mcp.server.fastmcp import FastMCP
from app import (
    get_article_text,
    summarize_text,
    get_pdf_url_from_unpaywall,
    extract_text_from_pdf_url
)

mcp = FastMCP("doi-summary-mcp")

UNPAYWALL_EMAIL = "genceraliemre@gmail.com"

@mcp.tool()
async def summarize_doi(doi: str) -> str:
    """
    DOI girilerek makale özeti alınır.
    Öncelik sırası:
    1. Unpaywall üzerinden PDF varsa tam metni özetle
    2. PDF yoksa abstract'ı özetle
    """
    try:
        pdf_url = get_pdf_url_from_unpaywall(doi, UNPAYWALL_EMAIL)
        if pdf_url:
            try:
                full_text = extract_text_from_pdf_url(pdf_url)
                if not full_text.strip():
                    return "PDF bulundu ancak içerik çıkarılamadı."
                return summarize_text(full_text)
            except Exception as e:
                return f"PDF indirildi ancak işlenirken hata oluştu:\n{str(e)}"

        text = get_article_text(doi)
        if "bulunamadı" in text:
            return "Makale erişimi sağlanamadı."
        return summarize_text(text)

    except Exception as e:
        return f"Bir hata oluştu:\n{str(e)}"

if __name__ == "__main__":
    mcp.run(transport="stdio")
