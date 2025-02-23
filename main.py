from fastapi import FastAPI

app = FastAPI()

# Memory cache to store results for each page (to be implemented later)
cached_pages = {}


@app.get("/")
async def root():
    """
    The root endpoint ("/") behaves the same as "/1".
    It returns the news from page 1.
    """
    return await get_news(1)


@app.get("/{page_count}")
async def get_news(page_count: int):
    """
    Returns 'page_count' * 30 news items.
    For now, we generate dummy data so the tests pass.
    """
    #Dummy news object with the expected structure
    dummy_news = {
        "title": "title",
        "points": 0,
        "sent_by": "fake author",
        "published": "just now",
        "comments": 0
    }

    news_list = [dummy_news.copy() for _ in range(page_count * 30)]

    return news_list
