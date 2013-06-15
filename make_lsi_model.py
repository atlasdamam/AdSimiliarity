import urllib2
import re
import unicodedata
from BeautifulSoup import BeautifulSoup
from gensim import corpora, models, similarities
import os

#Global Variables


def getHeadText(soup, file_path):

    headText = ""

    #Get title
    t = soup.find("title").__str__()
    title = t[t.find('>')+1:t.find('<',t.find('>')+1,len(t))]
    print title
    #Add title text to headText
    headText += title

    #Get keywords from meta tag with name=keywords. The actual keywords lie in the content field.
    keywords = soup.findAll("meta", attrs ={'name' : 'keywords'})
    print "KEYWORDS: "
    for k in keywords:
        print k['content']
        headText += unicodedata.normalize('NFKD',k['content']).encode('ascii','ignore')


    #Get description from meta tag with name=description. Likewise, the actual description text lies in the content field.
    description = soup.findAll("meta", attrs ={'name' : 'description'})
    print "DESCRIPTION: "
    for d in description:
        print d['content']
        headText += unicodedata.normalize('NFKD',d['content']).encode('ascii','ignore')

    headText = headText.replace(",", " ")
    headText = headText.replace('\n' , ' ')
    headText = headText.replace('.' , ' ')
    return headText

#We are not currently using text from the body of the webpage.

#def getBodyText():
#    b = soup.find('body')
#    [s.extract() for s in b('iframe', 'script', 'select' , 'input')]
#    #body = b.find(text = True)
#    body = b.findAll(text = True)
#    bodyText = ''
#    for bo in body:
#        bodyText += bo
#
#    print bodyText
#        
#    '''
#    #print b
#    print b.find('<')
#    print b.find('>')
#    print b[b.find('>')+1:b.find('<',b.find('>')+5,len(b))]
#'''
        
#with open("ClearHtml.txt", "w") as text_file:
    
        #text_file.write(headText)
        #getBodyText()


listofAds = []
path = str(os.getcwd()) + "/ads1_and_2"
#path = "/Users/Sam_Toizer/Documents/School/15th grade/Q3/Online Advertising/AdSimiliarity/ads1_and_2"
listing = os.listdir(path)
for infile in listing:
    #print "html filename is: " + infile
    html_file = open(os.path.join(path, infile), "r")
    data = html_file.read()
    adsoup = BeautifulSoup(data)
    headText = getHeadText(adsoup, os.path.join(path, infile))
    #print
    try:
        listofAds.append(unicodedata.normalize('NFKD',headText).encode('ascii','ignore'))
    except:
        listofAds.append(headText)


print "Done reading files."    




# remove common words and tokenize
stoplist = set('for a of the and to in you on - your else free deal website discount online system or with be ad'.split()) # we need to add more words like you , on , - , your , else
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

lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=25) # initialize an LSI transformation
lsi.save("adsLsi.lsi")
corpus_lsi = lsi[corpus_tfidf] # create a double wrapper over the original corpus: bow->tfidf->fold-in-lsi
for doc in corpus_lsi:
    print doc

print "LSI topics:"
for i in range(25):
    print "\n"
    print str(i+1) + ":"
    print lsi.print_topics(25)[i]

'''
lsi.save('model.lsi') # same for tfidf, lda, ...
lsi = models.LsiModel.load('model.lsi')

model = ldamodel.LdaModel(corpus, id2word=dictionary, num_topics=100)
'''


print "Done creating lsi model."






        
        
        
        

