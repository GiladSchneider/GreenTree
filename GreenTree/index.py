from config import *
from flask import render_template
from config import *

@app.route('/')
@app.route('/index/')
@app.route('/home/')
def index():
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    return render_template('index.html', products=products)