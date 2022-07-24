from config import *
from flask import request, render_template, redirect, url_for

def get_attributes():
    cursor.execute("SELECT * FROM attributes")    # execute a query
    results = cursor.fetchall()                   # fetch all the rows in a list of lists
    return results

# create an add attribute function
def add_attribute(attribute_name, attribute_description, attribute_active):
    cursor.execute("INSERT INTO attributes (attribute_name, attribute_description, attribute_active) VALUES (%s, %s, %s)", (attribute_name, attribute_description, attribute_active))
    connection.commit()
    return True

# create a route for the attributes url
@app.route('/attributes/')
def attributes():
    # display the attributes
    attributes = get_attributes()
    return render_template('attributes/attributes.html', attributes=attributes)

# create a route for adding an attribute
@app.route('/attributes/add/', methods=['GET', 'POST'])
def add_attribute_page():
    # if the request is a post
    if request.method == 'POST':
        # get the data from the form
        attribute_name = request.form['attribute_name']
        attribute_description = request.form['attribute_description']
        attribute_active = request.form['attribute_active']
        # add the attribute
        add_attribute(attribute_name, attribute_description, attribute_active)
        # redirect to the attributes page
        return redirect(url_for('attributes'))
    # if the request is a get
    else:
        # return the add attribute page
        return render_template('attributes/add_attribute.html')

# create a route for editing an attribute
@app.route('/attributes/edit/<int:attribute_id>', methods=['GET', 'POST'])
def edit_attribute_page(attribute_id):
    # if the request is a post
    if request.method == 'POST':
        # get the data from the form
        attribute_name = request.form['attribute_name']
        attribute_description = request.form['attribute_description']
        attribute_active = request.form['attribute_active']
        # edit the attribute
        cursor.execute("UPDATE attributes SET attribute_name = %s, attribute_description = %s, attribute_active = %s WHERE attribute_id = %s", (attribute_name, attribute_description, attribute_active, attribute_id))
        connection.commit()
        # redirect to the attributes page
        return redirect(url_for('attributes'))
    # if the request is a get
    else:
        # get the attribute
        cursor.execute("SELECT * FROM attributes WHERE attribute_id = %s", (attribute_id,))
        results = cursor.fetchone()
        # return the edit attribute page
        return render_template('attributes/edit_attribute.html', attribute=results)

# create a route for deleting an attribute
@app.route('/attributes/delete/<int:attribute_id>')
def delete_attribute(attribute_id):
    # delete the attribute
    cursor.execute("DELETE FROM attributes WHERE attribute_id = %s", (attribute_id,))
    connection.commit()
    # redirect to the attributes page
    return redirect(url_for('attributes'))