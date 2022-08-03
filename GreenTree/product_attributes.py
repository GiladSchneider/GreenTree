from config import *
from flask import render_template, request, redirect, url_for

def get_product_attributes(product_id=None, product_attribute_id=None):
    if product_id is None and product_attribute_id is None:
        cursor.execute("SELECT * FROM product_attributes") 
    elif product_id is not None and product_attribute_id is not None:
        cursor.execute("SELECT * FROM product_attributes WHERE product_id = %s AND product_attribute_id = %s", (product_id, product_attribute_id))
    elif product_id is not None:
        cursor.execute("SELECT * FROM product_attributes WHERE product_id = %s", (product_id))
    elif product_attribute_id is not None:
        cursor.execute("SELECT * FROM product_attributes WHERE product_attribute_id = %s", (product_attribute_id))
    results = cursor.fetchall()                           
    return results

def add_product_attribute(product_id, attribute_id, attribute_value):
    cursor.execute("INSERT INTO product_attributes (product_id, attribute_id, attribute_value) VALUES (%s, %s, %s)", (product_id, attribute_id, attribute_value))
    connection.commit()
    return True

def delete_by_product_attribute(product_id=None, attribute_id=None):
    if product_id is None and attribute_id is None:
        return False
    elif product_id is not None and attribute_id is not None:
        cursor.execute("DELETE FROM product_attributes WHERE product_id = %s AND attribute_id = %s", (product_id, attribute_id))
    elif product_id is not None:
        cursor.execute("DELETE FROM product_attributes WHERE product_id = %s", (product_id))
    elif attribute_id is not None:
        cursor.execute("DELETE FROM product_attributes WHERE attribute_id = %s", (attribute_id))
    connection.commit()
    return True

# create a route for the product_attributes url
@app.route('/product_attributes/')
def product_attributes():
    # display the product_attributes
    product_attributes = get_product_attributes()
    return render_template('product_attributes.html', product_attributes=product_attributes)

# create a route for adding a product_attribute
@app.route('/product_attributes/add', methods=['GET', 'POST'])
def add_product_attribute_page():
    # if the request is a post
    if request.method == 'POST':
        # get the data from the form
        product_id = request.form['product_id']
        attribute_id = request.form['attribute_id']
        attribute_value = request.form['attribute_value']
        # add the product_attribute
        add_product_attribute(product_id, attribute_id, attribute_value)
        # redirect to the product_attributes page
        return redirect(url_for('product_attributes'))
    # if the request is a get
    else:
        # return the add product_attribute page
        return render_template('add_product_attribute.html')

# create an edit product attribute page
@app.route('/product_attributes/edit/<int:product_attribute_id>', methods=['GET', 'POST'])
def edit_product_attribute_page(product_attribute_id):
    # if the request is a post
    if request.method == 'POST':
        # get the data from the form
        product_id = request.form['product_id']
        attribute_id = request.form['attribute_id']
        attribute_value = request.form['attribute_value']
        # edit the product_attribute
        cursor.execute("UPDATE product_attributes SET product_id = %s, attribute_id = %s, attribute_value = %s WHERE product_attribute_id = %s", (product_id, attribute_id, attribute_value, product_attribute_id))
        connection.commit()
        # redirect to the product_attributes page
        return redirect(url_for('product_attributes'))
    # if the request is a get
    else:
        # get the product_attribute
        cursor.execute("SELECT * FROM product_attributes WHERE product_attribute_id = %s", (product_attribute_id,))
        results = cursor.fetchone()
        # return the edit product_attribute page
        return render_template('edit_product_attribute.html', product_attribute=results)


# create a delete product attribute page
@app.route('/product_attributes/delete/<int:product_attribute_id>')
def delete_product_attribute(product_attribute_id):
    # delete the product_attribute
    cursor.execute("DELETE FROM product_attributes WHERE product_attribute_id = %s", (product_attribute_id,))
    connection.commit()
    # redirect to the product_attributes page
    return redirect(url_for('product_attributes'))

