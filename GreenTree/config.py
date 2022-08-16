from pymysql import connect, cursors
from flask import Flask
from os import listdir

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
ICONS_FOLDER = 'GreenTree/static/svg_icons/'
DATABASE_ICONS_FOLDER = '/static/svg_icons/' 

# get all the file names from the svg_icons folder
TEMP_icons_list = []
for file in listdir(ICONS_FOLDER):
    if file.endswith(".svg"):
        TEMP_icons_list.append(file)
icons_list = [DATABASE_ICONS_FOLDER + icon for icon in TEMP_icons_list]
                                