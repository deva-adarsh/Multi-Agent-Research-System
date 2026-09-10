from src.tools.tools import web_search, scrape_url

result = web_search.invoke(
    "What is the latest news about AI?"
)

web_result=scrape_url.invoke(
    "https://techcrunch.com/category/artificial-intelligence/"
)
print(web_result)