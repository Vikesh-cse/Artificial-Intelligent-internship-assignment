from langchain.tools import tool

@tool
def mock_searxng_search(query: str):
    """Search for recent news headlines based on a query."""
    
    if "crypto" in query.lower():
        return "Bitcoin hits all-time high after ETF approval."
    elif "ai" in query.lower():
        return "OpenAI releases new powerful model."
    else:
        return "Stock market fluctuates amid inflation concerns."