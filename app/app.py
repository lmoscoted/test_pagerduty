import uuid
import asyncio

from flask import Flask
from flask_migrate import Migrate
from flask_apscheduler import APScheduler
from flasgger import Swagger

from config import Config
from api.route.service import service_api
from api.route.incident import incident_api
from api.route.team import team_api
from api.route.escalation_policy import escalation_policy_api 
from api.route.stats import stats
from database import db


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

migrate = Migrate(app, db)

scheduler = APScheduler()

# Registering the endpoint
app.register_blueprint(service_api)
app.register_blueprint(incident_api)
app.register_blueprint(team_api)
app.register_blueprint(escalation_policy_api)
app.register_blueprint(stats)

# Configuring Swagger
app.config['SWAGGER'] = {
    'title': 'Pagerduty Dashboard Test',
    'uiversion': 3
}
swagger = Swagger(app)


# Function for the scheduler that fetchs and store the data
def extract_load_job():
    from api.service.pager_duty import PagerDutyService as pd_service
    print('Starting Job')
    res = asyncio.run(pd_service().fetch_and_store_data())
    if res:
        print("Data extracted and loaded into DB")
    else:
        print("Data extraction/loading failed")


if __name__ == "__main__":
    # Schedule the job for extracting data from the API and storing into Database.
    scheduler.add_job(func=extract_load_job, trigger='interval',
                      hours=Config.REFRESH_DATA_RATE,id=uuid.uuid4().hex)
    
    print(f"Job for fetching and storing data to the Database will run in {Config.REFRESH_DATA_RATE} hours")
    scheduler.start()
    
    app.run(host='0.0.0.0', port=5000, debug=Config.DEBUG_MODE)



