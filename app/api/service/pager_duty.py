import logging as log

from api.service.api_requests import PagerDutyAPI
from api.service.data_storage import DataStorage
from database import SessionLocal


class PagerDutyService:
    from config import Config

    def __init__(self, base_url=Config.PAGER_DUTY_URL, token_api=Config.PAGERDUTY_API_KEY):
        self.api = PagerDutyAPI(base_url, token_api)
        self.data_storage = DataStorage(SessionLocal())
    

    async def fetch_and_store_data(self):
        try:
            # Fetch data from PagerDuty API
            incidents_data = await self.api.fetch_incidents_with_pagination()
            services_data = await self.api.fetch_services_with_pagination()
            teams_data = await self.api.fetch_teams_with_pagination()
            escalation_policies_data = await self.api.fetch_escalation_policies_with_pagination()

            log.info('Data fetched from Pagerduty API')

            # Store data in database
            self.data_storage._store_teams(teams_data)
            self.data_storage._store_escalation_policies(escalation_policies_data)
            self.data_storage._store_services(services_data)
            self.data_storage._store_incidents(incidents_data)
            
            # Commit changes to database
            self.data_storage.session.commit()
            log.info('Data from Pagerduty API saved in Database')
            return True

        except Exception as e:
            # Log error
            log.error(f"Error fetching and storing data: {e}")

            # Roll back changes to database
            self.data_storage.session.rollback()
            return False