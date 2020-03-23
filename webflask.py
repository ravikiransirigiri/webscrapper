# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 13:27:26 2020

@author: ravi.kiran.sirigiri
"""

import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
#import pymongo
from flask import Flask, render_template, request,jsonify
import json

app = Flask(__name__)  # initialising the flask app with the name 'app'

@app.route('/',methods=['GET']) # route with allowed methods as POST and GET
def index():
    if request.method == 'GET':
        flipkart_url =  "https://www.flipkart.com/search?q=iphone" # preparing the URL to search the product on flipkart
        uClient = uReq(flipkart_url) # requesting the webpage from the internet
        flipkartPage = uClient.read() # reading the webpage
        uClient.close() # closing the connection to the web server
        flipkart_html = bs(flipkartPage, "html.parser") # parsing the webpage as HTML
        bigboxes = flipkart_html.findAll("div", {"class": "bhgxx2 col-12-12"}) # seacrhing for appropriate tag to redirect to the product link
        del bigboxes[0:3] # the first 3 members of the list do not contain relevant information, hence deleting them.
        box = bigboxes[0] #  taking the first iteration (for demo)
        productLink = "https://www.flipkart.com" + box.div.div.div.a['href'] # extracting the actual product link
        prodRes = requests.get(productLink) # getting the product page from server
        prod_html = bs(prodRes.text, "html.parser") # parsing the product page as HTML
        commentboxes = prod_html.find_all('div', {'class': "_3nrCtb"})# finding the HTML section containing the customer comments
        
        #table = db[searchString] # creating a collection with the same name as search string. Tables and Collections are analogous.
        #filename = searchString+".csv" #  filename to save the details
        #fw = open(filename, "w") # creating a local file to save the details
        #headers = "Product, Customer Name, Rating, Heading, Comment \n" # providing the heading of the columns
        #fw.write(headers) # writing first the headers to file
        reviews = [] # initializing an empty list for reviews
        #  iterating over the comment section to get the details of customer and their comments
        for commentbox in commentboxes:
            try:
                name = commentbox.div.div.find_all('p', {'class': '_3LYOAd _3sxSiS'})[0].text
            
            except:
                name = 'No Name'
            
            try:
                rating = commentbox.div.div.div.div.text
            
            except:
                rating = 'No Rating'
            
            try:
                commentHead = commentbox.div.div.div.p.text
            except:
                commentHead = 'No Comment Heading'
            try:
                comtag = commentbox.div.div.find_all('div', {'class': ''})
                custComment = comtag[0].div.text
            except:
                custComment = 'No Customer Comment'
            #fw.write(searchString+","+name.replace(",", ":")+","+rating + "," + commentHead.replace(",", ":") + "," + custComment.replace(",", ":") + "\n")
            mydict = {"Product": "jeans", "Name": name, "Rating": rating, "CommentHead": commentHead,
                      "Comment": custComment} # saving that detail to a dictionary
            #x = table.insert_one(mydict) #insertig the dictionary containing the rview comments to the collection
            reviews.append(mydict) #  appendin
        return json.dumps(reviews)
    else:
        print("nothing")
            
if __name__ == "__main__":
    app.run(port=9000,debug=True,use_reloader=False) # running the app on the local machine on port 8000