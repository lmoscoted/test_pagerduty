import io
import base64

import matplotlib.pyplot as plt


def generate_graph():
    from api.model.models import Incident, Service
    from database import SessionLocal as session

    # Query database and prepare data
    services = session.query(Service).all()
    service_names = [service.name for service in services]
    incident_counts = []
    incident_status_counts = {}

    for service in services:
        incidents = session.query(Incident).filter(Incident.service_id == service.id).all()
        incident_counts.append(len(incidents))
        incident_status_counts[service.name] = {}
        for incident in incidents:
            if incident.status not in incident_status_counts[service.name]:
                incident_status_counts[service.name][incident.status] = 0
            incident_status_counts[service.name][incident.status] += 1

    # Create the bar chart
    fig, ax = plt.subplots(2, 1, figsize=(12, 14))

    ax[0].bar(service_names, incident_counts)
    ax[0].set_xlabel('Service')
    ax[0].set_ylabel('Incident Count')
    ax[0].set_title('Incident Counts by Service')

    for i, service in enumerate(service_names):
        ax[1].bar(incident_status_counts[service].keys(), incident_status_counts[service].values(), label=service)

    ax[1].set_xlabel('Status')
    ax[1].set_ylabel('Incident Count')
    ax[1].set_title('Incident Status Breakdown by Service')
    ax[1].legend()

    # Save the graph to a BytesIO buffer
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    plt.close()

    # Encode the image
    image_data = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
    return image_data