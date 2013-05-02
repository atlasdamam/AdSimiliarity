import urllib2
import re
import unicodedata
from bs4 import BeautifulSoup
from gensim import corpora, models, similarities


def getHeadText():
    headText = ""
    #get title
    t = soup.find("title").__str__()
    title = t[t.find('>')+1:t.find('<',t.find('>')+1,len(t))]
    #print title
    headText += title

    #get Keywords
    keywords = soup.findAll("meta", attrs ={'name' : 'keywords'})
    #print keywords
    for k in keywords:
        #print k['content']
        
        headText += unicodedata.normalize('NFKD',k['content']).encode('ascii','ignore')

    #get Description
    description = soup.findAll("meta", attrs ={'name' : 'description'})
    #print description
    for d in description:
        #print d
        headText += unicodedata.normalize('NFKD',d['content']).encode('ascii','ignore')

    return headText.replace('\n' , ' ')

def getBodyText():
    b = soup.find('body')
    [s.extract() for s in b('iframe', 'script', 'select' , 'input')]
    #body = b.find(text = True)
    body = b.findAll(text = True)
    bodyText = ''
    for bo in body:
        bodyText += bo

    print bodyText
        
    '''
    #print b
    print b.find('<')
    print b.find('>')
    print b[b.find('>')+1:b.find('<',b.find('>')+5,len(b))]
'''
        


#with open("ClearHtml.txt", "w") as text_file:
    
        #text_file.write(headText)
        #getBodyText()

listofAds = []
for i in range (0,100):
    html_file = open("ads/"+str(i)+".html","r")
    data = html_file.read()
    soup = BeautifulSoup(data)
    headText = getHeadText()
    #print i
    #print headText
    try:
        listofAds.append(unicodedata.normalize('NFKD',headText).encode('ascii','ignore'))
    except:
        listofAds.append(headText)

print "DONE"


# remove common words and tokenize
stoplist = set('for a of the and to in you on - your else'.split()) # we need to add more words like you , on , - , your , else
texts = [[word for word in ads.lower().split() if word not in stoplist]
          for ads in listofAds]

# remove words that appear only once
all_tokens = sum(texts, [])
tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
texts = [[word for word in text if word not in tokens_once]
          for text in texts]

dictionary = corpora.Dictionary(texts)
dictionary.save('adsDic.dict')

corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('adsCor.mm', corpus) # store to disk, for later use

tfidf = models.TfidfModel(corpus) # step 1 -- initialize a model

corpus_tfidf = tfidf[corpus]

lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=100) # initialize an LSI transformation
corpus_lsi = lsi[corpus_tfidf] # create a double wrapper over the original corpus: bow->tfidf->fold-in-lsi

'''
lsi.save('model.lsi') # same for tfidf, lda, ...
lsi = models.LsiModel.load('model.lsi')

model = ldamodel.LdaModel(corpus, id2word=dictionary, num_topics=100)

'''

print "Done"






        
        
        
        

