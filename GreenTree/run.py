from flask import Flask, render_template
from config import app
from views import strains, products, product_attributes, attributes

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

app.run(debug=True)