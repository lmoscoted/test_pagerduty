import pytest
from unittest.mock import patch, Mock
from api.service.api_requests import PagerDutyAPI
from config import Config


@pytest.mark.asyncio
async def test_get_headers(pagerduty_api):
    headers = await pagerduty_api._get_headers()

    assert headers["Accept"] == "application/json"
    assert headers["Content-Type"] == "application/json"
    assert headers["Authorization"] == f"Token token={Config.PAGERDUTY_API_KEY}"


@pytest.mark.asyncio
async def test_get_(pagerduty_api):
    with patch("aiohttp.ClientSession") as mock_session:
        mock_session.return_value = Mock()
        mock_session.return_value.get.return_value = Mock()
        mock_session.return_value.get.return_value.json.return_value = {"incidents": [],
                                                                         "limit": 25, "more": True,
                                                                           "offset": 0, "total": None}

        response = await pagerduty_api._get("incidents")

        assert isinstance(response, dict)
        assert "incidents" in response
        assert "limit" in response
        assert "more" in response
        assert "offset" in response
        assert "total" in response


@pytest.mark.asyncio
async def test_get_incidents(pagerduty_api):
    with patch("aiohttp.ClientSession") as mock_session:
        mock_session.return_value = Mock()
        mock_session.return_value.get.return_value = Mock()
        mock_session.return_value.get.return_value.json.return_value = {"incidents": [], "limit": 25, 
                                                                        "more": True, "offset": 0,
                                                                          "total": None}

        response = await pagerduty_api.get_incidents()

        assert isinstance(response, dict)
        assert "incidents" in response
        assert "limit" in response
        assert "more" in response
        assert "offset" in response
        assert "total" in response

@pytest.mark.asyncio
async def test_get_services(pagerduty_api):
    with patch("aiohttp.ClientSession") as mock_session:
        mock_session.return_value = Mock()
        mock_session.return_value.get.return_value = Mock()
        mock_session.return_value.get.return_value.json.return_value = {"services": [], "limit": 25,
                                                                         "more": True, "offset": 0, 
                                                                         "total": None}
        response = await pagerduty_api.get_services()

        assert isinstance(response, dict)
        assert "services" in response
        assert "limit" in response
        assert "more" in response
        assert "offset" in response
        assert "total" in response

@pytest.mark.asyncio
async def test_get_teams(pagerduty_api):
    with patch("aiohttp.ClientSession") as mock_session:
        mock_session.return_value = Mock()
        mock_session.return_value.get.return_value = Mock()
        mock_session.return_value.get.return_value.json.return_value = {"teams": [], 
                                                                        "limit": 25, "more": True,
                                                                          "offset": 0, "total": None}
        response = await pagerduty_api.get_teams()

        assert isinstance(response, dict)
        assert "teams" in response
        assert "limit" in response
        assert "more" in response
        assert "offset" in response
        assert "total" in response


@pytest.mark.asyncio
async def test_get_escalation_policies(pagerduty_api):
    with patch("aiohttp.ClientSession") as mock_session:
        mock_session.return_value = Mock()
        mock_session.return_value.get.return_value = Mock()
        mock_session.return_value.get.return_value.json.return_value = {"escalation_policies": [], 
                                                                        "limit": 25, "more": True, 
                                                                        "offset": 0, "total": None}
        
        response = await pagerduty_api.get_escalation_policies()

        assert isinstance(response, dict)
        assert "escalation_policies" in response
        assert "limit" in response
        assert "more" in response
        assert "offset" in response
        assert "total" in response


@pytest.mark.asyncio
async def test_fetch_with_pagination(pagerduty_api):
    with patch("aiohttp.ClientSession") as mock_session:
        mock_session.return_value = Mock()
        mock_session.return_value.get.return_value = Mock()
        mock_session.return_value.get.return_value.json.return_value = {"incidents": [], 
                                                                        "limit": 25, "more": True, 
                                                                        "offset": 0, "total": None}
        
        response = await pagerduty_api._fetch_with_pagination("incidents")

        assert isinstance(response, list)
        assert all(isinstance(item, dict) for item in response)


@pytest.mark.asyncio
async def test_fetch_incidents_with_pagination(pagerduty_api):
    with patch("aiohttp.ClientSession") as mock_session:
        mock_session.return_value = Mock()
        mock_session.return_value.get.return_value = Mock()
        mock_session.return_value.get.return_value.json.return_value = {"incidents": [],
                                                                         "limit": 25, "more": True,
                                                                           "offset": 0, "total": None}
        
        response = await pagerduty_api.fetch_incidents_with_pagination()

        assert isinstance(response, list)
        assert all(isinstance(item, dict) for item in response)


@pytest.mark.asyncio
async def test_fetch_services_with_pagination(pagerduty_api):
    with patch("aiohttp.ClientSession") as mock_session:
        mock_session.return_value = Mock()
        mock_session.return_value.get.return_value = Mock()
        mock_session.return_value.get.return_value.json.return_value = {"services": [], 
                                                                        "limit": 25, "more": True, 
                                                                        "offset": 0, "total": None}
        
        response = await pagerduty_api.fetch_services_with_pagination()

        assert isinstance(response, list)
        assert all(isinstance(item, dict) for item in response)


@pytest.mark.asyncio
async def test_fetch_teams_with_pagination(pagerduty_api):
    with patch("aiohttp.ClientSession") as mock_session:
        mock_session.return_value = Mock()
        mock_session.return_value.get.return_value = Mock()
        mock_session.return_value.get.return_value.json.return_value = {"teams": [], 
                                                                        "limit": 25, "more": True, 
                                                                        "offset": 0, "total": None}
        
        response = await pagerduty_api.fetch_teams_with_pagination()

        assert isinstance(response, list)
        assert all(isinstance(item, dict) for item in response)


@pytest.mark.asyncio
async def test_fetch_escalation_policies_with_pagination(pagerduty_api):
    with patch("aiohttp.ClientSession") as mock_session:
        mock_session.return_value = Mock()
        mock_session.return_value.get.return_value = Mock()
        mock_session.return_value.get.return_value.json.return_value = {"escalation_policies": [], 
                                                                        "limit": 25, "more": True, 
                                                                        "offset": 0, "total": None}
        
        response = await pagerduty_api.fetch_escalation_policies_with_pagination()

        assert isinstance(response, list)
        assert all(isinstance(item, dict) for item in response)