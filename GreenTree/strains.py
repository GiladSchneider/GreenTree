from config import *
from flask import Blueprint, render_template, request, redirect, url_for

# create a route for the strains url
@app.route('/strains/')
def strains():
    # return the strains page
    return render_template('strains.html')