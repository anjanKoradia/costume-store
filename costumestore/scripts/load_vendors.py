from authentication.models import User
from accounts.models import Address
from accounts.models import Vendor
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
                        vendor = Vendor.objects.update_or_create(
                            user=user,
                            defaults={
                                "shop_name":record[0],
                                "bio":record[10],
                                "description":record[11],
                            }
                        )
    
                        address = Address.objects.update_or_create(
                            user=user,
                            defaults={
                                "address": record[4],
                                "city": record[5],
                                "state": record[6],
                                "pin_code": record[7],
                                "country":record[8]
                            }
                        )
                        
                        print(f"Vendors:[{user.name}] added successfully")
                
                except Exception as e:
                    print(e, record)

            count += 1
