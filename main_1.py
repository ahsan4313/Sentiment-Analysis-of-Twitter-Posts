import collections
import DocumentSet
import Model
#import Document
if __name__ == "__main__":
    K=500
    alpha=0.1
    beta=0.1
    iterNum=30
    dataset="Tweet"
    dataDir="data/Tweet"
    wordToMap={}
    wordToMap=collections.OrderedDict(wordToMap)
    res=DocumentSet.DocumentSet(dataDir,wordToMap)
    V=len(wordToMap)
    model=Model.Model(K,V,iterNum,alpha,beta,dataset,"")
    model.initialize(res)
    model.gibbsSampling(res)
    model.outputClusteringResult("results",res)