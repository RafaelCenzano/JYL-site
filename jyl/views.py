from jyl import app, forms
from flask import render_template, redirect, url_for, request, flash, make_response

'''
Views
'''
@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
@app.route('/home/', methods=['GET'])
def index():

    page = make_response(render_template('home.html'))
    page.set_cookie('page', 'index', max_age=60 * 60 * 24 * 365)
    return page