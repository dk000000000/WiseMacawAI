class module(object):
    def __init__(self):
        self.testcodes = ["word game",
                            "reddit_search",
                            "twitter_search",
                            "twitter",
                          "ask question",
                          "joke",
                          "chitchat",
                          "chat",
                          "text adventure",
                          "ghost adventure",
                          "horoscope",
                          "riddle game",
                          "message board",
                          "search",
                          "startModule",
                          ]

    def response(self, text, context):
        raise NotImplementedError

    def repeat(self,text,context):
        if "flow" in context:
            context["flow"][1]+=1
        return "<prosody rate=\"x-slow\"> "+context["Conversation"][-2]["text"]+"</prosody> "

    def help(self,text,context):
        help_text = ""
        if "flow" in context:
            context["flow"][1]+=1
            help_text = "Well, I can tell you about news articles and trending tweets I've heard, tell you some jokes, hear your horoscope, answer your questions, show you what's happening on my message board, or we could even play a word game or a riddle game or a text adventure game!"
            help_text += " If we're in the middle of something and you want to do something else, just say back. "
        return help_text

    def pause(self,text,context):
        pause_text = ""
        if "flow" in context:
            context["flow"][1]=0
            context["hold"]=False
            help_text = "Well, I can tell you about news articles and trending tweets I've heard, tell you some jokes, hear your horoscope, answer your questions, show you what's happening on my message board, or we could even play a word game or a riddle game or a text adventure game!"
            help_text += " If we're in the middle of something and you want to do something else, just say back. "
        return pause_text

    def intro(self,text,context):
        return self.response(text,context)
        #raise NotImplementedError
