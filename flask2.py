# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 14:35:14 2020

@author: ravi.kiran.sirigiri
"""

from flask import Flask,render_template
app=Flask(__name__)

@app.route('/') # route with allowed methods as POST and GET
def home():
#    h={
#       'name':'ravi'}
#    return h
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True,use_reloader=False)