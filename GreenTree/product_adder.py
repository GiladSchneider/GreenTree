from config import connection, cursor
import pandas as pd

# Read in the data from excel file 'products.xlsx'
products = pd.read_excel('products.xlsx')

# Print the dataframe
print(products)

