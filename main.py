from flask import Flask, render_template, json, request
from flask_mysqldb import MySQL
import MySQLdb
import sys,pickle
import baseline_classifier
from werkzeug import generate_password_hash, check_password_hash
from twitter import *
import time,threading
import urllib
import urllib2
import json
import tweepy
import time
import datetime
import collections
import DocumentSet
import re
import Model
mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'analyzer'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
conn = MySQLdb.Connect(host="127.0.0.1", port=3306, user="root", passwd="ayesha", db="analyzer")
cursor = conn.cursor()
stopWords=[]


	
	


def get_all_trends():
    cursor.execute("select trend_name from trends")
    results=[item[0] for item in cursor.fetchall()]
    return results
	
	
@app.route('/tweets',methods=['POST'])
def tweets():
    if request.method=='POST':
        var=request.form['submit']
    sql='select distinct tweet from processed where trend_name = %s LIMIT 25'
    cursor.execute(sql,(var,))
    all=[]
    results=[item[0] for item in cursor.fetchall()]
    for item in results:
        #item=item.encode('utf-8', errors='replace')
        all.append(item)
    wordToMap={}
    K=15
    alpha=0.1
    beta=0.1
    iterNum=10
    res=baseline_classifier.BaselineClassifier(all,var,'today')
    res2=res.return_processed()
	
    wordToMap=collections.OrderedDict(wordToMap)
    res1=DocumentSet.DocumentSet(wordToMap,res2)
    V=len(wordToMap)
    model=Model.Model(K,V,iterNum,alpha,beta,"")
    model.initialize(res1)
    model.gibbsSampling(res1)
    model.outputClusteringResult("results",res1)
    imagearray=model.return_images()
    #model.cloud_image()
    res.classify()
    val={}
    val=res.return_all()
    labels=val["labels"]
    texxt=val["text"]
    tweet=val["tweet"]
    time=val["time"]
    sql='select positive from classified where trend_name= %s'
    cursor.execute(sql,(var,))
    pos_count=[item[0] for item in cursor.fetchall()]
    sql='select negative from classified where trend_name= %s'
    cursor.execute(sql,(var,))
    neg_count=[item[0] for item in cursor.fetchall()]
    sql='select neutral from classified where trend_name= %s'
    cursor.execute(sql,(var,))
    neut_count=[item[0] for item in cursor.fetchall()]
    lengt=len(labels)
    i=0
    positive=[]
    negative=[]
    neutral=[]
    sql='select distinct tweet from tweets where trend_name = %s LIMIT 25'
    cursor.execute(sql,(var,))
    real=[]
    results=[item[0] for item in cursor.fetchall()]
    for item in results:
        #item=item.encode('utf-8', errors='replace')
        real.append(item)
    for i in range(lengt):
        if labels[i]=='positive':
            positive.append(real[i])
    for i in range(lengt):
        if labels[i]=='negative':
            negative.append(real[i])
    for i in range(lengt):
        if labels[i]=='neutral':
            neutral.append(real[i])
    return render_template('follow.html',positive=pos_count[0],negative=neg_count[0],neutral=neut_count[0],pos=positive,neg=negative,neu=neutral,trend_name=var,image_array=len(imagearray),allimage=imagearray)

	
	
	
@app.route('/mainindex')
def mainindex():
    return mainpage()
def mainpage():
    #items=[]
   # items=get_all_trends()
    return render_template('index.html')



@app.route('/Politics')
def Politics():
    cursor.execute("select trend_name from trend_domain where trend_domain='Politics'")
    results = [item[0] for item in cursor.fetchall()]
    return render_template('trends.html',item=results, domain='Politics')

@app.route('/Education')
def Education():
    cursor.execute("select trend_name from trend_domain where trend_domain='Education'")
    results = [item[0] for item in cursor.fetchall()]
    return render_template('trends.html',item=results,domain='Education')

@app.route('/Sports')
def Sports():
    cursor.execute("select trend_name from trend_domain where trend_domain='Sports'")
    results = [item[0] for item in cursor.fetchall()]
    return render_template('trends.html',item=results, domain='Sports')

	
@app.route('/Celebrity')
def Celebrity():
    cursor.execute("select trend_name from trend_domain where trend_domain='Celebrity'")
    results = [item[0] for item in cursor.fetchall()]
    return render_template('trends.html',item=results,domain='Celebrity')	

@app.route('/Terrorism')
def Terrorism():
    cursor.execute("select trend_name from trend_domain where trend_domain='Terrorism'")
    results = [item[0] for item in cursor.fetchall()]
    return render_template('trends.html',item=results,domain='Terrorism')	
	
	
@app.route('/Others')
def others():
    cursor.execute("select trend_name from trend_domain where trend_domain='Others'")
    results = [item[0] for item in cursor.fetchall()]
    return render_template('trends.html',item=results, domain='Others')

@app.route("/")
def main():
    return mainpage()
	
if __name__=="__main__":
    app.run()
