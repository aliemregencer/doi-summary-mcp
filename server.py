from mcp.server.fastmcp import FastMCP
from app import get_article_text, summarize_text

mcp = FastMCP("doi-summary-mcp")

@mcp.tool()
async def summarize_doi(doi: str) -> str:
    """
    DOI girilerek makale özeti alınır.
    """
    text = get_article_text(doi)
    if "bulunamadı" in text:
        return "Makale erişimi sağlanamadı."

    summary = summarize_text(text)
    return summary

if __name__ == "__main__":
    mcp.run(transport="stdio")