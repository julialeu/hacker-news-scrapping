
This project develops an asynchronous API with FastAPI to scrape news from Hacker News. The API has two major endpoints:
GET /: As GET /1. It returns 30 news items from page 1.

GET /{page_count}: This endpoint returns news_items from page_count and page_count multiplied by thirty for news items by concatenating page 1 to the page that is specified.

The application caches data in-memory to lower the number of requests to the same page and thus simplify reading.

Requirements:

Python >=3.9

Docker and Docker Compose for your deployment.

Dependencies:

A set of Python packages located in requirements.txt

Local Installation and Usage:

1. Clone the repository:
git clone https://github.com/julialeu/flanks.git

cd flanks

2. Create and activate a virtual environment:
python3 -m venv .venv

source .venv/bin/activate

3. Install the dependencies:
pip install -r requirements.txt

4. Run the API locally:
uvicorn main:app --host 0.0.0.0 --port 3000 --reload

5. Test the API:
curl -s localhost:3000 | jq ----> This should give you the news in JSON format.

6. Running Tests: To execute tests, make sure that pytest and pytest-asyncio are installed. Then, run from your project root:
pytest

7. Docker: The project contains a Dockerfile and a docker-compose.yml file to use for deployment.

8. Dockerfile and docker-compose.yml:

The Dockerfile uses the python:3.9-slim image, installs dependencies, copies the source code, and exposes port 3000. The default command starts the app with Uvicorn.
version: "3.9"

9. Build and Run with Docker:
To get started, navigate to the project root and execute the following commands:
docker compose build --no-cache
docker compose up -d

If you need to stop and remove the container, use:
docker compose down

10. Caching Mechanism
The get_news function implements a straightforward in-memory cache (cached_pages) to keep track of data for each page. This approach helps avoid the need to download and parse the same page repeatedly.

11. Asynchronous Concurrency
The API now incorporates asyncio.gather in the get_news endpoint for parallel fetching of pages. The difference guarantees that multiple pages are scraped concurrently instead of one after the other, improving response times overall.
For instance, to demonstrate the concurrent behavior, you can implement a delay inside the fetch_page method:
async def fetch_page(page_number: int):
    await asyncio.sleep(1) 

Then run ----> curl -w "Total Time: %{time_total}s\n" -o /dev/null -s http://localhost:3000/2

Concurrent page fetch should take approximately 1 second overall, as opposed to 2 seconds (sequential page fetching).

12. Parsing Hacker News
The fetch_page function retrieves a Hacker News page and utilizes BeautifulSoup to extract the following information:

- Title (using the selector span.titleline a)
- Points
- Posted by (sent_by)
- Published time
- Number of comments

In cases where a title cannot be found, it will return "No title".










