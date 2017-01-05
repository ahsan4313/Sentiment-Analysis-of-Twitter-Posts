import collections
class Document:
    def __init__(self,text,wordToMap):
        v=len(wordToMap)
        #print text
        wordFreMap={}
        wordFreMap=collections.OrderedDict(wordFreMap)
        token=""
        self.text=text
        tokenid=0
        count=0
        st=text.split()
        for token in st:
            #print token
            if(wordToMap.has_key(token)==False):
               # print token
                tokenid=v
                wordToMap[token]= tokenid
                v=v+1
            else:
                tokenid=wordToMap[token]

               # print tokenid
            if(wordFreMap.has_key(tokenid)==False):

                wordFreMap[tokenid]=1
                #print "if"
                #print tokenid
                #print wordFreMap[tokenid]
            else:
                val=wordFreMap[tokenid]
                wordFreMap[tokenid]=val+1
                #print "else"
                #print tokenid
                #print wordFreMap[tokenid]
        self.wordNum=len(wordFreMap)

        self.wordArray=[]
        self.wordFreArray=[]
        w=0
        word=wordFreMap.items()
        for i in range(self.wordNum):
            self.wordArray.append(0)
            self.wordFreArray.append(0)
        for key in wordFreMap:
            
            self.wordArray[w]=key
            #print self.wordArray[w]
            self.wordFreArray[w]=wordFreMap[key]
            #print self.wordFreArray[w]
            w=w+1
        #print count
    def returntext(self):
        return self.text
    def returnnum(self):
        return self.wordNum
    def returnwordarray(self,key):
        return self.wordArray[key]
    def returnwordfrearray(self,key):
        return self.wordFreArray[key]
