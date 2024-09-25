from pytest_mock import mocker

from api.model.models import Incident, Service


def test_incidents_by_service_and_status(client, mocker,session):
    import importlib
    importlib.import_module('api.model.models')

    mocker.patch('api.model.models.Incident.query.all', return_value=[Incident(id="INC1", service_id="SERV1", status="triggered")])
    mocker.patch('api.model.models.Service.query.get', return_value=Service(id="SERV1", name="Test Service"))

    response = client.get('/api/v1/incidents/by-service-and-status')

    assert response.status_code == 200
    assert isinstance(response.json, dict)


def test_incidents_by_service_and_status_csv(client, mocker,session):
    import importlib
    importlib.import_module('api.model.models')

    mocker.patch('api.model.models.Incident.query.all', return_value=[Incident(id="INC2", service_id="SERV2", status="resolved")])
    mocker.patch('api.model.models.Service.query.get', return_value=Service(id="SERV2", name="Test Service"))

    response = client.get('/api/v1/incidents/by-service-and-status/csv')

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'text/csv; charset=utf-8'
    assert response.headers['Content-Disposition'] == 'attachment; filename=incidents_by_service_and_status.csv'


def test_incidents_by_service(client, mocker,session):
    import importlib
    importlib.import_module('api.model.models')

    mocker.patch('api.model.models.Incident.query.all', return_value=[Incident(id="INC3", service_id="SERV3", 
                                                                               status="triggered"),
                                                                      Incident(id="INC4", service_id="SERV4", 
                                                                               status="resolved")])
    mocker.patch('api.model.models.Service.query.get', side_effect=[Service(id="SERV3", name="Test Service 3"), 
                                                                    Service(id="SERV4", name="Test Service 4")])

    response = client.get('/api/v1/incidents/by-service')

    assert response.status_code == 200
    assert isinstance(response.json, dict)


def test_incidents_by_service_csv(client, mocker,session):
    import importlib

    importlib.import_module('api.model.models')
    mocker.patch('api.model.models.Incident.query.all', return_value=[Incident(id="INC4", service_id="SERV4", status="triggered")])
    mocker.patch('api.model.models.Service.query.get', return_value=Service(id="SERV4", name="Test Service"))

    response = client.get('/api/v1/incidents/by-service/csv')

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'text/csv; charset=utf-8'
    assert response.headers['Content-Disposition'] == 'attachment; filename=incidents_by_service.csv'