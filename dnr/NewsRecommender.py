import numpy as np
from gensim import corpora, models, similarities
import operator
import re
from scipy import spatial
import time
import tempfile

class Recommendation(object):

    #1. Initialize with gensim model
    #follow : https://radimrehurek.com/gensim/models/word2vec.html
    #Interestingly you can do this for any language
    #Initialization of Model
    def __init__(self,model,path_to_temp = '/tmp/'):
        self.path_to_temp = path_to_temp
        self.model = model

    #get WordVec embeddings and multiply embeddings with respective tfidf score
    #words that doesn't exist in model are not updated yet
    #new version will try to address this issue
    #Assuming your model is trained with enough words so that minimum may not fall in model
    def getWordVec(self,word,tfidfFactor=1):
        try:
            return self.model.wv.__getitem__(word)*tfidfFactor
        except:
            return np.zeros(100)

    #2. Initialize with data with latest read
    #getLatest(Read) will take a newsList assume like below
    #newsList = ['सवा १० अर्बको हकप्रद सेयर आउँदै',
    #  'थामिने छाँट छैन सिँगौरी',
    #  'नयाँ शक्तिको प्रचार आक्रामक, कहाँबाट अाउँछ खर्च ?',
    #  'मन्त्री पासवानलाई एयर एम्बुलेन्सबाट भारत लग्ने तयारी ',
    #  'कान्तिपुर हिसान एडुफेयर जेठ पहिलो साता',
    #  'काठमाडौं आइपुगिन् सोनाक्षी',
    #  'नक्कली प्रमाणपत्र बुझाएको भन्दै पाइलट पक्राउ',
    #  'सत्तापक्षीय दलले एमाओवादीलाई भने, ‘सरकार फेर्ने समय उचित होइन’',
    #  'फोरम लोकतान्त्रिक अध्यक्षमा गच्छदारको मात्र उम्मेद्वारी']
    # This is an example for nepali text but you can do this for english or anyother language
    def addLatestRead(self,newsList):
        self.newsList = newsList
        self.computeTfIdfScore(list(map(lambda x:x.split(),self.newsList)))

    #3. Compute tfidfScore
    #this is step by step process to calculate tf-idf score for the documents in user LatestNewsRead from above
    #finally the vector representing the entire latestread as mean vector will be calculated
    #for detail please refer to readme.md file
    def computeTfIdfScore(self,tweets):
        '''
        tempfile = str(time.time()).replace('.','')
        tempdict = self.path_to_temp + tempfile +'.dict'
        tempmm = self.path_to_temp + tempfile +'.mm'
        tempindex = self.path_to_temp + tempfile +'.index'
        #trying with tempfile
        tempdict = tempfile.TemporaryFile()
        tempmm = tempfile.TemporaryFile()
        tempindex = tempfile.TemporaryFile()
        #end trying with tempfile
        '''
        try:
            # STEP 1 : Compile corpus and dictionary
            # create dictionary (index of each element)
            dictionary = corpora.Dictionary(tweets)
            # dictionary.save('/tmp/tweets.dict') # store the dictionary, for future reference
            # dictionary.save(tempdict) # store the dictionary, for future reference

            # compile corpus (vectors number of times each elements appears)
            raw_corpus = [dictionary.doc2bow(t) for t in tweets]
            # corpora.MmCorpus.serialize('/tmp/tweets.mm', raw_corpus) # store to disk
            # corpora.MmCorpus.serialize(tempmm, raw_corpus) # store to disk

            # STEP 2 : similarity between corpuses
            # dictionary = corpora.Dictionary.load('/tmp/tweets.dict')
            # dictionary = corpora.Dictionary.load(tempdict)

            # corpus = corpora.MmCorpus('/tmp/tweets.mm')
            # corpus = corpora.MmCorpus(tempmm)
            corpus = raw_corpus

            # Transform Text with TF-IDF
            tfidf = models.TfidfModel(corpus) # step 1 -- initialize a model
            # corpus tf-idf
            corpus_tfidf = tfidf[corpus]

            # STEP 3 : Create similarity matrix of all files
            index = similarities.MatrixSimilarity(tfidf[corpus])
            # index.save('/tmp/deerwester.index')
            # index.save(tempindex)
            # index = similarities.MatrixSimilarity.load('/tmp/deerwester.index')
            # index = similarities.MatrixSimilarity.load(tempindex)
            #sims = index[corpus_tfidf] #For thiss purpose we don't use similarity matrix

            self.index = index.index

            reverseDict = {j:i for i,j in dict(dictionary).items()}

            tweetsIdf=[]

            for t,i in zip(tweets,self.index):
                tweetsIdf.append(list(map(lambda x:i[reverseDict[x]],t)))

                tweetsVec = []
                for tw,idf in zip(tweets,tweetsIdf):
                    t = np.array(list(map(lambda u,v:self.getWordVec(u,v),tw,idf)))
                    tweetsVec.append(np.mean(t,axis=0))
                    tVec = np.array(tweetsVec)
                    self.V = np.mean(tVec,axis=0)

        except Exception as e:
            print(e)
        '''
        tempfiles = [k for k in os.listdir(self.path_to_temp) if k.startswith(tempfile)]
        for tfile in tempfiles:
            try:
                os.remove(tfile)
            except Exception as e:
                print(e)
        '''

    #4. Get Recommendation
    #Finally this will return recommended index based on cosine distance
    #remember n must be less than the number of documents to be recommended from else n will be minimum
    #of number of documents and n given as input, default n is 10
    def getRecommendation(self,newNews,n=10):
        latestVec={}
        for key,values in newNews.items():
            x = np.mean(np.array(list(map(lambda x:self.getWordVec(x,1),values.split()))),axis=0)
            sim = 1 - spatial.distance.cosine(x,self.V)
            dis = np.arccos(sim)/np.pi
            latestVec[key] = 1 - dis
        maxRecom = min(len(newNews),n)
        self.recommendation = sorted(latestVec.items(), key=operator.itemgetter(1),reverse=True)[:maxRecom]

        return list(map(lambda x:x[0],self.recommendation))
