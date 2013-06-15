import unicodedata
from BeautifulSoup import BeautifulSoup
from gensim import corpora, models, similarities

# Change to Scott's version

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


def slamAd(filepath):
    singleAdFile = open(filepath, "r")
    singleData = singleAdFile.read()
    singlesoup = BeautifulSoup(singleData)
    headText = getHeadText(singlesoup, filepath)
    try:
        singleHeadText = unicodedata.normalize('NFKD', headText).encode('ascii', 'ignore')
    except:
        singleHeadText = headText

    # remove common words and tokenize
    #text = [word for word in headText.lower().split() if word not in stoplist]
    print singleHeadText
    adDictionary = corpora.Dictionary.load("adsDic.dict")
    vec_bow = adDictionary.doc2bow(singleHeadText.lower().split())
    lsi = models.LsiModel.load('adsLsi.lsi')
    vec_lsi = lsi[vec_bow]

    max = -4
    maxTopic = -1
    for pair in vec_lsi:
        if abs(pair[1]) > max:
            max = abs(pair[1])
            maxTopic = pair[0]

    print "\nMax: " + str(max)
    if (max < 1.0):
        print "Can't assign topic"
    else:
        print lsi.print_topics(25)[maxTopic]


#fp = raw_input("Enter path to slam ad: ")
#slamAd(fp)