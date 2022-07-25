from flask import Flask, render_template
from config import app
from views import index, strains, products, product_attributes, attributes

app.run(debug=True)