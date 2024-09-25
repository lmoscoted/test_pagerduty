from pytest_mock import mocker
from sqlalchemy import func, text
from api.model.models import Service, EscalationPolicy


def test_service_count_csv(client, mocker, session):
    import importlib
    importlib.import_module('api.model.models')

    mocker.patch('api.model.models.Service.query.all', return_value=[Service(id="SERV1", name="Test Service 1"), 
                                                                     Service(id="SERV2", name="Test Service 2")])
    response = client.get('/api/v1/services/count/csv')

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'text/csv; charset=utf-8'
    assert response.headers['Content-Disposition'] == 'attachment; filename=service_count.csv'


def test_service_count(client, mocker, session):
    import importlib
    importlib.import_module('api.model.models')
    from api.model.models import Service

    mock_service_query_all = mocker.patch('api.model.models.Service.query.all')
    session.rollback()

    session.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
    session.execute(text("DELETE FROM services"))
    session.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
    session.commit()


    # Frist the escalation policies must exist in the database, because of the integrity constraints
    escalation_p1 = EscalationPolicy(id="EP1", name="Escalation policy 1")
    escalation_p2 = EscalationPolicy(id="EP2", name="Escalation policy  2")
    session.add(escalation_p1)
    session.add(escalation_p2)
    session.commit()

    service1 = Service(id="SERV1", name="Test Service 1", escalation_policy_id="EP1")
    service2 = Service(id="SERV2", name="Test Service 2",  escalation_policy_id="EP2")
    
    session.add(service1)
    session.add(service2)
    session.commit()
    
    mock_service_query_all.return_value = [service1, service2]

    response = client.get('/api/v1/services/count')

    assert response.status_code == 200
    assert response.json
    assert isinstance(response.json, dict)
    assert response.json['count'] == 2