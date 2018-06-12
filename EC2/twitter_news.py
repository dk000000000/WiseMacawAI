from module import module
from twitter_search import twitter_search

class twitter_news(module):
    def __init__(self):
        super().__init__()
        news = twitter_search()

    def response(self,text,context):
        if "news" not in context.keys():
            context["news"] = {}
            context["news"]["stage"] = 0
            context["twitter_search"] = {}
            context["twitter_search"]["reddit"] = []
            context["twitter_search"]["title"] = ""
            context["twitter_search"]["func"] = "intro"
            return news.response(text,context)

        news.has_response(text,context)
        if context["twitter_search"]["has_response"] == 1:
            context["twitter_search"]["func"] = "title"
            context["news"]["stage"] = 1
            return news.response(text,context)

        if context["news"]["stage"] == 0:
            context["twitter_search"]["func"] = "title"
            try:
                r_text = news.response(text,context)
            except:
                r_text = news.recommend(text,context)
            else:
                pass
            context["news"]["stage"] = 1
            return r_text + ". do you want to hear comments about this?"
        elif context["news"]["stage"] == 1:
            context["twitter_search"]["func"] = "comment"
            if self.yes_representation(text, context) and len(context["twitter_search"]["reddit"]) > 1:
                return news.response(text,context) + " do you want to hear another comment about this?"
            elif self.yes_representation(text, context) and len(context["twitter_search"]["reddit"]) == 1:
                context["news"]["stage"] = 2
                return news.response(text,context) + " do you want to hear  a different piece of news about this?"
            else:
                context["news"]["stage"] = 0
                return "Please tell me  <prosody pitch=\"high\"> a topic </prosody> that you are interested in. "
        else:
            context["twitter_search"]["func"] = "title"
            context["news"]["stage"] = 1
            if self.yes_representation(text, context):
                context["twitter_search"]["func"] == "title_same_topic"
                return news.response(text,context)
            else:
                return news.recommend(text,context)




    def intro(self,text,context):
        return "Sounds like you're interested in twitter news. " \
                "Please tell me  <prosody pitch=\"high\"> a topic </prosody> that you are interested in. "

    def no_representation(self, text, context):
        text = text.lower()
        if (text == "how are you"):
            if (context["intent"] == "AMAZON.NoIntent"):
                return True
            else:
                return False
        if True in [tuple(b.lower().split()) in list(ngrams(text.lower().split(),len(b.lower().split()))) for b in self.nowords]:
            return True
        return False

    def yes_representation(self, text, context):
        text = text.lower()
        if (text == "how are you"):
            if (context["intent"] == "AMAZON.YesIntent"):
                return True
            else:
                return False
        if True in [tuple(b.lower().split()) in list(ngrams(text.lower().split(),len(b.lower().split()))) for b in self.yeswords] :
            return True
        return False
