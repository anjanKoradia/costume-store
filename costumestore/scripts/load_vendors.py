from accounts.models import Vendor
import csv
import os

def run():
    # accessing data file
    dataset_location = "/home/anjan/Anjan/Projects/django/ecommerce-store/costumestore/scripts/data/vendors.csv"

    with open(dataset_location) as file:
        read_file = csv.reader(file)
        count = 1
        for record in read_file:
            if count == 1:
                pass
            else:
                print(record)
        
            count += 1