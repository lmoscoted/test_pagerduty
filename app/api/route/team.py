import csv


from flask import Blueprint, jsonify, send_file
from flasgger import swag_from


team_api = Blueprint('team_api', __name__, url_prefix='/api/v1')

@team_api.route('/teams/with-services', methods=['GET'])
@swag_from('teams_with_services.yml')
def teams_with_services_():
    from api.model.models import Team
    """Return the number of Teams and their related Services"""

    teams = Team.query.all()
    teams_with_services = []
    for team in teams:
        services = team.services
        teams_with_services.append({'team': team.name, 'services': [service.name for service in services]})
    return jsonify(teams_with_services), 200


@team_api.route('/teams/with-services/csv', methods=['GET'])
@swag_from('teams_with_services_csv.yml')
def teams_with_services():
    """Return the number of Teams and their related Services"""
    from api.model.models import Team
    from io import BytesIO, StringIO

    teams = Team.query.all()
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Service ID', 'Service Name', 'Team ID', 'Team Name'])
    
    for team in teams:
        services = team.services
        for service in services:
            writer.writerow([service.id, service.name, team.id, team.name])
    
    output.seek(0)
    return send_file(
        BytesIO(output.read().encode('utf-8')),
        as_attachment=True,
        download_name='teams_with_services.csv',
        mimetype='text/csv'
    ), 200
