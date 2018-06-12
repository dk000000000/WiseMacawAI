import csv
jokelist = [e for e in csv.reader(open("jokes.csv",'r'), delimiter=',')]
badwords = open('en.txt','r').read().split('\n')[:-1]
t = csv.writer(open("joke1.csv","w"), delimiter=',')
for a in jokelist:
    if True not in [b in a[1].lower() for b in badwords]:
        t.writerow(a)
