from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from database import db


class Incident(db.Model):
    __tablename__ = "incidents"

    id = Column(String(20), primary_key=True)
    incident_key= Column(String(32), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(String(1200))
    status = Column(String(255), nullable=False)
    service_id = Column(String(12), ForeignKey("services.id"), nullable=False)
    services = relationship("Service", back_populates="incidents")
    


class Service(db.Model):
    __tablename__ = "services"

    id = Column(String(12), primary_key=True)
    name = Column(String(255))
    description = Column(String(1200))
    escalation_policy_id = Column(String(12), ForeignKey("escalation_policies.id"), nullable=False)
    escalation_policy =  relationship("EscalationPolicy", back_populates="services")
    incidents = relationship("Incident", back_populates="services")
    teams = relationship(
        "Team", secondary="services_teams", back_populates="services"
    )


class Team(db.Model):
    __tablename__ = "teams"

    id = Column(String(12), primary_key=True)
    name = Column(String(255))
    description = Column(String(1200))
    services = relationship("Service", secondary="services_teams", back_populates="teams")
    escalation_policies = relationship(
        "EscalationPolicy", secondary="escalation_policy_teams", back_populates="teams"
    )


class EscalationPolicy(db.Model):
    __tablename__ = "escalation_policies"

    id = Column(String(12), primary_key=True)
    name = Column(String(255))
    description = Column(String(1200))
    services = relationship(
        "Service", back_populates="escalation_policy"
    )
    teams = relationship(
        "Team", secondary="escalation_policy_teams", back_populates="escalation_policies"
    )


class ServiceTeam(db.Model):
    __tablename__ = "services_teams"

    service_id = Column(String(12), ForeignKey("services.id"), primary_key=True)
    team_id = Column(String(12), ForeignKey("teams.id"), primary_key=True)


class EscalationPolicyTeam(db.Model):
    __tablename__ = "escalation_policy_teams"

    escalation_policy_id = Column(String(12), ForeignKey("escalation_policies.id"), primary_key=True)
    team_id = Column(String(12), ForeignKey("teams.id"), primary_key=True)
