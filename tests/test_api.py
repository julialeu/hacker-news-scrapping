
import pytest
import httpx
from httpx import ASGITransport
from main import app


@pytest.mark.asyncio
async def test_get_one_page():
    """
    Check that the endpoint /1 returns exactly 30 news items.
    """
    # Create an ASGI transport that wraps our FastAPI app.
    transport = ASGITransport(app=app)

    # Use this transport in an AsyncClient to make requests.
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/1")  # Send a GET request to the /1 endpoint.

    # Make sure the response status code is 200 (OK).
    assert response.status_code == 200

    # Convert the response to JSON format.
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
