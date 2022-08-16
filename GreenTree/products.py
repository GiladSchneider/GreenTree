from unicodedata import name
from numpy import random
from attributes import get_attributes
from config import *
from flask import render_template, request, redirect, url_for
from product_attributes import add_product_attribute, delete_by_product_attribute, get_product_attributes
from datetime import date, datetime

def get_products():
    cursor.execute("SELECT * FROM products")    # execute a query
    results = cursor.fetchall()                 # fetch all the rows in a list of lists
    return results

def add_product(name, description, active, image_filepath=None, type=None, brand=None, price=None, discount_price=None, strain=None, strain_type=None, thc_percentage=None, size=None, weight=None, strain_terpenes=None, strain_taste=None, strain_description=None):
    product_rating = random.randint(1, 5)
    product_reviews = random.randint(1, 20)
    strain_rating = random.randint(1, 5)
    strain_reviews = random.randint(1, 20)
    
    args = [name, description, active, image_filepath, 
            type, brand, price, discount_price, 
            strain, strain_type, thc_percentage, 
            size, weight, strain_terpenes, strain_taste, 
            product_rating, product_reviews, strain_rating, strain_reviews, 
            strain_description]
    cursor.execute("""INSERT INTO products 
    (product_name, product_description, product_active, product_image_filepath, 
    product_type, product_brand, product_price, product_discount_price, 
    product_strain, product_strain_type, product_thc_percentage,
    product_size, product_weight, product_strain_terpenes, product_strain_taste, 
    product_rating, product_reviews, product_strain_rating, product_strain_reviews,
    product_strain_description)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", args)
    connection.commit()
    return cursor.lastrowid

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
        weight = request.form['weight']
        strain_terpenes = request.form['strain_terpenes']
        strain_taste = request.form['strain_taste']
        strain_description = request.form['strain_description']
        # END NEW
        
        filename = None
        db_filepath = DEFAULT_IMAGE_FILEPATH
        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            filepath = IMAGES_FOLDER + filename
            db_filepath = DATABASE_IMAGE_FOLDER + filename
            image_file.save(filepath)                                  
        # add the product to the database
        add_product(name, description, active, db_filepath, product_type, brand, price, discount_price, strain, strain_type, thc_percentage, size, weight, strain_terpenes, strain_taste, strain_description)
        # add the attributes to the product
        product_id = cursor.lastrowid        
        for attribute_id in attributes:
            add_product_attribute(product_id=product_id, attribute_id=attribute_id, attribute_value='No Value')

        return redirect(url_for('products'))
    
    # return the add_product page
    display_attributes = get_attributes()

    # get a list of unique brand names from the database
    cursor.execute("SELECT DISTINCT product_brand FROM products")
    brands = cursor.fetchall()

    # get a list of unique product types from the database
    cursor.execute("SELECT DISTINCT product_type FROM products")
    product_types = cursor.fetchall()

    # get a list of unique strains from the database
    cursor.execute("SELECT DISTINCT product_strain FROM products")
    strains = cursor.fetchall()

    # get a list of unique strain types from the database
    cursor.execute("SELECT DISTINCT product_strain_type FROM products")
    strain_types = cursor.fetchall()

    # get a list of unique strain terpenes from the database
    cursor.execute("SELECT DISTINCT product_strain_terpenes FROM products")
    strain_terpenes = cursor.fetchall()

    # get a list of unique strain tastes from the database
    cursor.execute("SELECT DISTINCT product_strain_taste FROM products")
    strain_tastes = cursor.fetchall()

    return render_template('add_product.html', 
                            attributes=display_attributes, 
                            product_types=product_types, 
                            brands=brands, 
                            strains=strains, 
                            strain_types=strain_types,
                            strain_terpenes=strain_terpenes,
                            strain_tastes=strain_tastes)

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
        weight = request.form['weight']
        strain_terpenes = request.form['strain_terpenes']
        strain_taste = request.form['strain_taste']
        strain_description = request.form['strain_description']

        # change the product image if the user uploaded a new image
        db_filepath = DEFAULT_IMAGE_FILEPATH
        if image_file and allowed_file(image_file.filename) and image_file.filename != 'default_product_image.png':
            filename = secure_filename(image_file.filename)
            filepath = IMAGES_FOLDER + filename
            db_filepath = DATABASE_IMAGE_FOLDER + filename
            image_file.save(filepath)
            cursor.execute("UPDATE products SET product_image_filepath = %s WHERE product_id = %s", (db_filepath, product_id))

        # update the product in the database
        cursor.execute("""UPDATE products SET product_name = %s,
                                              product_description = %s,
                                              product_active = %s,
                                              product_type = %s,
                                              product_brand = %s,
                                              product_price = %s,
                                              product_discount_price = %s,
                                              product_strain = %s,
                                              product_strain_type = %s,
                                              product_thc_percentage = %s,
                                              product_size = %s,
                                              product_weight = %s,
                                              product_strain_terpenes = %s,
                                              product_strain_taste = %s,
                                              product_strain_description = %s
                                              WHERE product_id = %s""", (name, description, active, product_type, brand, price, discount_price, strain, strain_type, thc_percentage, size, weight, strain_terpenes, strain_taste, strain_description, product_id))
        
        # get the attributes from the select picker
        attributes = request.form.getlist('attributes')
         # add the attributes to the product     
        for attribute_id in attributes:
            add_product_attribute(product_id=product_id, attribute_id=attribute_id, attribute_value='No Value')

        connection.commit()
        # return the products page
        return redirect(url_for('products'))
    
    # get the product from the database
    cursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id))
    results = cursor.fetchone()

    # get the attributes
    attributes = get_attributes()
    
    # get the product attributes from the database
    cursor.execute("SELECT * FROM product_attributes WHERE product_id = %s", (product_id))
    product_attributes = cursor.fetchall()
    # remove the product attributes from the attributes list
    cleaned_attributes = []
    seen_attributes = {}
    for product_attribute in product_attributes:
        seen_attributes[product_attribute['attribute_id']] = True
    for attribute in attributes:        
        if attribute['attribute_id'] not in seen_attributes:
            cleaned_attributes.append(attribute)
    attributes = cleaned_attributes

    # grab a list of product brands from the database
    cursor.execute("SELECT DISTINCT product_brand FROM products")
    brands = cursor.fetchall()
    
    # get a list of unique product types from the database
    cursor.execute("SELECT DISTINCT product_type FROM products")
    product_types = cursor.fetchall()

    # get a list of unique strains from the database
    cursor.execute("SELECT DISTINCT product_strain FROM products")
    strains = cursor.fetchall()

    # get a list of unique strain types from the database
    cursor.execute("SELECT DISTINCT product_strain_type FROM products")
    strain_types = cursor.fetchall()

    # return the edit_product page
    return render_template('edit_product.html', 
                            product=results,
                            attributes=attributes, 
                            product_types=product_types, 
                            brands=brands, 
                            strains=strains, 
                            strain_types=strain_types)

# create a route for the view_product url
@app.route('/products/view/<product_id>', methods=['GET', 'POST'])
def view_product_page(product_id):

    # check if the request is a POST request
    if request.method == 'POST':
        # get the review from the form
        rating = request.form['rate']
        content = request.form['review_content']
        date = datetime.now()
        email = request.form['review_email']
        name = request.form['review_name']

        all = [rating, content, date, email, name, product_id]
        
        # insert the review into the database
        cursor.execute("INSERT INTO reviews (review_rating, review_text, review_date, review_email, review_name, product_id) VALUES (%s, %s, %s, %s, %s, %s)", all)
        connection.commit()

    # get product information from the database
    cursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id))
    product_info = cursor.fetchone()

    # get 5 random products from the database
    cursor.execute("SELECT * FROM products ORDER BY RAND() LIMIT 5")
    related_products = cursor.fetchall()

    # get the reviews for the product
    cursor.execute(f"SELECT * FROM reviews WHERE product_id = {product_id}")
    reviews=cursor.fetchall()

    # get the products attributes from the database
    cursor.execute("SELECT * FROM product_attributes WHERE product_id = %s", (product_id))
    product_attribute_ids = cursor.fetchall()

    attributes = []
    for product_attribute_id in product_attribute_ids:
        cursor.execute("SELECT * FROM attributes WHERE attribute_id = %s", (product_attribute_id['attribute_id']))
        attributes.append(cursor.fetchone())

    return render_template('view_product.html', product=product_info, related_products=related_products, reviews=reviews, icons_list=icons_list, attributes=attributes)

# create a route for the search products url
@app.route('/index/search/<database>/<category>/<query>', methods=['GET', 'POST'])
def search_type(database, category, query):
    sql_query = f"""SELECT * FROM {database} WHERE {category} = '{query}'"""
    print('\n', sql_query, '\n')
    print('SUCCESS')
    # get the products that match the search query
    cursor.execute(sql_query)
    results = cursor.fetchall()

    # if we are searching product attributes, return the correcponding products
    new_results = []
    if database == 'product_attributes':
        for result in results:
            cursor.execute("SELECT * FROM products WHERE product_id = %s", (result['product_id']))
            new_results.append(cursor.fetchone())
        results = new_results
    
    return render_template('index.html', products=results)


    
       