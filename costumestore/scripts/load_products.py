from accounts.models import Vendor
from vendor.models import Product
import math
import csv
import os


def run():
    # accessing data file
    directory = os.path.dirname(__file__)
    dataset_location = os.path.join(directory, "data/products.csv")

    with open(dataset_location) as file:
        read_file = csv.reader(file)
        products = list(read_file)
        products_per_vendor = math.floor((len(products) / Vendor.objects.all().count()))

        Product.objects.all().delete()

        for index, vendor in enumerate(Vendor.objects.all()):
            for i in range(
                products_per_vendor * index, products_per_vendor * (index + 1)
            ):
                if i == 0:
                    pass
                else:
                    try:
                        product = Product.objects.create(
                            vendor=vendor,
                            name=products[i][0],
                            category=products[i][1],
                            subcategory=products[i][2],
                            images=[{"url": products[i][3]}],
                            rating=products[i][4],
                            price=products[i][5],
                            discount=products[i][6],
                        )

                        print(f"Product:[{product.name}] added successfully")
                    except Exception as e:
                        print(e, products[i])
