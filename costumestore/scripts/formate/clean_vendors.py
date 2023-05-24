# This code is to clean raw data and convert it into desire format

import os
import pandas as pd

# set directory path
directory = "/home/anjan/Anjan/Projects/django/ecommerce-store/costumestore/scripts"

# accessing raw data file
raw_file_location = "raw-data/vendors.csv"
raw_file = os.path.join(directory, raw_file_location)

# accessing data file
file = os.path.join(directory, "data/vendors.csv")

# set unnecessary column names to drop from csv file
columns_to_remove = [
    "First_name",
    "Last_name",
    "Designation",
    "User_Mobile_alt",
    "email_id_2",
    "add2",
    "locality",
    "landmark",
    "glusr_usr_ph_area",
    "glusr_usr_ph_number",
]

# read csv file
df = pd.read_csv(raw_file)

# remove whitespace from column names
df.columns = df.columns.str.strip()
df.to_csv(raw_file, index=False)

# merge First_name and Last_name columns into name column
name = df["First_name"] + " " + df["Last_name"]
df.insert(1, "name", name)
df.to_csv(file, index=False)

# drop unnecessary column
df = df.drop(columns=columns_to_remove)
df.to_csv(file, index=False)

# rename column names ad per need
new_colums_names = {
    "Western_Wear_Retailers": "shop_name",
    "User_Mobile_1": "phone",
    "email_id_1": "email",
    "add1": "address",
    "glusr_usr_sellinterest": "bio",
    "glusr_usr_company_desc": "description",
}
df = df.rename(columns=new_colums_names)
df.to_csv(file, index=False)

# Remove rows where a email value is empty
df = df[df["email"].notnull()]
df.to_csv(file, index=False)

# Remove rows where a name value is empty
df = df[df["name"].notnull()]
df.to_csv(file, index=False)
