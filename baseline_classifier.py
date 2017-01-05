import sys
import re
import classifier_helper, html_helper, pickle
import time
reload(sys)
sys.setdefaultencoding = 'utf-8'
from flask import Flask, render_template, json, request
from flask_mysqldb import MySQL
import MySQLdb
import sys,pickle
from werkzeug import generate_password_hash, check_password_hash
import time,threading
import urllib
import urllib2
import json
import tweepy
import time
import datetime
#start class
class BaselineClassifier:
    #variables    
    #start __init__
    def __init__(self, data, keyword, time):
        #Instantiate classifier helper        
        self.helper = classifier_helper.ClassifierHelper('data/feature_list.txt')
        #Remove duplicates

        self.lenTweets = len(data)
        self.twee=data
        #self.origTweets = self.getUniqData(data)
        self.tweets = self.twee
        self.file_name='data/stopwords.txt'
        self.results = {}
        #self.neut_count = [0] * self.lenTweets
        self.neut_count=0
        self.pos_count = 0
        self.neg_count = 0
        self.stopwords=[]
        self.stopwords.append('AT_USER')
        self.stopwords.append('URL')
		
		
        self.time = time
        self.keyword = keyword
        self.html = html_helper.HTMLHelper()
    #end


    def return_processed(self):
        return self.tweets
		

    def getFeatureVector(self,tweet):
        featureVector = []
    #split tweet into words
        words = tweet.split()
        for w in words:
        #replace two or more with two occurrences
            w = replaceTwoOrMore(w)
        #strip punctuation
            w = w.strip('\'"?,.')
        #check if the word stats with an alphabet
            val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w)
        #ignore if it is a stop word
            if(w in self.stopwords or val is None):
                continue
            else:
                featureVector.append(w.lower())
        return featureVector


    #start getUniqData
    def getUniqData(self, data):
        uniq_data = {}        
        for i in data:
            d = data[i]
            u = []
            for element in d:
                if element not in u:
                    u.append(element)
            #end inner loop
            uniq_data[i] = u            
        #end outer loop
        return uniq_data
    #end
    
    #start getProcessedTweets
    def getProcessedTweets(self, data):
        tw = []	
        tweets = {}        
        for i in data:
            d = i
            #print d
            
            #for t in d:
            tw.append(self.helper.process_tweet(d))
            #tweets[i] = tw            
        #end loop
        return tw
    
    #start classify
    def classify(self):          
        conn = MySQLdb.Connect(host="127.0.0.1", port=3306, user="root", passwd="ayesha", db="analyzer")
        cursor = conn.cursor() 
        w=0	
        labe=[]
        tex=[]
        twe=[]
        all_tweets=self.twee		
        count = 0
        for i in self.tweets:
            #tw = self.tweets[i]
            tw=i
            featureVector = []
    #split tweet into words
            words = tw.split()
            for wr in words:

                wr = wr.strip('\'"?,.')

                featureVector.append(wr)
            #count = 0
            res = {}
            pos_words=[]
            neg_words=[]
            for feature in featureVector:
                sql='select * from positive_words where word = %s '
                cursor.execute(sql,(feature,))
                results=[item[0] for item in cursor.fetchall()]
                if (len(results)>0):
                    pos_words.append(feature)
                else:
                    sql='select * from negative_words where word = %s '
                    cursor.execute(sql,(feature,))
                    results=[item[0] for item in cursor.fetchall()]
                    if (len(results)>0):
                        neg_words.append(feature)
			

            if(len(pos_words) > len(neg_words)):
                label = 'positive'
                self.pos_count += 1
            elif(len(pos_words) < len(neg_words)):
                label = 'negative'
                self.neg_count += 1
            else:
                if(len(pos_words)>0 and len(neg_words)>0):
                    label= 'negative'
                    self.neg_count +=1
                else:
                    label = 'neutral'
                    self.neut_count += 1
            #cursor.execute("insert into label_count (trend_name,pos_count,neg_count,neut_count) values (%s,%s,%s)" , [self.keyword,self.pos_count,self.neg_count,self.neut_count])
            #conn.commit()
            labe.append(label)
            tex.append(tw)
            twe.append(all_tweets[w])
            #result = {'text': tw, 'tweet': tw, 'label': label}
            #res[count] = result                
            count += 1  
            w=w+1
            #end inner loop
        #self.results = res
        self.labels=labe
        self.text=tex
        self.tweeti=twe
		
        #end outer loop   
        filename = 'data/results_lastweek.pickle'
        outfile = open(filename, 'wb')        
        pickle.dump(self.results, outfile)        
        outfile.close()
        '''
        inpfile = open('data/results_lastweek.pickle')
        self.results = pickle.load(inpfile)
        inpfile.close()
        '''
    #end
    
    #start substring whole word match
    def string_found(self, string1, string2):
        if re.search(r"\b" + re.escape(string1) + r"\b", string2):
            return True
        return False
    #end
    
    #start writeOutput
    def writeOutput(self, filename, writeOption='w'):
        fp = open(filename, writeOption)
        for i in self.results:
            res = self.results[i]
            for j in res:
                item = res[j]
                text = item['text'].strip()
                label = item['label']
                writeStr = text+" | "+label+"\n"
                fp.write(writeStr)
            #end inner loop
        #end outer loop      
    #end writeOutput
    
    #start printStats
    def return_all(self):
        my_results={}
        my_results["labels"]=self.labels
        my_results["text"]=self.text
        my_results["tweet"]=self.tweeti
        my_results["time"]=self.time
        my_results["pos_count"]=self.pos_count
        my_results["neg_count"]=self.neg_count
        my_results["neut_count"]=self.neut_count
        return my_results
    #end
#end class    
