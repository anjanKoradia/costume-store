import csv
import os
from authentication.models import User
from accounts.models import Address
from accounts.models import Vendor


def run():
    """
    Import vendors from a CSV file and create corresponding User, Vendor, and Address objects.

    This function reads a CSV file containing vendor data, creates User objects with role 'vendor',
    and associates Vendor and Address objects with the created User. The User objects are created
    using the specified CSV fields, and the Vendor and Address objects are updated or created
    based on the User association.
    """
    # accessing data file
    directory = os.path.dirname(__file__)
    dataset_location = os.path.join(directory, "data/vendors.csv")

    with open(dataset_location, encoding="utf-8") as file:
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
                        is_active=True,
                    )

                    if user:
                        Vendor.objects.update_or_create(
                            user=user,
                            defaults={
                                "shop_name": record[0],
                                "bio": record[10],
                                "description": record[11],
                            },
                        )
                        Address.objects.update_or_create(
                            user=user,
                            defaults={
                                "address": record[4],
                                "city": record[5],
                                "state": record[6],
                                "pin_code": record[7],
                                "country": record[8],
                            },
                        )

                        print(f"Vendors:[{user.name}] added successfully")

                except Exception as e:
                    print(e, record)

            count += 1
