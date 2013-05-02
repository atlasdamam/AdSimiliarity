import json
import AlchemyAPI
import unicodedata



# Create an AlchemyAPI object.
alchemyObj = AlchemyAPI.AlchemyAPI()

# Load the API key from disk.
alchemyObj.loadAPIKey("api_key.txt")


URL = "http://style.justfab.com/dms3733/?cvosrc=display.1366044.0&m_campaign=7218780&m_medium=97228490&m_content=0&pid=97228490&aid=271379042,271379042&cid=0,0&placement=DBLCLK%20UNASSIGNED:%20PID%2097228490"

# Categorize a web URL.
result = alchemyObj.URLGetCategory(URL);
print result



# Extract topic keywords from a web URL.
result = alchemyObj.URLGetRankedKeywords(URL);
print result

'''
# Load a HTML document to analyze.
htmlFileHandle = open("data/example.html", 'r')
htmlFile = htmlFileHandle.read()
htmlFileHandle.close()


# Categorize a HTML document.
result = alchemyObj.HTMLGetCategory(htmlFile, "http://www.test.com/");
print result
'''



