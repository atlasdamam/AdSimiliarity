from nltk.corpus import stopwords   # stopwords to detect language
from nltk import wordpunct_tokenize # function to split up our words
import urllib2
import re
import unicodedata
from BeautifulSoup import BeautifulSoup
from gensim import corpora, models, similarities
import os


#Global Variables


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

def cleanFiles(soup, file_path):

    headText = ""

    #Get title
    t = soup.find("title").__str__()
    title = t[t.find('>')+1:t.find('<',t.find('>')+1,len(t))]
    if title=="":
        #This file has no title, so it does not have all of the things we require: title, description, keywords. Therefore, delete it.
        print "This file has no title. Deleting " + file_path
        os.remove(file_path)
        return
    elif title!="":
        headText += title

    #Get keywords from meta tag with name=keywords. The actual keywords lie in the content field.
    keywords = soup.findAll("meta", attrs ={'name' : 'keywords'})
    for k in keywords:
        try: 
            temp = k['content']
        except:
            #Since there is no content in the keywords meta tag, this file does not contain descriptions and keywords and a title. Therefore, delete it.
            print "There exists a keywords meta tag in this file which has no content. Deleting" + file_path
            os.remove(file_path)
            return
        #try: 
        headText += unicodedata.normalize('NFKD',k['content']).encode('ascii', 'ignore')
        #except: 
        #    print "Conversion to unicode failed."


    #Get description from meta tag with name=description. Likewise, the actual description text lies in the content field.
    description = soup.findAll("meta", attrs ={'name' : 'description'})
    for d in description:
        try:
            temp = d['content']
        except:
            #Since there is no content in the keywords meta tag, this file does not contain descriptions and keywords and a title. Therefore, delete it.
            print "There exists a description meta tag in this file which has no content. Deleting" + file_path
            os.remove(file_path)
            return
        #try: 
        headText += unicodedata.normalize('NFKD',d['content']).encode('ascii', 'ignore')
        #except: 
        #    print "Conversion to unicode failed."

    #This double-checks to make sure the file has keywords, description, and a title.
    if not(keywords!=[] and description!=[] and title!=""):
        print "File does not have all of the following: keywords, description, and title. Deleting " + file_path
        os.remove(file_path)
        return

    print "language: " + get_language(headText)
    if not(get_language(headText)=='english'):
        print "File not in english. Deleting " + file_path
        os.remove(file_path)
        return

    return 




#listofAds = ["adfromhtml.it.html", "adfromnews247.gr.html", "adfromradio.de.html", "adfrom9minecraft.net.html", "adfromaddictinggames.com.html", "adfromallmusic.com.html", "adfromamctheatres.com.html", "adfromandroidcommunity.com.html", "adfromlos40.com.html", "adfromsearch.ch.html", "adfromzalando.pl.html"]
path = "/Users/scottneaves/Desktop/Online Advertising/AdSimiliarity/ads_new"
listing = os.listdir(path)
for infile in listing:
    print infile
    #print "html filename is: " + infile
    html_file = open(os.path.join(path, infile), "r")
    data = html_file.read()
    adsoup = BeautifulSoup(data)
    cleanFiles(adsoup, os.path.join(path, infile))
    print


print "Done cleaning files."    








        
        
        
        

