from module import module
from reddit_search import reddit_search

class reddit_news(module):
    def __init__(self):
        super().__init__()
        news = reddit_search()

    def response(self,text,context):
        if "reddit" not in context.keys():
            context["reddit"] = {}
            context["reddit"]["stage"] = 0
            context["reddit_search"] = {}
            context["reddit_search"]["reddit"] = []
            context["reddit_search"]["title"] = ""
            context["reddit_search"]["func"] = "intro"
            return news.response(text,context)

        news.has_response(text,context)
        if context["reddit_search"]["has_response"] == 1:
            context["reddit_search"]["func"] = "title"
            context["reddit"]["stage"] = 1
            return news.response(text,context)

        if context["reddit"]["stage"] == 0:
            context["reddit_search"]["func"] = "title"
            try:
                r_text = news.response(text,context)
            except:
                r_text = news.recommend(text,context)
            else:
                pass
            context["reddit"]["stage"] = 1
            return r_text + ". do you want to hear comments about this?"
        elif context["reddit"]["stage"] == 1:
            context["reddit_search"]["func"] = "comment"
            if self.yes_representation(text, context) and len(context["reddit_search"]["reddit"]) > 1:
                return news.response(text,context) + " do you want to hear another comment about this?"
            elif self.yes_representation(text, context) and len(context["reddit_search"]["reddit"]) == 1:
                context["reddit"]["stage"] = 2
                return news.response(text,context) + " do you want to hear  a different piece of news about this?"
            else:
                context["reddit"]["stage"] = 0
                return "Please tell me  <prosody pitch=\"high\"> a topic </prosody> that you are interested in. "
        else:
            context["reddit_search"]["func"] = "title"
            context["reddit"]["stage"] = 1
            if self.yes_representation(text, context):
                context["reddit_search"]["func"] == "title_same_topic"
                return news.response(text,context)
            else:
                return news.recommend(text,context)




    def intro(self,text,context):
        return "Sounds like you're interested in reddit news. " \
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
