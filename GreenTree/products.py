from math import nan
from attributes import get_attributes
from config import *
from flask import render_template, request, redirect, url_for
from product_attributes import add_product_attribute, delete_by_product_attribute, get_product_attributes

def get_products():
    cursor.execute("SELECT * FROM products")    # execute a query
    results = cursor.fetchall()                 # fetch all the rows in a list of lists
    return results

def add_product(name, description, active, image_filepath=None, type=None, brand=None, price=None, discount_price=None, strain=None, strain_type=None, thc_percentage=None, size=None):
    args = [name, description, active, image_filepath, type, brand, price, discount_price, strain, strain_type, thc_percentage, size]
    cursor.execute("INSERT INTO products (product_name, product_description, product_active, product_image_filepath, product_type, product_brand, product_price, product_discount_price, product_strain, product_strain_type, product_thc_percentage, product_size) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", args)    
    connection.commit()                          # commit the changes to the database
    return True

def delete_product(id):
    cursor.execute("DELETE FROM products WHERE product_id = %s", (id))
    delete_by_product_attribute(product_id=id)
    connection.commit()
    return True

def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def secure_filename(filename):
    return filename.replace(' ', '_')

# create a route for the products url
@app.route('/products/')
def products():
    # print the list of products on the products page
    return render_template('products.html', products=get_products())

# create a route for the add_product url
@app.route('/products/add', methods=['GET', 'POST'])
def add_product_page():
    # check if the request is a POST request
    if request.method == 'POST':
        # get the values from the form
        name = request.form['name']
        description = request.form['description']
        active = request.form['active']
        image_file = request.files['image']
        # get the attributes from the select picker
        attributes = request.form.getlist('attributes')
        
        # NEW
        product_type = request.form['product_type']
        brand = request.form['brand']
        price = request.form['price']
        discount_price = request.form['discount_price']
        strain = request.form['strain']
        strain_type = request.form['strain_type']
        thc_percentage = request.form['thc_percentage']
        size = request.form['size']
        # END NEW
        
        filename = None
        db_filepath = DEFAULT_IMAGE_FILEPATH
        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            filepath = IMAGES_FOLDER + filename
            db_filepath = DATABASE_IMAGE_FOLDER + filename
            image_file.save(filepath)                                  
        # add the product to the database
        add_product(name, description, active, db_filepath, product_type, brand, price, discount_price, strain, strain_type, thc_percentage, size)
        # add the attributes to the product
        product_id = cursor.lastrowid        
        for attribute_id in attributes:
            add_product_attribute(product_id=product_id, attribute_id=attribute_id, attribute_value='No Value')

        return redirect(url_for('products'))
    
    # return the add_product page
    display_attributes = get_attributes()
    return render_template('add_product.html', attributes=display_attributes, product_types=PRODUCT_TYPES)

# create a route for the delete_product url
@app.route('/products/delete/<product_id>')
def delete_product_page(product_id):
    delete_product(product_id)             # delete the product
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
        image_file = request.files['image']
        product_type = request.form['product_type']
        brand = request.form['brand']
        price = request.form['price']
        discount_price = request.form['discount_price']
        strain = request.form['strain']
        strain_type = request.form['strain_type']   
        thc_percentage = request.form['thc_percentage']
        size = request.form['size']


        # change the product image if the user uploaded a new image
        db_filepath = DEFAULT_IMAGE_FILEPATH
        if image_file and allowed_file(image_file.filename) and image_file.filename != 'default_product_image.png':
            filename = secure_filename(image_file.filename)
            filepath = IMAGES_FOLDER + filename
            db_filepath = DATABASE_IMAGE_FOLDER + filename
            image_file.save(filepath)
            cursor.execute("UPDATE products SET product_image_filepath = %s WHERE product_id = %s", (db_filepath, product_id))


        # update the product in the database
        cursor.execute("UPDATE products SET product_name = %s, product_description = %s, product_active = %s, product_type = %s, product_brand = %s, product_price = %s, product_discount_price = %s, product_strain = %s, product_strain_type = %s, product_thc_percentage = %s, product_size = %s WHERE product_id = %s", (name, description, active, product_type, brand, price, discount_price, strain, strain_type, thc_percentage, size, product_id))
        connection.commit()
        # return the products page
        return redirect(url_for('products'))
    
    # get the product from the database
    cursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id))
    results = cursor.fetchone()

    # get the attributes
    attributes = get_attributes()

    # grab a list of product brands from the database
    cursor.execute("SELECT DISTINCT product_brand FROM products")
    brands = cursor.fetchall()
    
    # return the edit_product page
    return render_template('edit_product.html', product=results, attributes=attributes, product_types=PRODUCT_TYPES, brands=brands)
