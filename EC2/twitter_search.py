from module import module
import requests, io, time, os, re, string, operator, tweepy, json
import nltk
from nltk.tokenize import word_tokenize
#import boto3
#from boto3.dynamodb.conditions import Key
#from botocore.exceptions import ClientError
from datetime import datetime, timedelta, date
from itertools import groupby
from collections import defaultdict
from nltk.util import ngrams
from dateutil import parser
from nltk.corpus import stopwords
import spacy
import redisClient

class twitter_search(module):
    def __init__(self):
        super().__init__()
        self.table = redisClient.redisClient("twitter")
        dir_path = os.getcwd()
        nltk.data.path.append(dir_path+"/nltk_data")
        words = open('data/stopwords.txt','r').read().split('\n')
        self.stopwords = list(set(nltk.corpus.stopwords.words('english'))|set(words))
        self.nlp = spacy.load('en')
        self.categories = ["business"
                    , "entertainment"
                    , "fashion"
                    , "finance"
                    , "game"
                    , "health"
                    , "lifestyles"
                    , "market"
                    , "news"
                    , "politics"
                    , "science"
                    , "sports"
                    , "technology"]

    def response(self,text,context):
        if "twitter_search" not in context.keys():
            context["twitter_search"] = {}
            context["twitter_search"]["func"] = "title"
            context["twitter_search"]["title"] = ""
        body = ""
        if "has_response" not in context["twitter_search"].keys():
            #store unused news about same topic
            context["twitter_search"]["news_list"] = []
            context["twitter_search"]["has_response"] = 0
            #store used news
            context["twitter_search"]["past"] = []

        if context["twitter_search"]["func"] == "intro":
            return self.intro(text, context)
        elif context["twitter_search"]["func"] == "title":
            #check topic first
            if context["twitter_search"]["has_response"] == 0:
                context["twitter_search"]["news_list"] = []
                self.has_response(text,context)
            if context["twitter_search"]["has_response"] == 1:
                context["twitter_search"]["has_response"] = 0
                if self.fetch_all_news(context):
                    return context["twitter_search"]["title"]
                else:
                    raise Exception()
            else:
                raise Exception()
        elif context["twitter_search"]["func"] == "title_same_topic":
            if self.fetch_all_news(context):
                return context["twitter_search"]["title"]
            else:
                context["twitter_search"]["func"] = "title"
                raise Exception()
        elif context["twitter_search"]["func"] == "comment":
            body = context["twitter_search"]["tweet"].pop(0)
            return ("Here\'s a tweet favorited by %d people.  <prosody pitch=\"high\">" + body + "</prosody> ") % int(context["twitter_search"]["twitter_score"].pop(0) + 1)

    def general(self,text,context):
        if "twitter_search" not in context.keys():
            context["twitter_search"] = {}
            context["twitter_search"]["func"] = "title"
            context["twitter_search"]["title"] = ""
        body = ""
        if "has_response" not in context["twitter_search"].keys():
            #store unused news about same topic
            context["twitter_search"]["news_list"] = []
            context["twitter_search"]["has_response"] = 0
            #store used news
            context["twitter_search"]["past"] = []

        if context["twitter_search"]["func"] == "intro":
            return self.intro(text, context)
        elif context["twitter_search"]["func"] == "title":
            #check topic first
            if context["twitter_search"]["has_response"] == 0:
                context["twitter_search"]["news_list"] = []
                self.recommend_categories(text,context)
            if context["twitter_search"]["has_response"] == 1:
                context["twitter_search"]["has_response"] = 0
                if self.fetch_all_news(context):
                    return context["twitter_search"]["title"]
                else:
                    raise Exception()
            else:
                raise Exception()
        elif context["twitter_search"]["func"] == "comment":
            body = context["twitter_search"]["tweet"].pop(0)
            return ("Here\'s a tweet favorited by %d people.  <prosody pitch=\"high\">" + body + "</prosody> ") % int(context["twitter_search"]["twitter_score"].pop(0) + 1)


    def recommend(self,text,context):
        if "twitter_search" not in context.keys():
            context["twitter_search"] = {}
            context["twitter_search"]["func"] = "title"
            context["twitter_search"]["title"] = ""
        body = ""
        if "has_response" not in context["twitter_search"].keys():
            #store unused news about same topic
            context["twitter_search"]["news_list"] = []
            context["twitter_search"]["has_response"] = 0
            #store used news
            context["twitter_search"]["past"] = []

        if context["twitter_search"]["func"] == "intro":
            return self.intro(text, context)
        elif context["twitter_search"]["func"] == "title":
            try:
                response = self.GetItem("Today_news")
            except:
                raise Exception()
            else:
                if len(response) != 0:
                    context["twitter_search"]["news_list"] = [name for name in response['news'] if name not in context["twitter_search"]["past"]]
                    if self.fetch_all_news(context):
                        return context["twitter_search"]["title"]
                raise Exception()
        elif context["twitter_search"]["func"] == "comment":
            body = context["twitter_search"]["tweet"].pop(0)
            return ("Here\'s a tweet favorited by %d people.  <prosody pitch=\"high\">" + body + "</prosody> ") % int(context["twitter_search"]["twitter_score"].pop(0) + 1)



#===========================================================================
#                       helper functions
#has repsonse will be called after we ask user question
    def has_response(self, text, context):
        if "has_response" not in context["twitter_search"].keys():
            #store used news
            context["twitter_search"]["past"] = []
            #store unused news about same topic
            context["twitter_search"]["news_list"] = []
        filtered_text = self.filter_text(text)
        keywords = self.extract_candidate_words(text.lower())
        news_score = {}
        news_list = []
        redefined_words = list(keywords)
        for word in filtered_text:
            flag = True
            for key in keywords:
                if word in key:
                    flag = False
                    break
            if flag:
                redefined_words.append(word)
        for word in redefined_words:
            news_list.extend(self.get_news_list(word, context))
        if len(news_list) == 0:
            #not find response
            context["twitter_search"]["has_response"] = 2
            return False
        else:
            for name, value in news_list:
                if name not in news_score.keys():
                    news_score[name] = value
                else:
                    news_score[name] += value
            news_list = [k for k, v in sorted(news_score.items(), key=lambda p: p[1], reverse=True)]
            context["twitter_search"]["news_list"] = news_list.copy()
            #find response
            context["twitter_search"]["has_response"] = 1
            return True

    def extract_candidate_words(self, text, good_tags=set(['JJ', 'JJR', 'JJS', 'NN', 'NNP', 'NNS', 'NNPS'])):
        doc = self.nlp(text)
        # for ent in doc.ents:
        #  print ent, ent.label, ent.label_
        candidates = {}
        for n in doc.noun_chunks:
            candidates[str(n)] = 1
        return candidates.keys()

    def recommend_categories(self, text, context):
        if "has_response" not in context["twitter_search"].keys():
            #store used news
            context["twitter_search"]["past"] = []
            #store unused news about same topic
            context["twitter_search"]["news_list"] = []
        filtered_text = self.filter_text(text)
        news_list = []
        for theme in self.categories:
            if theme in filtered_text:
                try:
                    response = self.GetItem(theme+"_news")
                except:
                    return False
                else:
                    if len(response)!=0:
                        context["twitter_search"]["news_list"] = [name for name in response['news'] if name not in context["twitter_search"]["past"]]
                        context["twitter_search"]["has_response"] = 1
                        return True
        context["twitter_search"]["has_response"] = 2
        return False


    def filter_text(self, body):
        text = [word for sent in nltk.sent_tokenize(body) for word in nltk.word_tokenize(sent) if (re.sub("[^a-zA-Z ]", "", word.lower()) not in self.stopwords)]
        text = [word.lower() for word in text if word.isalpha() and word.lower() not in self.stopwords]
        text = [word for word in text if re.search('[a-zA-Z]', word) and len(re.sub("[^a-zA-Z ]", "", word)) > 1]
        candidates = {}
        for word in text:
            candidates[word] = 1
        return candidates.keys()

    #return a list of tuple [(news:score)], all news score are normalized
    def get_news_list(self, word, context):
        news_list = []
        news = {}
        try:
            response = self.GetItem(word)
        except:
            pass
        else:
            if len(response) != 0:
                origin = response
                if len(origin) > 0:
                    for name in origin["news"].keys():
                        if name not in context["twitter_search"]["past"]:
                            news[name] = datetime.strptime(origin["news"][name][1], "%Y-%m-%dT%H:%M:%S")
                    new_news = [k for k, v in sorted(news.items(), key=lambda p: p[1], reverse=True)][:20]
                    if len(new_news) == 0:
                        return news_list.copy()
                    news_score = {}
                    total = 0
                    for news_name in new_news:
                        news_score[news_name] = float.fromhex(origin["news"][name][0])
                        #print ("news_score: " + str(news_score[news_name]))
                        total += news_score[news_name]
                    if total == 0:
                        news_list = [(k, v) for k, v in sorted(news_score.items(), key=lambda p: p[1], reverse=True)]
                    else:
                        news_list = [(k, v*1.0/total) for k, v in sorted(news_score.items(), key=lambda p: p[1], reverse=True)]
        return news_list.copy()

    def fetch_all_news(self, context):
        if len(context["twitter_search"]["news_list"]) == 0:
            return False
        today = date.today()
        while(len(context["twitter_search"]["news_list"]) > 0):
            news = context["twitter_search"]["news_list"].pop(0)
            try:
                response = self.GetItem(news)
            except:
                continue
            else:
                if len(response) == 0:
                    source = response['source']
                    context["twitter_search"]["past"].append(news)
                    news_date = datetime.strptime(response['date'], "%Y-%m-%dT%H:%M:%S")
                    delta = today - news_date.date()
                    context["twitter_search"]["title"] = self.add_time(news,delta.days,source)
                    context["twitter_search"]["tweet"] = response['comment'][:]
                    context["twitter_search"]["twitter_score"] = response['comment_score'][:]
                    return True
                else:
                    continue
        return False

    def intro(self,text,context):
        return "Sounds like you're interested in news. " \
                "Please tell me  <prosody pitch=\"high\"> a topic </prosody> that you are interested in. "

    def add_puncuation(self, body):
        if body[-1] != '?' and body[-1] != '.' and body[-1] != '!':
            body = body + " . "
        return "<prosody rate=\"fast\"  pitch=\"high\">" + body +" </prosody>"

    def add_time(self, latest_news, time_lapse,latest_source):
        latest_news = self.add_puncuation(latest_news)
        if (time_lapse <= 0):
            body = ("I heard a story about that from %s today . "  + latest_news) % latest_source
        elif time_lapse == 1:
            body = ("I heard a story about that from %s yesterday . "  + latest_news) % latest_source
        elif time_lapse == 2:
            body = ("I heard a story about that from %s two days ago . "  + latest_news) % latest_source
        elif time_lapse < 7:
            body = ("I heard a story about that from %s a few days ago . " + latest_news) % latest_source
        elif time_lapse < 14:
            body = ("I heard a story about that from %s last week . "  + latest_news) % latest_source
        else:
            body = ("I heard a story about that from %s few weeks ago . "  + latest_news) % latest_source
        return body


    def GetItem(self, name):
        return json.loads(self.table.getData(name, "json"))
