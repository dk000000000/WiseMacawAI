from module import module
from twitter import twitter

class twitter_menu(module):
    def __init__(self):
        super().__init__()
        self.twitter = twitter()

    def response(self, text, context):
        if "t" not in context.keys():
            context["t"] = {}
            context["t"]["stage"] = 0
            context["twitter"]["stage"] = 0
            return self.intro(text, context) + self.twitter.response(text, context)
        num = context["twitter"]["num"]
        topic_list = context["twitter"]["topic_list"]

        if context["t"]["stage"] == 0:
            if self.yes_representation(text, context) and len(context["twitter"]["tweets"])>1:
                context["twitter"]["stage"] = 2
                return self.twitter.response(text, context)
            elif self.yes_representation(text, context) and len(context["twitter"]["tweets"]) == 1:
                context["twitter"]["stage"] = 2
                context["t"]["stage"] = 1
                return self.twitter.response(text, context)
            else:
                context["twitter"]["topic"] = topic_list[num - 1]['name']
                context["twitter"]["tweets"] = self.twitter.catch_tweets(topic_list[num - 1]['query'])
                context["twitter"]["stage"] = 0
                return self.twitter.response(text, context)
        else:
            context["twitter"]["stage"] = 0
            context["t"]["stage"] = 0
            return self.twitter.response(text, context)





    def intro(self,text,context):
        return "I can read you top-trending tweets. "

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
