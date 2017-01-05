import Document
import json
class DocumentSet:
    def __init__(self,wordToMap,all):
        self.D=0
        self.documents=[]
        line=""
        r=open("alltweets.txt",'w')
        
        element=""
        i=1
        for line in all:
            
            self.D=self.D+1
            i=i+1
            r.write(line+'\n')
            res=Document.Document(line,wordToMap)
            self.documents.append(res)
        #print self.D
    def return_D(self):
        return self.D
    def __getitem__(self, key):
        return self.documents[key]
    def gettext(self,key):
        return self.documents[key].returntext()