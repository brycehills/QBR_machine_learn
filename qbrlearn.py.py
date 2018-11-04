import bs4
import numpy as np
from urllib.request import urlopen as request
from bs4 import BeautifulSoup as soup

link = 'http://www.espn.com/nfl/qbr/_/year/2017/type/player-week/week/'
default = link;

for i in range(1,17):
    link = link+str(i)
    print(link)
    link = default;

client = request(link)

page_html = client.read()
client.close()
page_content = soup(page_html, "html.parser")

matrix = np.ones((10,10))

# indirectly finds total number of rows
stat_row = page_content.findAll("td",{"class":"sortcell"})
