"""
Methods to populate the PostgreSQL database using the data in .csv files before running the APIs.
"""

import csv
import os
from mystore.models import StoreTimezone, StoreTiming, StoreStatusLog, StoreStatus
from main.settings import BASE_DIR

def create_store_data():
    print("1")

    filepath = os.path.join(BASE_DIR, "scripts/data/store_timezone.csv")
    with open(filepath) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # print(row)
            StoreTimezone.objects.create(
                store_id=row['store_id'],
                timezone_str=row['timezone_str'],
            )

def populate_store_start_end_time():
    print("2")

    filepath = os.path.join(BASE_DIR, "scripts/data/menu_hours.csv")
    with open(filepath) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # print(row)
            store = StoreTimezone.objects.filter(store_id=row['store_id']).first()
            if store:
                store_timing = StoreTiming.objects.create(
                    store=store,
                    day=row['day'],
                    start_time=row['start_time_local'],
                    end_time=row['end_time_local'],
                )
                # print(store_timing)

def create_store_status_log():
    print("3")
    filepath = os.path.join(BASE_DIR, "scripts/data/store_status.csv")
    with open(filepath) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            store = StoreTimezone.objects.filter(store_id=row['store_id']).first()
            status = StoreStatus.ACTIVE if row['status'] == 'active' else StoreStatus.INACTIVE
            timestamp = row['timestamp_utc'][:len(row['timestamp_utc'])-4]
            if store:
                status_log = StoreStatusLog.objects.create(
                    store=store,
                    status=status,
                    timestamp=timestamp
                )
                # print(status_log)

def run():
    create_store_data()
    populate_store_start_end_time()
    create_store_status_log()