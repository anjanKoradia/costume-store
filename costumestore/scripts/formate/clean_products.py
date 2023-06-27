import os
import numpy as np
import pandas as pd

# set directory path
DIRECTORY = "/home/anjan/Anjan/Projects/django/ecommerce-store/costumestore/scripts"

# accessing raw data file
RAW_FILE_LOCATION = "raw-data/products.csv"
raw_file = os.path.join(DIRECTORY, RAW_FILE_LOCATION)

# accessing data file
file = os.path.join(DIRECTORY, "data/products.csv")

# set unnecessary column names to drop from csv file
columns_to_remove = ["link", "no_of_ratings", "discount_price"]

# read csv file
df = pd.read_csv(raw_file, low_memory=False)

# replace category tags
df["category"] = df["category"].replace(
    {
        "women's clothing": "women",
        "men's clothing": "men",
        "bags & luggage": "accessories",
    }
)

# remove ₹ from price
df["price"] = df["price"].str.removeprefix(prefix="₹")

# convert price & rating to integer
df["price"] = pd.to_numeric(df["price"], errors="coerce", downcast="integer")
df["ratings"] = pd.to_numeric(df["ratings"], errors="coerce", downcast="integer")

# Remove rows where a price value is empty
df = df[df["price"].notnull()]

# fill 0 at empty place in ratings column
df["ratings"].fillna(0, inplace=True)

# covert float to int
df["ratings"] = df["ratings"].round().astype(int)
df["price"] = df["price"].round().astype(int)

# calculate discount and store in new column
df["discount"] = np.random.randint(9, 80, size=len(df))

# drop unnecessary column
df = df.drop(columns=columns_to_remove)

# Shuffle the data
df = df.sample(frac=1).reset_index(drop=True)

df.to_csv(file, index=False)
