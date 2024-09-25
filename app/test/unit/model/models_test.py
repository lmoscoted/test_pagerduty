import pytest
import sqlalchemy
from api.model.models import Incident, Service, Team, EscalationPolicy


def test_incident_creation_with_service(session):

    session.rollback()
    escalation_policy = EscalationPolicy(id="LADS100", name="Test Escalation Policy", description="This is a test escalation policy")
    session.add(escalation_policy)
    session.commit() 

    service = Service(id="CASD", name="Test Service", description="This is a test service", escalation_policy_id="LADS100")
    session.add(service)
    session.commit()

    incident = Incident(id="AFFJ", incident_key="abc", title="Test Incident", description="This is a test incident", status="open", service_id="CASD")
    session.add(incident)
    session.commit()

    assert incident.service_id == "CASD"
    assert incident.services == service
 
def test_service_creation_with_escalation_policy(session):
    session.rollback()

    escalation_policy = EscalationPolicy(id="LADS2", name="Test Escalation Policy", description="This is a test escalation policy")
    session.add(escalation_policy)
    session.commit()

    service = Service(id="CASD2", name="Test Service", description="This is a test service", escalation_policy_id="LADS2")
    session.add(service)
    session.commit()

    assert service.escalation_policy_id == "LADS2"
    assert service.escalation_policy == escalation_policy
  
def test_service_creation_without_escalation_policy(session):
    session.rollback()

    service = Service(id="CASD3", name="Test Service", description="This is a test service", escalation_policy_id="LADS3")
    with pytest.raises(sqlalchemy.exc.IntegrityError): 
        session.add(service)
        session.flush()



def test_incident_creation_without_service(session):
    session.rollback()

    incident = Incident(id="AFFJ2", incident_key="abc", title="Test Incident", description="This is a test incident", status="triggered", service_id="CASD5")
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        session.add(incident)
        session.flush()
 
def test_team_creation_with_service(session):
    session.rollback()

    escalation_policy = EscalationPolicy(id="LADS6", name="Test Escalation Policy", description="This is a test escalation policy")
    session.add(escalation_policy)
    session.commit()

    service = Service(id="CASD5", name="Test Service", description="This is a test service", escalation_policy_id="LADS6")
    session.add(service)
    session.commit()

    team = Team(id="BAXC", name="Test Team", description="This is a test team")
    team.services.append(service)
    session.add(team)
    session.commit()

    assert team.services == [service]

def test_team_creation_without_service(session):
    session.rollback()

    team = Team(id="BAXC1", name="Test Team", description="This is a test team")
    session.add(team)
    session.commit()

    assert team.services == []

def test_escalation_policy_creation_with_team(session):
    session.rollback()

    team = Team(id="BAXC2", name="Test Team", description="This is a test team")
    session.add(team)
    session.commit()

    escalation_policy = EscalationPolicy(id="LADS8", name="Test Escalation Policy", description="This is a test escalation policy")
    escalation_policy.teams.append(team)
    session.add(escalation_policy)
    session.commit()

    assert escalation_policy.teams == [team]

def test_escalation_policy_creation_without_team(session):
    session.rollback()

    escalation_policy = EscalationPolicy(id="LADS7", name="Test Escalation Policy", description="This is a test escalation policy")
    session.add(escalation_policy)
    session.commit()

    assert escalation_policy.teams == []





