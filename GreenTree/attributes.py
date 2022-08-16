from config import *
from flask import request, render_template, redirect, url_for
from product_attributes import delete_by_product_attribute

def get_attributes():
    cursor.execute("SELECT * FROM attributes")    # execute a query
    results = cursor.fetchall()                   # fetch all the rows in a list of lists
    return results

# create an add attribute function
def add_attribute(attribute_name, attribute_description, attribute_active, attribute_type="general", icon_filename=DATABASE_ICONS_FOLDER+"default_icon.svg"):
    cursor.execute("INSERT INTO attributes (attribute_name, attribute_description, attribute_active, attribute_type, attribute_icon_filename) VALUES (%s, %s, %s, %s, %s)", (attribute_name, attribute_description, attribute_active, attribute_type, icon_filename))
    connection.commit()
    return True

def delete_attribute(attribute_id):
    cursor.execute("DELETE FROM attributes WHERE attribute_id = %s", (attribute_id))
    delete_by_product_attribute(attribute_id=attribute_id)
    connection.commit()
    return True

# create a route for the attributes url
@app.route('/attributes/')
def attributes():
    # display the attributes
    attributes = get_attributes()
    return render_template('attributes.html', attributes=attributes)

# create a route for adding an attribute
@app.route('/attributes/add/', methods=['GET', 'POST'])
def add_attribute_page():
    # if the request is a post
    if request.method == 'POST':
        # get the data from the form
        attribute_name = request.form['attribute_name']
        attribute_description = request.form['attribute_description']
        attribute_active = request.form['attribute_active']
        attribute_type = request.form['attribute_type']
        icon_filename = request.form['icon_filename']
        # add the attribute
        add_attribute(attribute_name, attribute_description, attribute_active, attribute_type, icon_filename)
        # redirect to the attributes page
        return redirect(url_for('attributes'))
    # if the request is a get
    else:
        # return the add attribute page
        return render_template('add_attribute.html', icons_list=icons_list)

# create a route for editing an attribute
@app.route('/attributes/edit/<int:attribute_id>', methods=['GET', 'POST'])
def edit_attribute_page(attribute_id):
    # if the request is a post
    if request.method == 'POST':
        # get the data from the form
        attribute_name = request.form['attribute_name']
        attribute_description = request.form['attribute_description']
        attribute_active = request.form['attribute_active']
        attribute_type = request.form['attribute_type']
        icon_filename = request.form['icon_filename']
        # edit the attribute
        cursor.execute("UPDATE attributes SET attribute_name = %s, attribute_description = %s, attribute_active = %s, attribute_type = %s, attribute_icon_filename = %s WHERE attribute_id = %s", (attribute_name, attribute_description, attribute_active, attribute_type, icon_filename, attribute_id))
        connection.commit()
        # redirect to the attributes page
        return redirect(url_for('attributes'))
    # if the request is a get
    else:
        # get the attribute
        cursor.execute("SELECT * FROM attributes WHERE attribute_id = %s", (attribute_id,))
        results = cursor.fetchone()
        # return the edit attribute page
        return render_template('edit_attribute.html', attribute=results, icons_list=icons_list)

# create a route for deleting an attribute
@app.route('/attributes/delete/<int:attribute_id>')
def delete_attribute_page(attribute_id):
    # delete the attribute
    delete_attribute(attribute_id)
    # redirect to the attributes page
    return redirect(url_for('attributes'))