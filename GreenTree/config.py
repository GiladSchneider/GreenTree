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