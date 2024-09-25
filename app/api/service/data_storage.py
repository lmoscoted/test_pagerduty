from api.model.models import Incident, Service, Team, EscalationPolicy, ServiceTeam, EscalationPolicyTeam


class DataStorage:
    def __init__(self, session):
        self.session = session


    def _store_incidents(self, incidents_data):
        with self.session:
            for incident_data in incidents_data:
                incident = self.session.get(Incident, str(incident_data['id']))
                if  not incident:
                    # Create an Incident object using relevant fields
                    incident = Incident(
                        id=incident_data["id"],
                        incident_key=incident_data["incident_key"],
                        title=incident_data["title"],
                        description=incident_data.get("description"),
                        status=incident_data["status"],
                        # Extract service details if available
                        service_id=(incident_data["service"]["id"]
                                    if incident_data.get("service") else None),       
                    )
                else:
                    incident.title = incident_data["title"]
                    incident.description = incident_data.get("description")
                    incident.status = incident_data.get("status")

                # Add the incident to the session for storage
                self.session.add(incident)
            self.session.commit()

    def _store_services(self, services_data):
            with self.session:
                for service_data in services_data:
                    # Check if team already exists
                    service = self.session.query(Service).get(str(service_data["id"]))
                    if not service:
                        # Create a Service object using relevant fields
                        service = Service(
                            id = service_data["id"],
                            name=service_data["name"],
                            description=service_data.get("description"),
                            escalation_policy_id=service_data['escalation_policy']['id'],
                        )
                    else:
                        service.name = service_data["name"]
                        service.description = service_data.get("description")
                    # Extract and store related data (optional)
                    if service_data.get("teams"):
                        for team_data in service_data["teams"]:
                            # Check if team already exists
                            team = self.session.query(Team).get(str(team_data["id"]))
                        if team:
                            if self.session.query(ServiceTeam).filter_by(service_id=service.id, team_id=team.id).first():
                                # print(f"Relationship already exists between Service {service.id} and Team {team.id}")
                                pass
                            else:
                                # Associate the team with the escalation policy
                                service.teams.append(team)

                        # Add the service to the session for storage
                    self.session.add(service)

                self.session.commit()

    def _store_teams(self, teams_data):
        with self.session:
            for team_data in teams_data:
                # Check if team already exists
                team = self.session.query(Team).get(str(team_data["id"]))
                if not team:
                    # Create a new Team object
                    team = Team(
                        id=team_data["id"],
                        name=team_data["name"],
                        description=team_data.get("description"),
                    )
                else:
                    # Update the existing team
                    team.name = team_data["name"]
                    team.description = team_data.get("description")

                # Add the team to the session for storage
                self.session.add(team)
            self.session.commit()

    def _store_escalation_policies(self, escalation_policies_data):
        with self.session:
            for escalation_policy_data in escalation_policies_data:
                # Check if team already exists
                escalation_policy = self.session.query(EscalationPolicy).get(str(escalation_policy_data["id"]))

                if not escalation_policy:
                    # Create an EscalationPolicy object using relevant fields
                    escalation_policy = EscalationPolicy(
                        id=escalation_policy_data["id"],
                        name=escalation_policy_data["name"],
                        description=escalation_policy_data.get("description"),
                    )
                else:
                    # Update the existing escalation_policy
                    escalation_policy.name = escalation_policy_data["name"]
                    escalation_policy.description = escalation_policy_data.get("description")

                # Extract and store related data (optional)
                if escalation_policy_data.get("services"):
                    for service_data in escalation_policy_data["services"]:
                        # Check if service already exists
                        service = self.session.query(Service).get(str(service_data["id"]))
                        if service:
                            if service.id in [s.id for s in escalation_policy.services]:
                                # print(f"Relationship already exists between EscalationPolicy {escalation_policy.id} and Service {service.id}")
                                pass
                            else:
                                # Associate the service with the escalation policy
                                escalation_policy.services.append(service)

                if escalation_policy_data.get("teams"):
                    for team_data in escalation_policy_data["teams"]:
                        # Check if team already exists
                        team = self.session.query(Team).get(str(team_data["id"]))

                        if team:
                            if self.session.query(EscalationPolicyTeam).filter_by(escalation_policy_id=escalation_policy.id, team_id=team.id).first():
                                # print(f"Relationship already exists between EscalationPolicy {escalation_policy.id} and Team {team.id}")
                                pass
                            else:
                                # Associate the team with the escalation policy
                                escalation_policy.teams.append(team)
                # Add the escalation policy to the session for storage
                self.session.add(escalation_policy)
            self.session.commit()