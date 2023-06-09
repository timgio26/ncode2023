from flask import render_template,redirect, url_for,request,send_file
from app import app #,db,api

@app.route('/')
def index():
    return render_template('home.html')