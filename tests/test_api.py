# tests/test_api.py

import asyncio
import time
import pytest
import httpx
from httpx import ASGITransport
from main import app, cached_pages
from unittest.mock import patch

@pytest.mark.asyncio
async def test_get_one_page():
    """
    Check that the endpoint /1 returns exactly 30 news items.
    """
    # Create an ASGI transport that wraps the FastAPI app.
    transport = ASGITransport(app=app)

    # Use this transport in an AsyncClient to make requests.
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/1")  # Send a GET request to the /1 endpoint.

    assert response.status_code == 200
    data = response.json()

    # Check that the response is a list.
    assert isinstance(data, list)

    # Check that the list contains exactly 30 items.
    assert len(data) == 30

    # Take the first news item and verify it has the expected fields.
    first_item = data[0]
    assert "title" in first_item
    assert "points" in first_item
    assert "sent_by" in first_item
    assert "published" in first_item
    assert "comments" in first_item

@pytest.mark.asyncio
async def test_get_two_pages():
    """
    Check that the endpoint /2 returns exactly 60 news items.
    """
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/2")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 60

@pytest.mark.asyncio
async def test_get_three_pages():
    """
    Check that the endpoint /3 returns exactly 90 news items.
    """
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/3")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 90

    first_item = data[0]
    assert "title" in first_item
    assert "points" in first_item
    assert "sent_by" in first_item
    assert "published" in first_item
    assert "comments" in first_item

@pytest.mark.asyncio
async def test_cache_mechanism():
   """
   Verify that:
   - The first call to /1 should fetch and cache page 1.
   - The next call to /2 should fetch only page 2 (since page 1 is cached).
   """
   # Clear the cache to ensure a fresh start.
   cached_pages.clear()

   with patch("main.fetch_page") as mock_fetch:
       # Simulate fetch_page returning 30 fake items per page.
       mock_fetch.side_effect = lambda page: [f"fake_data_page_{page}"] * 30

       transport = ASGITransport(app=app)
       async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
           # Call /1
           await ac.get("/1")
           # Call /2
           await ac.get("/2")

   # Extract the arguments used in fetch_page calls.
   pages_called = [call.args[0] for call in mock_fetch.call_args_list]
   assert pages_called == [1, 2], f"Unexpected fetch_page calls: expected [1, 2], but got {pages_called}"

@pytest.mark.asyncio
async def test_async_concurrency():
    # Ensure a clean start without cache.
    cached_pages.clear()

    async def delayed_fetch(page: int):
        # Simulate a 1 sec delay for each call.
        await asyncio.sleep(1)
        return [f"fake_data_page_{page}"] * 30

    with patch("main.fetch_page", side_effect=delayed_fetch) as mock_fetch:
        start_time = time.monotonic()
        transport = ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
            # Request 2 pages, which should be executed in parallel
            response = await ac.get("/2")
        duration = time.monotonic() - start_time


    print(f"Duration: {duration:.2f} seconds")

    # if the program is executed concurrently this message will not be display in the terminal
    assert duration < 1.5, f"Concurrent execution took too long: {duration} seconds"