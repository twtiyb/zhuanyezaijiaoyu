import requests
from bs4 import BeautifulSoup



loginUrl = 'http://zjpx.hnhhlearning.com/Home/Login/DoHnzjLogin'
account = {'LoginAccount':'41052619900221006X',
           'LoginPassword':'000000',
           'LoginValCode':'04337',
           'LoginType':'0',
            'HnzjLoginTab':'0',
           'X-Requested-With':'XMLHttpRequest'
           }


response = requests.get(loginUrl,account)

soup = BeautifulSoup(response.text, 'lxml')
soup.select('#id1')






