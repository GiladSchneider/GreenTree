from pymysql import connect, cursors
from flask import Flask

app = Flask(__name__)

# create a connection to the database
connection = connect(host='localhost',
                                user='root',
                                password='password',
                                db='GreenTree',
                                charset='utf8mb4',
                                cursorclass=cursors.DictCursor)

cursor = connection.cursor()

IMAGES_FOLDER = 'GreenTree/static/'
DATABASE_IMAGE_FOLDER = '/static/'
DEFAULT_IMAGE_FILEPATH = '/static/default_product_image.png'

PRODUCT_TYPES = ["Vape Cartridge",
                "Edible", 
                "Beverage",
                "Gunnies",
                "Equipment",
                "Other"]          
                                