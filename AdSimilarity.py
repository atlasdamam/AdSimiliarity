import urllib2
import re
import unicodedata
from BeautifulSoup import BeautifulSoup
from gensim import corpora, models, similarities
import os

#Global Variables
count_keywords = 0
count_description = 0
count_title = 0
count_key_desc_and = 0
count_key_desc_or = 0

def getHeadText(soup, file_path):
    global count_keywords
    global count_description
    global count_title
    global count_key_desc_and
    global count_key_desc_or

    headText = ""
    #Get title
    t = soup.find("title").__str__()
    title = t[t.find('>')+1:t.find('<',t.find('>')+1,len(t))]
    if title!="": 
        count_title += 1
    print title
    #Add title text to headText
    headText += title

    #Get keywords from meta tag with name=keywords. The actual keywords lie in the content field.
    keywords = soup.findAll("meta", attrs ={'name' : 'keywords'})
    if keywords!=[]:
        count_keywords += 1
    print "KEYWORDS: "
    for k in keywords:
        try: 
            doNothing = True
            print k['content']
        except:
            print "There exists a keywords meta tag in this file which has no content"
        try: 
            headText += unicodedata.normalize('NFKD',k['content']).encode('ascii','strict')
            #count_keywords = count_keywords + 1
        except: 
            print "Error in conversion to ascii. Deleting file."
            try:
                os.remove(file_path)
            except: 
                print "Error in removing file?"

    #Get description from meta tag with name=description. Likewise, the actual description text lies in the content field.
    description = soup.findAll("meta", attrs ={'name' : 'description'})
    if description!=[]:
        count_description += 1
    print "DESCRIPTION: "
    for d in description:
        try:
            doNothing = True
            print d['content']
        except:
            print "There exists a description meta tag in this file which has no content"
        try: 
            headText += unicodedata.normalize('NFKD',d['content']).encode('ascii','strict')
            #count_description = count_description + 1
        except: 
            print "Error in conversion to ascii. Deleting file."
            try:
                os.remove(file_path)
            except: 
                print "Error in removing file?"
        
    if keywords!=[] and description!=[]:
        count_key_desc_and += 1

    if not(keywords!=[] and description!=[]):
        os.remove(file_path)

    if keywords!=[] or description!=[]:
        count_key_desc_or += 1

    return headText.replace('\n' , ' ')

def slamAd(filepath):
    file_path = "nopath"
    singleAdFile = open(filepath, "r")
    singleData = singleAdFile.read()
    singlesoup = BeautifulSoup(singleData)
    try:
        singleHeadText = unicodedata.normalize('NFKD', getHeadText(singlesoup, file_path)).encode('ascii', 'strict')
    except:
        singleHeadText = getHeadText(singlesoup, file_path)

    # remove common words and tokenize
    #text = [word for word in headText.lower().split() if word not in stoplist]
    print singleHeadText
    adDictionary = corpora.Dictionary.load("adsDic.dict")
    vec_bow = adDictionary.doc2bow(singleHeadText.lower().split())
    vec_lsi = lsi[vec_bow]

    max = -4
    maxTopic = -1
    for pair in vec_lsi:
        if abs(pair[1]) > max:
            max = abs(pair[1])
            maxTopic = pair[0]
    print "Max topic number: " + str(maxTopic)
    print lsi.print_topics(100)[maxTopic]


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
path = "/Users/scottneaves/Desktop/Online Advertising/AdSimiliarity/ads_new"
listing = os.listdir(path)
for infile in listing:
    #print "html filename is: " + infile
    html_file = open(os.path.join(path, infile), "r")
    data = html_file.read()
    adsoup = BeautifulSoup(data)
    headText = getHeadText(adsoup, os.path.join(path, infile))
    #print
    try:
        listofAds.append(unicodedata.normalize('NFKD',headText).encode('ascii','strict'))
    except:
        listofAds.append(headText)


print "Done reading files."    
print "Number of files with keyword meta tags (which have content): " 
print count_keywords
print "Number of files with description meta tags (which have content): "
print count_description
print "Number of files with keywords and descriptions"
print count_key_desc_and
print "Number of files with keywords or descriptions"
print count_key_desc_or
print "Number of files with titles"
print count_title




# remove common words and tokenize
stoplist = set('for a of the and to in you on - your else money free deal website discount online system or with be'.split()) # we need to add more words like you , on , - , your , else
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
for doc in corpus_lsi:
    print doc

'''
lsi.save('model.lsi') # same for tfidf, lda, ...
lsi = models.LsiModel.load('model.lsi')

model = ldamodel.LdaModel(corpus, id2word=dictionary, num_topics=100)
'''


print "Done"






        
        
        
        

