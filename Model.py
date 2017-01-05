import DocumentSet
import sys
import math
import random
import shutil
import os
import numpy as np
from nltk.corpus import stopwords 
from nltk.stem.wordnet import WordNetLemmatizer
import string
import gensim
from gensim import corpora
from PIL import Image
from os import path
import matplotlib.pyplot as plt
import random
from random import randint
from wordcloud import WordCloud, STOPWORDS
import Document
class Model:
    def __init__(self,K,V,iterNum,alpha,beta,ParameterStr):
        self.ParameterStr=ParameterStr
        self.alpha=alpha
        self.beta=beta
        self.K=K
        self.V=V
        self.topics={}
        self.D=0
        self.z=[]
        self.iterNum=iterNum
        self.alpha0=K * alpha
        self.beta0=V * beta
        self.m_z=[]
        self.n_z=[]
        self.n_zv=[]
        self.imagearray=[]
        self.smallDouble=1e-150
        self.largeDouble=1e150
        for i in range(self.K):
            self.n_zv.append([])		
		

        for i in range(self.K):
            self.m_z.append(0)
            self.n_z.append(0)
            for j in range(self.V):
                self.n_zv[i].append(0)
    def grey_color_func(self,word, font_size, position, orientation, random_state=None, **kwargs):
        return "hsl(0, 0%%, %d%%)" % random.randint(60, 100)
    def initialize(self,documenSet): 
        count=0
        self.D = documenSet.return_D()
        for k in range(self.D):
            self.z.append(0)
        for m in range(self.D):
            res=documenSet[m]
            #print res.returntext()
            cluster=int(self.K * random.uniform(0,1))
            #print res.returnnum()
            self.z[m]=cluster
            self.m_z[cluster]= self.m_z[cluster]+1
            for w in range(res.returnnum()):
                wordNo=res.returnwordarray(w)
                #print wordNo
                count=count+1
                wordFre=res.returnwordfrearray(w)
                #print wordFre
                self.n_zv[cluster][wordNo]=self.n_zv[cluster][wordNo]+wordFre
                self.n_z[cluster]=self.n_z[cluster]+wordFre

        	
    def gibbsSampling(self,documentSet):
        for i in range(self.iterNum):
            for d in range(self.D):
                res=documentSet[d]
                cluster=self.z[d]
               # print res.returntext()
                self.m_z[cluster]=self.m_z[cluster]-1
                for w in range(res.returnnum()):
                    wordNo=res.returnwordarray(w)
                    wordFre=res.returnwordfrearray(w)
                    self.n_zv[cluster][wordNo]=self.n_zv[cluster][wordNo]-wordFre
                    self.n_z[cluster]=self.n_z[cluster]-wordFre
                cluster= self.sampleCluster(d,res)
                #print cluster
                self.z[d]=cluster
                self.m_z[cluster]=self.m_z[cluster]+1
                for w in range(res.returnnum()):
                    wordNo=res.returnwordarray(w)
                    wordFre=res.returnwordfrearray(w)
                    self.n_zv[cluster][wordNo]=self.n_zv[cluster][wordNo]+wordFre
                    self.n_z[cluster]=self.n_z[cluster]+wordFre
					
					
    def sampleCluster(self,d,document):
        prob=[]	
        overflowCount=[]
        for p in range(self.K):
            prob.append(0.0)
            overflowCount.append(0)
			
			
        for k in range(self.K):
            prob[k]=(self.m_z[k]+self.alpha)/ (self.D-1+self.alpha0)
            
            valueofRule2=1.0
            i=0
            for w in range(document.returnnum()):
                wordNo=document.returnwordarray(w)
                wordFre=document.returnwordfrearray(w)
                for j in range(wordFre):
                    if(valueofRule2<self.smallDouble):
                        overflowCount[k]=overflowCount[k]-1
                        valueofRule2=valueofRule2*self.largeDouble
                    valueofRule2=valueofRule2*((self.n_zv[k][wordNo]+self.beta+j)/ (self.n_z[k]+self.beta0+i))
                    i=i+1
            prob[k]=valueofRule2*prob[k]
        self.reComputeProbs(prob,overflowCount,self.K)
        #print prob[0]
        k=1
        while(k<self.K):
            prob[k]=prob[k]+prob[k-1]
            k=k+1
        thred=random.uniform(0,1) * prob[self.K-1]
        kc=0
        for kChoosed in range(self.K):
            if(thred<prob[kChoosed]):
                kc=kChoosed
                break;  
        return kc
   

  
    def reComputeProbs(self,prob,overflowCount,K):
        max= -2147483648
        for k in range(K):
            if(overflowCount[k]>max and prob[k]>0):
                max=overflowCount[k]
                #print max
        for k in range(K):
            if(prob[k]>0):
                prob[k]=prob[k] * math.pow(self.largeDouble,(overflowCount[k]-max))
       # print prob[0]
    def outputClusteringResult(self,outputDir,documenSet):
        directory=r"C:\Users\DELL\Desktop\Twisent\static\allpictures"
        if  os.path.exists(directory):
            shutil.rmtree(directory)
        if not os.path.exists(directory):
            os.makedirs(directory)
        clustermap={}
        self.imagearray=[]
        newfile=open("allwords.txt",'w')
        #file=open(outputpath,'w')
        for c in range(self.D):
            topic=self.z[c]
            if(clustermap.has_key(topic)==False):
                clustermap[topic]=[]
        for d in range(self.D):
            topic=self.z[d]
            clustermap[topic].append(documenSet.gettext(d))
        i=0
     #####  getting the topics of the clusters  #####
        for key in clustermap:
            wor=""
            alltwe=clustermap[key]
            for item in alltwe:
                wor=wor+""+item
            self.cloud_image(wor,i)
            i=i+1
            
            #doc_complete=clustermap[key]
            #doc_clean=[self.clean(doc).split() for doc in doc_complete]
             #Creating the term dictionary of our courpus, where every unique term is assigned an index. dictionary = corpora.Dictionary(doc_clean)
            #dictionary = corpora.Dictionary(doc_clean)
            #Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
            #doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]
            #Creating the object for LDA model using gensim library
            #Lda = gensim.models.ldamodel.LdaModel 
            #ldamodel = Lda(doc_term_matrix, num_topics=1, id2word = dictionary, passes=1)
            #str1=''.join(''.join(str(elems) for elems in (ldamodel.print_topics(num_topics=1, num_words=1))))
            #newfile.write(str1.decode('utf-8'))			
        
		
		

    def clean(self,doc):
        stop = set(stopwords.words('english'))
        exclude = set(string.punctuation) 
        lemma = WordNetLemmatizer()
        stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
        punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
        normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
        return normalized
    def cloud_image(self,words,num):
        d = path.dirname(__file__)

        mask = np.array(Image.open(path.join(d, "square.png")))
        text = words

        
        stopwords = set(STOPWORDS)
        stopwords.add("int")
        stopwords.add("ext")
        stopwords.add("AT_USER")
        stopwords.add("URL")
        wc = WordCloud(max_words=1000, mask=mask, stopwords=stopwords, margin=20,
                       random_state=1).generate(text)
# store default colored image
        default_colors = wc.to_array()
        wc.to_file("static/allpictures/a_new_hope"+str(num)+".png")
        self.imagearray.append("../allpictures/a_new_hope"+str(num)+".png")
    def return_images(self):
        return self.imagearray
        				
	
	
	
	
	
	
