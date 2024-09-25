from flask import Blueprint, jsonify, send_file
from flasgger import swag_from


escalation_policy_api = Blueprint('escalation_policy_api', __name__, url_prefix='/api/v1')


@escalation_policy_api.route('/escalation-policies/with-teams-and-services/csv', methods=['GET'])
@swag_from('escalation_policies_with_teams_and_services_csv.yml')
def escalation_policies_with_teams_and_services():
    from api.model.models import EscalationPolicy
    from io import BytesIO, StringIO
    import csv

    escalation_policies = EscalationPolicy.query.all()
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Escalation Policy', 'Team Name', 'Team Id', 'Service Name', 'Service Id'])
    
    for escalation_policy in escalation_policies:
        teams = escalation_policy.teams
        services = escalation_policy.services
        for team in teams:
            for service in services:
                writer.writerow([escalation_policy.name, team.name, team.id, service.name, service.id])
    
    output.seek(0)
    return send_file(
        BytesIO(output.read().encode('utf-8')),
        as_attachment=True,
        download_name='escalation_policies_with_teams_and_services.csv',
        mimetype='text/csv'
    ), 200


@escalation_policy_api.route('/escalation-policies/with-teams-and-services', methods=['GET'])
@swag_from('escalation_policies_with_teams_and_services.yml')
def escalation_policies_with_teams_and_services_():
    from api.model.models import EscalationPolicy

    """Return the number of Escalation Policies and their Relationship with Teams and Services"""
    escalation_policies = EscalationPolicy.query.all()
    escalation_policies_with_teams_and_services = []
    for escalation_policy in escalation_policies:
        teams = escalation_policy.teams
        services = escalation_policy.services
        escalation_policies_with_teams_and_services.append({
            'escalation_policy': escalation_policy.name,
            'teams': [team.name for team in teams],
            'services': [service.name for service in services]
        })
        
    return jsonify(escalation_policies_with_teams_and_services), 200