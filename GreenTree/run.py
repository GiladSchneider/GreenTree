from flask import Flask
from config import app
import index, strains, products, product_attributes, attributes

app.run(debug=True)