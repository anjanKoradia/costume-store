from accounts.models import Vendor
from authentication.models import User
import csv
import os


def run():
    # accessing data file
    directory = os.path.dirname(__file__)
    dataset_location = os.path.join(directory, "data/vendors.csv")

    with open(dataset_location) as file:
        read_file = csv.reader(file)
        count = 1
        User.objects.exclude(role="admin").delete()
        for record in read_file:
            if count != 1:
                try:
                    user = User.objects.create_user(
                        email=record[3], 
                        password="Vendor@123", 
                        name=record[1], 
                        phone=record[2],
                        role="vendor",
                        is_active = True
                    )
                    
                    if user:
                        vendor = Vendor.objects.get(user=user)
                        vendor.shop_name = record[0]
                        vendor.save()
                        
                        print(f"Vendors:[{user.name}] added successfully")
                
                except Exception as e:
                    print(e, record)

            count += 1
