# main.py
from fastapi import FastAPI
import httpx
from bs4 import BeautifulSoup

app = FastAPI()

# Memory cache to store results for each page.
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
    This implementation fetches real data from Hacker News and uses a simple in-memory cache.
    """
    # Ensure we have at least one page.
    page_count = max(1, page_count)
    news_list = []

    # Loop through each page from 1 to page_count.
    for p in range(1, page_count + 1):
        if p in cached_pages:
            page_data = cached_pages[p]
        else:
            page_data = await fetch_page(p)
            cached_pages[p] = page_data

        news_list.extend(page_data)

    return news_list


async def fetch_page(page_number: int):
    """
    Fetches the Hacker News page for the given page number,
    parses the HTML, and returns a list of news items with the expected structure.
    """
    url = f"https://news.ycombinator.com/news?p={page_number}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    soup = BeautifulSoup(response.text, "html.parser")
    results = []

    # Each news item is in a <tr> with class "athing".
    stories = soup.find_all("tr", class_="athing")

    for story in stories:
        title_tag = story.find("a", class_="titlelink")
        if not title_tag:
            title_tag = story.select_one("span.titleline a")

        title = title_tag.get_text(strip=True) if title_tag else "No title"

        # The subtext (points, author, time, comments) is in the next <tr>.
        subtext = story.find_next_sibling("tr")
        if subtext:
            subtext_td = subtext.find("td", class_="subtext")

            points_tag = subtext_td.find("span", class_="score") if subtext_td else None
            points = int(points_tag.get_text().split()[0]) if points_tag else 0

            author_tag = subtext_td.find("a", class_="hnuser") if subtext_td else None
            sent_by = author_tag.get_text() if author_tag else "anonymous"

            time_tag = subtext_td.find("span", class_="age") if subtext_td else None
            published = time_tag.get_text() if time_tag else "unknown"

            comment_tags = subtext_td.find_all("a") if subtext_td else []
            comments = 0
            if comment_tags:
                # The last link usually contains the number of comments or "discuss".
                comment_text = comment_tags[-1].get_text()
                if "comment" in comment_text:
                    try:
                        comments = int(comment_text.split()[0])
                    except (IndexError, ValueError):
                        comments = 0
        else:
            points, sent_by, published, comments = 0, "anonymous", "unknown", 0

        results.append({
            "title": title,
            "points": points,
            "sent_by": sent_by,
            "published": published,
            "comments": comments
        })

    return results
