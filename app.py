from flask import Flask, render_template, request, redirect, jsonify, \
    url_for, flash

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





# Display all forms
@app.route('/')
def showMain():
    forms = ["thing1", "thing2", "cat-in-the-hat"]

    return render_template('forms.html', forms=forms)

if __name__ == '__main__':
    # app.config.from_object('config.DevelopmentConfig')
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
