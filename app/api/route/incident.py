from flask import Blueprint, jsonify, send_file
from flasgger import swag_from


incident_api = Blueprint('incident_api', __name__, url_prefix='/api/v1')

@incident_api.route('/incidents/by-service-and-status', methods=['GET'])
@swag_from('incidents_by_service_and_status.yml')
def incidents_by_service_and_status_():
    from api.model.models import Incident
    """Return the number of Incidents by Service and Status"""
    incidents = Incident.query.all()
    incidents_by_service_and_status = {}
    for incident in incidents:
        service_id = incident.service_id
        status = incident.status
        if service_id not in incidents_by_service_and_status:
            incidents_by_service_and_status[service_id] = {}
        if status not in incidents_by_service_and_status[service_id]:
            incidents_by_service_and_status[service_id][status] = 0
        incidents_by_service_and_status[service_id][status] += 1
    return jsonify(incidents_by_service_and_status), 200


@incident_api.route('/incidents/by-service-and-status/csv', methods=['GET'])
@swag_from('incidents_by_service_and_status_csv.yml')
def incidents_by_service_and_status():
    from api.model.models import Incident, Service
    from io import BytesIO, StringIO
    import csv

    incidents = Incident.query.all()
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Service ID', 'Service Name', 'Status', 'Incident Count'])
    
    incidents_by_service_and_status = {}
    for incident in incidents:
        service_id = incident.service_id
        service = Service.query.get(service_id)
        service_name = service.name
        status = incident.status
        if service_id not in incidents_by_service_and_status:
            incidents_by_service_and_status[service_id] = {'name': service_name, 'status_counts': {}}
        if status not in incidents_by_service_and_status[service_id]['status_counts']:
            incidents_by_service_and_status[service_id]['status_counts'][status] = 0
        incidents_by_service_and_status[service_id]['status_counts'][status] += 1
    
    for service_id, service_info in incidents_by_service_and_status.items():
        for status, count in service_info['status_counts'].items():
            writer.writerow([service_id, service_info['name'], status, count])
    
    output.seek(0)
    return send_file(
        BytesIO(output.read().encode('utf-8')),
        as_attachment=True,
        download_name='incidents_by_service_and_status.csv',
        mimetype='text/csv'
    ), 200


@incident_api.route('/incidents/by-service/csv', methods=['GET'])
@swag_from('incidents_by_service_csv.yml')
def incidents_by_service():
    from api.model.models import Incident, Service
    from io import BytesIO, StringIO
    import csv

    incidents = Incident.query.all()
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Service ID', 'Service Name', 'Incident Count'])
    
    incidents_by_service = {}
    for incident in incidents:
        service_id = incident.service_id
        service = Service.query.get(service_id)
        service_name = service.name
        if service_id not in incidents_by_service:
            incidents_by_service[service_id] = {'name': service_name, 'count': 0}
        incidents_by_service[service_id]['count'] += 1
    
    for service_id, service_info in incidents_by_service.items():
        writer.writerow([service_id, service_info['name'], service_info['count']])
    
    output.seek(0)
    return send_file(
        BytesIO(output.read().encode('utf-8')),
        as_attachment=True,
        download_name='incidents_by_service.csv',
        mimetype='text/csv'
    ), 200


@incident_api.route('/incidents/by-service', methods=['GET'])
@swag_from('incidents_by_service.yml')
def incidents_by_service_():
    from api.model.models import Incident, Service
    """Return the number of Incidents per Service"""
    incidents = Incident.query.all()
    incidents_by_service = {}
    for incident in incidents:
        service_id = incident.service_id
        service = Service.query.get(service_id)
        if service_id not in incidents_by_service:
            incidents_by_service[service_id] = {'name': service.name, 'count': 0}
        incidents_by_service[service_id]['count'] += 1
    return jsonify(incidents_by_service), 200
   
