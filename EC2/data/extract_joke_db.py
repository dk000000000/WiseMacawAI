from lxml import html
import requests
import csv
from operator import itemgetter
import pprint
print("start")
domain = 'http://www.joke-db.com/'
page = requests.get(domain)
tree = html.fromstring(page.content)
responce =  tree.xpath('//li[@class="category"]//a[@href!="javascript:void(0);"]/@href')
catagories = [cat[3:cat.index('clean')-1] for cat in responce]

print("scrap jokes")
types = ['clean','dirty']
Jokes = list()
for cat in catagories:
    for typ in types:
        print(cat,typ)
        first = 1
        link = domain+'c/'+cat+'/'+typ
        curpage = requests.get(link)
        curtree = html.fromstring(curpage.content)
        page_counter = curtree.xpath('//span[@id="page-counter"]/text()')
        #print(link)
        if len(page_counter)!=0:
            counter = page_counter[0].split()
            #print("after")
            last = int(counter[len(counter)-1])
            for i in range(first,last+1):
                page_jokes = [e.text_content() for e in curtree.xpath('//div[@class="joke-box-upper"]')]
                page_ratings = curtree.xpath('//span[@class="jokeScore score badge"]/text()')
                #pprint.pprint(page_jokes)
                for joke in Jokes:
                    if joke[0] in page_jokes:
                        index = page_jokes.index(joke[0])
                        joke.append(cat)
                        page_jokes.pop(index)
                        page_ratings.pop(index)
                #print(len(page_jokes),len(page_ratings))
                Jokes += [ [page_jokes[i],int(page_ratings[i]),typ,cat] for i in range(len(page_jokes))]
                #print(Jokes[len(Jokes)-1])
                if i != last:
                    curpage = requests.get(link+'/page:'+str(i+1))
                    curtree = html.fromstring(curpage.content)
print("save jokes")
with open('joke_db.csv','wb') as f:
    fileWriter = csv.writer(f, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for row in sorted(Jokes, key=itemgetter(1),reverse=False):
        fileWriter.writerow([unicode(s).encode("utf-8") for s in row])
