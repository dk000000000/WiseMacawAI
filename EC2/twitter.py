from module import module
from collections import defaultdict
import json, operator, tweepy, time, re, os, nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
class twitter(module):
    def __init__(self):
        super().__init__()
        api_key = ''#differen from fetch
        api_secret = ''
        access_token = ''
        access_token_secret = ''

        #Connecting twitter API
        auth = tweepy.OAuthHandler(api_key, api_secret)
        auth.set_access_token(access_token, access_token_secret)

        #Get the api
        self.api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        dir_path = os.getcwd()
        nltk.data.path.append(dir_path+"/nltk_data")
        self.yeswords = open('data/yes.txt','r').read().split('\n')
        self.nowords = open('data/no.txt','r').read().split('\n')
        self.stopwords = nltk.corpus.stopwords.words('english')

    def fomate_tweet(self,text):
        return re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z' \t])|(\w+:\/\/\S+)","", text)

    def help(self,text,context):
        return ("I can read you top-trending tweets, but you can also search for specific topics yourself."\
            " Just say . tweets about . followed by the name of a topic and I'll search for tweets about that topic."\
            " Unfortunately, I can't search for specific twitter handles.")
    def catch_tweets(self, text):
        unsortedtweets = []
        tweet_content = defaultdict(int)
        tweets = []
        try:
            unsortedtweets = tweepy.Cursor(self.api.search, q=text, count=100, result_type="popular", include_entities=True, lang="en").items(100)
        except Exception as e:
            pass
        else:
            for tweet in unsortedtweets:
                #Find the most popular text
                x = self.fomate_tweet(tweet.text)
                if len(x) > 3:
                    tweet_content[x] = tweet.favorite_count
            tweets = sorted(tweet_content.items(), key=operator.itemgetter(1), reverse=True)
        return tweets

    def catch_trend(self):
        return self.api.trends_place(23424977)[0]['trends']

    def no_representation(self, text, context):
        text = text.lower()
        if (text == "how are you"):
            if (context["intent"] == "AMAZON.NoIntent"):
                return True
        if True in [b.lower() in text.lower() for b in self.nowords] :
            return True
        return False

    def add_puncuation(self, body):
        if body[-1] != '?' and body[-1] != '.':
            body = body + "."
        return "<prosody pitch=\"high\">" + body +" </prosody>"

    def yes_representation(self, text, context):
        text = text.lower()
        if (text == "how are you"):
            if (context["intent"] == "AMAZON.YesIntent"):
                return True
        if True in [b.lower() in text.lower() for b in self.yeswords] :
            return True
        return False

    def construct_body(self, tweet):
        count = tweet[1]
        text = tweet[0]
        body = ("Great! Here's a favorited by <prosody pitch=\"high\"> %d people.  </prosody> " + self.add_puncuation(text)) % count
        return body

    def twitter_init(self, context):
        context["twitter"] = {}
        context["twitter"]["topic_list"] = self.catch_trend()
        context["twitter"]["stage"] = 0
        context["twitter"]["num"] = 0
        context["twitter"]["tweets"] = []
        context["twitter"]["topic"] = context["twitter"]["topic_list"][0]['name']


    def response(self, text, context):
        start = time.time()
        topic_list = context["twitter"]["topic_list"]
        num = context["twitter"]["num"]
        if context["twitter"]["stage"] == 0:
            context["twitter"]["num"] += 1
            return " \"Okay!\" she says, \"this tag,\" %s, \"is pretty popular. Want to hear a tweet from it?\"" % (self.fomate_tweet(topic_list[num]['name']))
        elif context["twitter"]["stage"] == 1:
            context["twitter"]["topic"] = topic_list[num - 1]['name']
            context["twitter"]["tweets"] = self.catch_tweets(topic_list[num - 1]['query'])
            return self.construct_body(context["twitter"]["tweets"].pop(0))
        elif context["twitter"]["stage"] == 2:
            return self.construct_body(context["twitter"]["tweets"].pop(0))

"""
if __name__ == "__main__":
    n = twitter()
    context = {}
    context["flow"] = [0, 1]
    context["Conversation"]=[{"functionality":11},{"functionality":11},{"functionality":11}]
    while(True):
        text = input("User: " )
        text_back = n.response(text, context)
        print(text_back)
"""
