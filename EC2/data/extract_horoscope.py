from lxml import html
import requests
import time
import csv
from operator import itemgetter
import pprint


def strip_non_ascii(string):
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)


start_time = time.time()


# sign = 1
# month = 7
# day = 12

linelist = list()


for year in range(2016,2017):
    for month in range(2, 3):
        for day in range(30, 32):
            for sign in range(1, 2):
                domain = 'https://www.horoscope.com/us/horoscopes/general/horoscope-archive.aspx?sign='+str(sign)+'&laDate='+str(year)+str(month).zfill(2)+str(day).zfill(2)
                page = requests.get(domain)
                tree = html.fromstring(page.content)
                text = tree.xpath('//div[@class="horoscope-content"]//p/text()')
                if text:
                    print(text)
                    line = [str(year),str(month),str(day),str(sign)]

                    tempText = text[1]
                    tempText = tempText[3:]
                    tempText = tempText[:-1]
                    tempText = strip_non_ascii(tempText)
                    line.append(tempText)
                    # print("\n================")
                    # print(tempText)

                    match = tree.xpath('//div[@class="matches-ratings row text-center"]//h4/text()')[:3]
                    # print(match[0])
                    # print(match[1])
                    # print(match[2])
                    line.extend(match)
                    rating = tree.xpath('//div[@class="row flex-center text-right"]//img[@class="img-responsive"]/@alt')
                    line.extend(rating)
                    linelist.append(line)
                    # print(rating[0])
                    # print(rating[1])
                    # print(rating[2])
                    # print(rating[3])
                    # print("================\n")

#print(linelist[1])

with open('wtf.csv','w') as f:
    writer=csv.writer(f, delimiter='|', quoting=csv.QUOTE_MINIMAL)
    for line in linelist:
        writer.writerow(line)

print("--- %s seconds ---" % (time.time() - start_time))


