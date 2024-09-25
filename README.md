# Back End Take Home Exercise

## Objective

Using the [pdt-agonzalezlucena] instance, demonstrate your ability to manage the everyday labor as a CSG Innovation Team Member and demonstrate the capacity to create and manage a successful backend app with the proper tools. As part of the interview process, a demonstration of the work performed and operational use of PagerDuty with the various integrations you implemented will be expected.

## Exercise

A senior executive at PagerDuty wants a dashboard to analyze the data contained in the above instance. To accomplish this, he must use the  API Key: [u+b4CCjDZsXfuxx-w_fw] to interact with the PagerDuty API endpoints and provide the necessary backend to feed the dashboard. To accomplish this, you will need to extract data from the API and store it in a MySQL database for further analysis, being able to present the data as follows:

* The number of existing Services
* Number of Incidents per Service
* Number of Incidents by Service and Status
* Number of Teams and their related Services
* Number of Escalation Policies and their Relationship with Teams and Services
* CSV report of each of the above points.
* Analysis of which Service has more Incidents and breakdown of Incidents by status.
* Graph reflecting the previous point.

## Introduction

This application is a backend dashboard that extracts data from the PagerDuty API and stores it in a MySQL database for further analysis. The application uses Python, Flask, SQLAlchemy, MySQL, Docker, nginx, and Appscheduler to provide a scalable and reliable solution.

## Installation

### Prerequisites

* Docker
* Docker Compose

> **Note:** You need to copy the .env.DEV file that is in the root directory and rename it as .env using you own environment variables.

 

### Building and Running the App Containers

To build and run the app containers, run the following command:
```bash
docker-compose up --build
```
This will build the Docker images and start the containers.

###  Initializing the Database
Once the app and the *database* are up and running, you should run the following command in a terminal to initialize the database:

```bash
docker-compose exec app bash -c "python init_db.py"
```
This will create the necessary tables in the database.

### Data Extracting and Loading
The app extracts data from the following PagerDuty Endpoints:

- https://api.pagerduty.com/services
- https://api.pagerduty.com/incidents
- https://api.pagerduty.com/teams
- https://api.pagerduty.com/escalation_policies

The app uses a PagerDuty API Key.

The app has a job scheduler (Appscheduler) that runs the data extraction and loading job defined in the **REFRESH_DATA_RATE** environment variable in the .env file. Notice that this is defined in hours. For this app it was set to 2 hours. 
But, in the first time when running the app, you can run this command in a terminal for extracting and populating the database with the Pageduty instance data inmediately without needing to wait until the job is completed:

```bash
docker-compose exec app bash -c "python extract_load.py"
```
## Usage
Now you can access to these endpoints for downloading the csv reports:
* http://localhost/api/v1/incidents/by-service-and-status/csv

*  http://localhost/api/v1/escalation-policies/with-teams-and-services/csv

* http://localhost/api/v1/incidents/by-service/csv

* http://localhost/api/v1/services/count/csv

* http://localhost/api/v1/teams/with-services/csv

Also you can you can view in an HTML page the analysis of which Service has more Incidents and breakdown of Incidents by status:

*  http://localhost/stats/services  

You should see something like:


![Service analysis graph](https://res.cloudinary.com/dp5eaxjjj/image/upload/v1727268393/services-graph.png)


Optionally, you can access to the below ones for getting the results as a json response. 
* http://localhost/api/v1/incidents/by-service-and-status
* http://localhost/api/v1/incidents/by-service
* http://localhost/api/v1/services/count
* http://localhost/api/v1/teams/with-services
* http://localhost/api/v1/escalation-policies/with-teams-and-services

## API Documentation
For the API documentation you can access to:
http://localhost/apidocs

## Testing
For testing you should stop the running containers, if any, and start the application:
```bash
docker-compose stop
```
Then start again the containers
```bash
docker-compose up  or  docker-compose up --build
```

For running the unit tests:
```bash
docker-compose exec app bash -c "python init_db.py && python -m pytest test/unit"
```

For running the integration tests:
```bash
docker-compose exec app bash -c "python init_db.py && python -m pytest test/integration"
```


## Additional Notes
* The data in the database is not being persisted.
* Sometimes could be needed recreate completely the containers:
```bash
 docker-compose up --build --force-recreate
```


