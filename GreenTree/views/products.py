from config import *
from flask import render_template, request, redirect, url_for

def get_products():
    cursor.execute("SELECT * FROM products")    # execute a query
    results = cursor.fetchall()                 # fetch all the rows in a list of lists
    return results

def add_product(name, description, active):
    cursor.execute("INSERT INTO products (product_name, product_description, product_active) VALUES (%s, %s, %s)", (name, description, active))
    connection.commit()
    return True

def delete_product(id):
    cursor.execute("DELETE FROM products WHERE product_id = %s", (id))
    connection.commit()
    return True

# create a route for the products url
@app.route('/products/')
def products():
    # print the list of products on the products page
    return render_template('products/products.html', products=get_products())

# create a route for the add_product url
@app.route('/products/add', methods=['GET', 'POST'])
def add_product_page():
    # check if the request is a POST request
    if request.method == 'POST':
        # get the values from the form
        name = request.form['name']
        description = request.form['description']
        active = request.form['active']
        # add the product to the database
        add_product(name, description, active)
        # return the products page
        return redirect(url_for('products'))
    
    # return the add_product page
    return render_template('products/add_product.html')

# create a route for the delete_product url
@app.route('/products/delete/<product_id>')
def delete_product_page(product_id):
    delete_product(product_id)                         # delete the product    
    return redirect(url_for('products'))   # redirect to the products page

# create a route for the edit_product url
@app.route('/products/edit/<product_id>', methods=['GET', 'POST'])
def edit_product_page(product_id):
    # check if the request is a POST request
    if request.method == 'POST':
        # get the values from the form
        name = request.form['name']
        description = request.form['description']
        active = request.form['active']
        # update the product in the database
        cursor.execute("UPDATE products SET product_name = %s, product_description = %s, product_active = %s WHERE product_id = %s", (name, description, active, product_id))
        connection.commit()
        # return the products page
        return redirect(url_for('products'))
    
    # get the product from the database
    cursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id))
    results = cursor.fetchone()
    # return the edit_product page
    return render_template('products/edit_product.html', product=results)
