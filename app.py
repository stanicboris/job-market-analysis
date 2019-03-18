from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from wtforms import Form

# from sqlalchemy import create_engine, asc, desc, \
#     func, distinct
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.serializer import loads, dumps

# from database_setup import Base, Things

import random
import string
import logging
import json
import httplib2
import requests


app = Flask(__name__)


# Connect to database and create database session
# engine = create_engine('sqlite:///flaskstarter.db')
# Base.metadata.bind = engine

# DBSession = sessionmaker(bind=engine)
# session = DBSession()

host = 'localhost'
port = 8000

# Display all forms
@app.route('/', methods=['GET'])
def index():
    print('request.method', request.method)
    print('request.json', request.json)
    # form = ButtonForm(request.form)
    # if form.validate_on_submit():
    #     if 'download' in request.form:
    #         print('download')
    #     elif 'watch' in request.form:
    #         print('watch')
    
    return render_template('scripts.html', data={'host':host, 'port':port})

@app.route('/', methods=['POST'])
def index_sub():
    import mongo
    email = request.form['mail']
    mongo = mongo.Mongo()
    cond = mongo.check_mail(email)
    if cond:
        mongo.add_email(email) 
        message = 'Votre email à été ajoutée à la liste !'
    else:
        message = 'Veuillez entrer un email valide'
    return render_template("scripts.html",message = message)
    
    
    
@app.route('/forms')
def showMain():
    forms = ["thing1", "thing2", "cat-in-the-hat"]

    return render_template('forms.html', forms=forms)


# class ButtonForm(Form):
#     submit = Su('Do this')
#     submit2 = Form.SubmitField('Do that')


if __name__ == '__main__':
    # app.config.from_object('config.DevelopmentConfig')
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host=host, port=port)
    
    
    
    
    
    
    
    
    
    
    
    
    
