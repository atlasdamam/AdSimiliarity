from nltk.corpus import stopwords   # stopwords to detect language
from nltk import wordpunct_tokenize # function to split up our words
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

def get_language_likelihood(input_text):
    """Return a dictionary of languages and their likelihood of being the 
    natural language of the input text
    """
 
    input_text = input_text.lower()
    input_words = wordpunct_tokenize(input_text)
 
    language_likelihood = {}
    total_matches = 0
    for language in stopwords._fileids:
        language_likelihood[language] = len(set(input_words) &
                set(stopwords.words(language)))
 
    return language_likelihood

def get_language(input_text):
    """Return the most likely language of the given text
    """
 
    likelihoods = get_language_likelihood(input_text)
    return sorted(likelihoods, key=likelihoods.get, reverse=True)[0]

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
    print title.encode('ascii', 'strict')
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
            print unicodedata.normalize('NFKD', k['content'])
        except:
            print "There exists a keywords meta tag in this file which has no content"
        try: 
            headText += unicodedata.normalize('NFKD',k['content'])
            #count_keywords = count_keywords + 1
        except: 
            print "Conversion to ASCII failed."


    #Get description from meta tag with name=description. Likewise, the actual description text lies in the content field.
    description = soup.findAll("meta", attrs ={'name' : 'description'})
    if description!=[]:
        count_description += 1
    print "DESCRIPTION: "
    for d in description:
        try:
            doNothing = True
            print unicodedata.normalize('NFKD', d['content'])
        except:
            print "There exists a description meta tag in this file which has no content"
        try: 
            headText += unicodedata.normalize('NFKD',d['content'])
            #count_description = count_description + 1
        except: 
            print "Conversion to ASII failed."

        
    print get_language(headText)

    if keywords!=[] and description!=[]:
        count_key_desc_and += 1

    if not(keywords!=[] and description!=[]):
        os.remove(file_path)

    if keywords!=[] or description!=[]:
        count_key_desc_or += 1

    return headText.replace('\n' , ' ')




listofAds = ["adfromhtml.it.html", "adfromnews247.gr.html", "adfromradio.de.html", "adfrom9minecraft.net.html", "adfromaddictinggames.com.html", "adfromallmusic.com.html", "adfromamctheatres.com.html", "adfromandroidcommunity.com.html", "adfromlos40.com.html", "adfromsearch.ch.html", "adfromzalando.pl.html"]
path = "/Users/scottneaves/Desktop/Online Advertising/AdSimiliarity/mixed_lang"
#listing = os.listdir(path)
for x in range(len(listofAds)):
    print listofAds[x]
    #print "html filename is: " + infile
    html_file = open(os.path.join(path, listofAds[x]), "r")
    data = html_file.read()
    adsoup = BeautifulSoup(data)
    headText = getHeadText(adsoup, os.path.join(path, listofAds[x]))
    #print
    try:
        listofAds.append(unicodedata.normalize('NFKD',headText).encode('ascii','strict'))
    except:
        listofAds.append(headText)
    print 


print "Done reading files."    








        
        
        
        

