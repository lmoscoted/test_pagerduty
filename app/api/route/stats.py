from flask import Blueprint,render_template
from flasgger import swag_from


from api.service.graph import generate_graph


stats = Blueprint('stats', __name__)


@stats.route('/stats/services', methods=['GET'])
@swag_from('service_analysis_graph.yml')
def service_analysis_graph():
    image_data = generate_graph()
    return render_template('index.html', image_data=image_data)
