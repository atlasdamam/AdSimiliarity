import urllib2
import re
from bs4 import BeautifulSoup

url="https://www.google.com/#safe=off&output=search&sclient=psy-ab&q=cars&oq=cars&gs_l=hp.3..0l4.927.1451.0.1662.4.4.0.0.0.0.239.582.1j2j1.4.0...0.0...1c.1.9.psy-ab.lPCE5MGPxh8&pbx=1&bav=on.2,or.r_cp.r_qf.&bvm=bv.45175338,d.b2I&fp=74349a4cebae5db4&biw=1517&bih=705"

#page content 
page = urllib2.urlopen(url).read()
soup = BeautifulSoup(page)


adlinks = soup.findAll('a')

for ad in adlinks:
    print ad
    
