from module import module
import re, time
import urllib
from lxml import html
import requests

class search(module):
    def __init__(self):
        super().__init__()


    def response(self,text,context):
        #start = time.time()
        query = urllib.parse.quote(text)
        link = 'https://duckduckgo.com/html/?q='+query
        page = requests.get(link)
        tree = html.fromstring(page.content)
        responce =  tree.xpath('//div[@class="result results_links results_links_deep web-result "]')[0]
        title = responce.xpath('//h2[@class="result__title"]/a[@class="result__a"]')[0].text_content()
        snippet = responce.xpath('//a[@class="result__snippet"]')[0].text_content()
        #print (time.time() - start)

        return title + " " + snippet
"""
def main():

    context = {}
    context["flow"] = [0, 1]

    while(True):
        text = input("User: " )
        text_back = response1(text, context)
        print("Bots: " + text_back)

if __name__ == "__main__":
   main()
"""
