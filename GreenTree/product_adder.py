import os
from os import listdir, rename
from config import cursor
from numpy.random import choice
from products import add_product
from product_attributes import add_product_attribute
from attributes import add_attribute
import pandas as pd

# Read in the data from excel file 'products.xlsx'
products = pd.read_excel('products.xlsx')
# replace nan with None
products = products.where((pd.notnull(products)), None)

# grab the list of column names
column_names = products.columns.tolist()

# create a list of products, each product is a dictionary
products_list = []
for index, row in products.iterrows():
    # create a dictionary to hold the product attributes
    product = {}
    # add the product attributes to the product dictionary
    for column_name in column_names:
        product[column_name] = row[column_name]
        
        if type(product[column_name]) == str:
            product[column_name] = product[column_name].strip()
 
    # add the product to the products list
    products_list.append(product)

# read all the file names from the folder "Standard Weed Pics" and save them to a list
file_names = []
for file_name in listdir("GreenTree/static/standard_images"):
    file_names.append("/static/standard_images/" + file_name)

# insert the products into the database
for product in products_list:

    add_product(product['Name'],
                product['Description'],
                1,
                image_filepath = choice(file_names),
                type = product['Product Type'],
                brand = product['Brand'],
                price = (product['Price']) if not pd.isnull(product['Price']) else None, 
                discount_price = product['Discounted Price'] if not pd.isnull(product['Discounted Price']) else None, 
                strain = product['Strain'], 
                strain_type = product['Strain Type'], 
                thc_percentage = product['THC %'] if not pd.isnull(product['THC %']) else None,
                size = product['Size'],
                strain_description=product['Strain Description'] if not pd.isnull(product['Strain Description']) else None
                )

    # add the attributes to the product    
    attributes = [product['Attribute 1'], product['Attribute 2'], product['Attribute 3'], product['Attribute 4']] 
    product_id = cursor.lastrowid

    for attribute in attributes:
        if not pd.isnull(attribute):
            # check if the attribute is in the attributes database. If not, add it.
            cursor.execute("SELECT * FROM attributes WHERE attribute_name = %s", (attribute))
            if cursor.rowcount == 0:
                default_desc = "No description"
                default_attr_active = 1
                add_attribute(attribute, default_desc, default_attr_active)

            # get the attribute_id
            cursor.execute("SELECT attribute_id FROM attributes WHERE attribute_name = %s", (attribute))
            attribute_id = cursor.fetchone()['attribute_id']
            # add the product attribute
            add_product_attribute(product_id, attribute_id, attribute_value='No Value')