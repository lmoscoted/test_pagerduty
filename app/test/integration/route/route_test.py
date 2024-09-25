import pytest
import asyncio
from api.service.pager_duty import PagerDutyService


@pytest.fixture(scope="session")
def fetch_and_store_data():
    res = asyncio.run(PagerDutyService().fetch_and_store_data())
    if res:
        print('Data saved.')      
    else:
         pytest.fail("Failed to fetch and store data")
         

def test_get_incidents_by_service_and_status_csv(client, fetch_and_store_data):
        
    response = client.get('/api/v1/incidents/by-service-and-status/csv')
    
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'text/csv; charset=utf-8'


def test_get_escalation_policies_with_teams_and_services_csv(client, fetch_and_store_data):
    response = client.get('/api/v1/escalation-policies/with-teams-and-services/csv')
    
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'text/csv; charset=utf-8'


def test_get_incidents_by_service_csv(client, fetch_and_store_data):

    response = client.get('/api/v1/incidents/by-service/csv')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'text/csv; charset=utf-8'


def test_get_services_count_csv(client, fetch_and_store_data):

    response = client.get('/api/v1/services/count/csv')

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'text/csv; charset=utf-8'
 
    
def test_get_teams_with_services_csv(client, fetch_and_store_data):
    
    response = client.get('/api/v1/teams/with-services/csv')

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'text/csv; charset=utf-8'


def test_get_services(client, fetch_and_store_data):

    response = client.get('/stats/services')

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'text/html; charset=utf-8'

 
def test_get_incidents_by_service_and_status(client, fetch_and_store_data):

    response = client.get('/api/v1/incidents/by-service-and-status')

    assert response.status_code == 200
    assert response.json
    assert isinstance(response.json, dict)


def test_get_escalation_policies_with_teams_and_services(client, fetch_and_store_data):

    response = client.get('/api/v1/escalation-policies/with-teams-and-services')

    assert response.status_code == 200
    assert response.json
    assert isinstance(response.json, list)


def test_get_teams_with_services(client, fetch_and_store_data):

    response = client.get('/api/v1/teams/with-services')

    assert response.status_code == 200
    assert response.json
    assert isinstance(response.json, list)



def test_get_incidents_by_service(client, fetch_and_store_data):

    response = client.get('/api/v1/incidents/by-service')

    assert response.status_code == 200
    assert response.json
    assert isinstance(response.json, dict)


def test_get_service_count(client, fetch_and_store_data):
    
    response = client.get('/api/v1/services/count')

    assert response.status_code == 200
    assert response.json
    assert isinstance(response.json, dict)


