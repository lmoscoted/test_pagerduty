import asyncio
import pytest
from unittest.mock import patch, Mock
from api.service.pager_duty import PagerDutyService


@pytest.fixture
def pagerduty_service():
    return PagerDutyService()


@pytest.mark.asyncio
async def test_fetch_and_store_data(pagerduty_service, mocker):
    mock_fetch_incidents = mocker.patch('api.service.api_requests.PagerDutyAPI.fetch_incidents_with_pagination')
    mock_store_incidents = mocker.patch('api.service.data_storage.DataStorage._store_incidents')
    mock_fetch_services = mocker.patch('api.service.api_requests.PagerDutyAPI.fetch_services_with_pagination')
    mock_store_services = mocker.patch('api.service.data_storage.DataStorage._store_services')
    mock_fetch_teams = mocker.patch('api.service.api_requests.PagerDutyAPI.fetch_teams_with_pagination')
    mock_store_teams = mocker.patch('api.service.data_storage.DataStorage._store_teams')
    mock_fetch_escalation_policies = mocker.patch('api.service.api_requests.PagerDutyAPI.fetch_escalation_policies_with_pagination')
    mock_store_escalation_policies = mocker.patch('api.service.data_storage.DataStorage._store_escalation_policies')

    mock_fetch_incidents.return_value = [{'id': 'INC1', 'title': 'Test Incident'}]
    mock_fetch_services.return_value = [{'id': 'SERV1', 'name': 'Test Service'}]
    mock_fetch_teams.return_value = [{'id': 'TEAM1', 'name': 'Test Team'}]
    mock_fetch_escalation_policies.return_value = [{'id': 'EP1', 'name': 'Test Escalation Policy'}]

    await pagerduty_service.fetch_and_store_data()

    mock_store_incidents.assert_called_once()
    mock_store_services.assert_called_once()
    mock_store_teams.assert_called_once()
    mock_store_escalation_policies.assert_called_once()


@pytest.mark.asyncio
async def test_fetch_and_store_data_error_fetch_incidents(pagerduty_service, mocker):
    mock_fetch_incidents = mocker.patch('api.service.api_requests.PagerDutyAPI.fetch_incidents_with_pagination')
    mock_fetch_incidents.side_effect = Exception()

    assert await pagerduty_service.fetch_and_store_data() == False


@pytest.mark.asyncio
async def test_fetch_and_store_data_error_fetch_services(pagerduty_service, mocker):
    mock_fetch_services = mocker.patch('api.service.api_requests.PagerDutyAPI.fetch_services_with_pagination')
    mock_fetch_services.side_effect = Exception()

    assert await pagerduty_service.fetch_and_store_data() == False


@pytest.mark.asyncio
async def test_fetch_and_store_data_error_store_services(pagerduty_service, mocker):
    mock_store_services = mocker.patch('api.service.pager_duty.DataStorage._store_services')
    mock_store_services.side_effect = Exception()

    assert await pagerduty_service.fetch_and_store_data() == False


@pytest.mark.asyncio
async def test_fetch_and_store_data_error_fetch_teams(pagerduty_service, mocker):
    mock_fetch_teams = mocker.patch('api.service.api_requests.PagerDutyAPI.fetch_teams_with_pagination')
    mock_fetch_teams.side_effect = Exception()

    assert await pagerduty_service.fetch_and_store_data() == False


@pytest.mark.asyncio
async def test_fetch_and_store_data_error_store_teams(pagerduty_service, mocker):
    mock_store_teams = mocker.patch('api.service.pager_duty.DataStorage._store_teams')
    mock_store_teams.side_effect = Exception()

    assert await pagerduty_service.fetch_and_store_data() == False


@pytest.mark.asyncio
async def test_fetch_and_store_data_error_fetch_escalation_policies(pagerduty_service, mocker):
    mock_fetch_escalation_policies = mocker.patch('api.service.api_requests.PagerDutyAPI.fetch_escalation_policies_with_pagination')
    mock_fetch_escalation_policies.side_effect = Exception()

    assert await pagerduty_service.fetch_and_store_data() == False


@pytest.mark.asyncio
async def test_fetch_and_store_data_error_store_escalation_policies(pagerduty_service, mocker):
    mock_store_escalation_policies = mocker.patch('api.service.pager_duty.DataStorage._store_escalation_policies')
    mock_store_escalation_policies.side_effect = Exception()

    assert await pagerduty_service.fetch_and_store_data() == False
    

@pytest.fixture
def mock_fetch_incidents(mocker):
    return mocker.patch('api.service.api_requests.PagerDutyAPI.fetch_incidents_with_pagination')


@pytest.mark.asyncio
async def test_fetch_and_store_data_raises_exception(mock_fetch_incidents):
    mock_fetch_incidents.side_effect = Exception('Mocked exception')
    pagerduty_service = PagerDutyService()

    assert await pagerduty_service.fetch_and_store_data() == False


@pytest.mark.asyncio
async def test_fetch_and_store_data_raises_exception(mock_fetch_incidents):
    mock_fetch_incidents.side_effect = Exception('Mocked exception')
    pagerduty_service = PagerDutyService()

    assert await pagerduty_service.fetch_and_store_data() == False


@pytest.mark.asyncio
async def test_fetch_and_store_data_timeout(mock_fetch_incidents):
    mock_fetch_incidents.side_effect = asyncio.TimeoutError('Timeout error')
    pagerduty_service = PagerDutyService()

    assert await pagerduty_service.fetch_and_store_data() == False


@pytest.mark.asyncio
async def test_fetch_and_store_data_connection_error(mock_fetch_incidents):
    mock_fetch_incidents.side_effect = ConnectionError('Connection error')
    pagerduty_service = PagerDutyService()

    assert await pagerduty_service.fetch_and_store_data() == False


