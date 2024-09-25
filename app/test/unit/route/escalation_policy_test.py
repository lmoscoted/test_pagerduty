from pytest_mock import mocker

from api.model.models import EscalationPolicy, Team, Service


def test_escalation_policies_with_teams_and_services_csv(client, mocker, session):
    # The model was imported in the function and not globally.
    import importlib
    importlib.import_module('api.model.models')
    mocker.patch('api.model.models.EscalationPolicy.query.all', 
                 return_value=[EscalationPolicy(id="LADS2", 
                                                name="Test Escalation Policy", 
                                                description="This is a test escalation policy", 
                                                teams=[Team(id="TEAM1", 
                                                name="Test Team")], 
                                                services=[Service(id="SERVICE1", 
                                                name="Test Service")])])
    
    response = client.get('/api/v1/escalation-policies/with-teams-and-services/csv')
    
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'text/csv; charset=utf-8'
    assert response.headers['Content-Disposition'] == 'attachment; filename=escalation_policies_with_teams_and_services.csv'


def test_escalation_policies_with_teams_and_services(client, mocker, session):
    # The model was imported in the function and not globally.
    import importlib
    importlib.import_module('api.model.models')
    mocker.patch('api.model.models.EscalationPolicy.query.all', 
                 return_value=[EscalationPolicy(id="LADS2", 
                                                name="Test Escalation Policy", 
                                                description="This is a test escalation policy", 
                                                teams=[Team(id="TEAM1", 
                                                name="Test Team")], 
                                                services=[Service(id="SERVICE1", 
                                                name="Test Service")])])

    response = client.get('/api/v1/escalation-policies/with-teams-and-services')

    assert response.status_code == 200
    assert isinstance(response.json, list)