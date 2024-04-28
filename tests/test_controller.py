import asyncio
import aiohttp
import pytest
from unittest.mock import MagicMock, patch
from app.controller import TaxCalculatorController


@pytest.fixture
def controller():
    return TaxCalculatorController()


@pytest.mark.asyncio
async def test_fetch_tax_brackets_success(controller):
    with patch('app.controller.aiohttp.ClientSession.get') as mock_get:
        # Create a MagicMock object for the response
        mock_response = MagicMock()
        mock_response.status = 200

        # Define the JSON data to be returned by the response
        tax_brackets_data = {'tax_brackets': [{'min': 0, 'max': 10000, 'rate': 0.1}]}

        # Define a coroutine task that returns the JSON data
        async def get_json():
            return tax_brackets_data

        # Mock the response.json() method to return the coroutine task
        mock_response.json.return_value = asyncio.create_task(get_json())

        # Configure the mock_get object to return the mock_response
        mock_get.return_value.__aenter__.return_value = mock_response

        # Call the fetch_tax_brackets method
        await controller.fetch_tax_brackets(2019)

        # Assert that the tax brackets cache is populated correctly
        assert 2019 in controller.tax_brackets_cache
        assert len(controller.tax_brackets_cache[2019]) == 1


@pytest.mark.asyncio
async def test_fetch_tax_brackets_failure(controller):
    with patch('app.controller.aiohttp.ClientSession.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status = 404
        mock_get.return_value.__aenter__.return_value = mock_response

        await controller.fetch_tax_brackets(2019)
        assert 2019 not in controller.tax_brackets_cache


@pytest.mark.asyncio
async def test_fetch_tax_brackets_unexpected_status_code(controller):
    # Test case for handling unexpected status code
    with patch('app.controller.aiohttp.ClientSession.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status = 500
        mock_get.return_value.__aenter__.return_value = mock_response

        await controller.fetch_tax_brackets(2019)
        assert 2019 not in controller.tax_brackets_cache

