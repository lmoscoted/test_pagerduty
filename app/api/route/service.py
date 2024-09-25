from flask import Blueprint, jsonify, send_file
from flasgger import swag_from


service_api = Blueprint('service_api', __name__, url_prefix='/api/v1')


@service_api.route('/services/count/csv', methods=['GET'])
@swag_from('service_count_csv.yml')
def service_count():
    from api.model.models import Service
    from io import BytesIO, StringIO
    import csv

    services = Service.query.all()
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Service Count'])
    writer.writerow([len(services)])
    
    output.seek(0)
    return send_file(
        BytesIO(output.read().encode('utf-8')),
        as_attachment=True,
        download_name='service_count.csv',
        mimetype='text/csv'
    ), 200

@service_api.route('/services/count', methods=['GET'])
@swag_from('service_count.yml')
def service_count_():
    from api.model.models import Service
    """Return the number of existing Services"""
    services = Service.query.all()
    return jsonify({'count': len(services)}), 200

