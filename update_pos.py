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
import re
from string import punctuation
from nltk.corpus import stopwords
import baseline_classifier
# MySQL configurations
# create table postive_words( id int auto_increment, word varchar(50), primary key(id));
conn = MySQLdb.Connect(host="127.0.0.1", port=3306, user="root", passwd="ayesha", db="analyzer")
cursor = conn.cursor()
conn.autocommit(True)          
cursor.execute("select distinct trend_name from tweets")
all_trends=cursor.fetchall()
for row in all_trends:
    print row[0]
    sql='select distinct tweet from processed where trend_name = %s'
    cursor.execute(sql,(row[0],))
    all=[]
    results=[item[0] for item in cursor.fetchall()]
    for item in results:
        all.append(item)
	res=baseline_classifier.BaselineClassifier(all,row[0],'today')
	res.classify()
    val={}
    val=res.return_all()
    labels=val["labels"]
    texxt=val["text"]
    tweet=val["tweet"]
    time=val["time"]
    pos_count=val["pos_count"]
    print pos_count
    neg_count=val["neg_count"]
    print neg_count
    neut_count=val["neut_count"]
    print neut_count
    cursor.execute("insert into classified (trend_name,positive,negative,neutral) values (%s,%s,%s,%s)" , [row[0],int(pos_count),int(neg_count),int(neut_count)])
    conn.commit()
    #id=row[0]
    #trend=row[1]
   # tweet=process_tweet(row[2])
   # querywords=tweet.split()
   # resultwords  = [word for word in querywords if word.lower() not in stopwords]
   # result = ' '.join(resultwords)
   # date=row[3]
   # cursor.execute("insert into processed (trend_name,tweet,date) values (%s,%s,%s)" , [trend,result,date])
   # conn.commit()
   # print result