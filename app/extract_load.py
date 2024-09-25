import asyncio


# Function that fetchs and store the data
def extract_load_job():
    from api.service.pager_duty import PagerDutyService as pd_service
    print('Starting Job')
    res = asyncio.run(pd_service().fetch_and_store_data())
    if res:
        print("Data extracted and loaded into DB")
    else:
        print("Data extraction/loading failed")


if __name__ == "__main__":
    extract_load_job()