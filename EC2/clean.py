import os
import nltk
from time import time
import re
from nltk import word_tokenize
dir_path = os.getcwd()
nltk.data.path.append(dir_path+"/nltk_data")
badwords = sorted(open('data/dirty.txt','r').read().split('\n'),key = lambda x:len(x),reverse=True)

def clean(text):
    a = time()
    if (text == None):
        return ""
    censor = "<prosody pitch = \"x-high\" rate=\"medium\">  <say-as interpret-as=\"interjection\">beep</say-as></prosody>"
    k = text.lower()
    for e in badwords:
        es = re.escape(e)
        r = r"%s\W|\W%s\W" % (es,es)
        #print(r)
        t = re.sub(r,censor,k)
        if t!=k:
            #print(t)
            k=t
    print(time()-a)
    return k


if __name__=="__main__":
    s = ["Here is a piece of comment with a score of 1 . Fuckin' Frogs! This is great! . . Why don't their buses have ac? Do you want to hear another reddit comment about this?"
    ,"they are so fucking cute"
    , "Oh fuck, all of Brans scenes are gonna be brutal this season, because literally everyone around him is now dead.The Lord of Light isnt done with you yet. I cant wait to see the Hound fucking fucks up with the Brotherhood in Season . Do you want to hear people's comments from Twitter about this news?"
    , "Here is a piece of news from Buzzfeed today. 17 Things Gay Men Want You To Know About Giving Blowjobs. Do you want to hear the body of the news?"
    , "I found something from a search engine that might interest you , Urban Dictionary: Dumb bitch She's that girl who makes you shake your head. She is that dumb bitch ... The Urban Dictionary Mug. ... You're such a dumb bitch."
    , "<prosody pitch = \"x-high\" rate=\"medium\">  <say-as interpret-as=\"interjection\">beep</say-as></prosody>"
    ]
    for e in s:
        print(e)
        print(clean(e))
        print()
