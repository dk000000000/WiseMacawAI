from twitter_search import twitter_search
from twitter import twitter
import os, nltk, random
from nltk.util import ngrams
from nltk.tokenize import word_tokenize

class Trendsetter:
    def __init__(self):
        self.module = twitter_search()
        self.twitter = twitter()
        self.yeswords = open('data/yes.txt','r').read().split('\n')#last line without next line
        self.nowords = open('data/no.txt','r').read().split('\n')#last line without next line
        dir_path = os.getcwd()
        nltk.data.path.append(dir_path+"/nltk_data")
        self.trend = ["top", "trending", "hashtag", "hash", "tag", "first"]
        self.topic = ["topic", "topics", "focus", "tell", "last", "second"]
        self.general = ["general", "first"]
        self.specific = ["specific", "last", "second"]

    #context["twitter_search"]["func"]
    #"intro", "title", "title_same_topic", "comment"
    def response(self, text, context):
        context["Trendsetter"]["turn"] += 1
        #next time enter
        if context["Trendsetter"]["stage"] == -1:
            if not context["Trendsetter"]["win"]:
                context["Trendsetter"]["turn"] = 0
                context["Trendsetter"]["stage"] = 0
                return "You find your way back to the Trendsetter\'s corner. She looks"\
                " up briefly to let you know she\'s seen you. \"Hey again,\" she says,"\
                " \"still dying to get these things trending. Listen to a couple and "\
                "I\'ll tell you what I\'ve heard. Sound good? Yes, or no?\""
            else:
                context["Trendsetter"]["turn"] = 0
                context["Trendsetter"]["stage"] = 0
                return "You find your way back to the Trendsetter\'s corner. She looks"\
                " up as you approach and waves cheerily. \"You\'re back!\" she says,"\
                " \"I heard something new about the chatbot\'s voice, and I\'m still"\
                " dying to get these things trending. Listen to a couple and I\'ll "\
                "tell you what I\'ve heard. Sound good? Yes, or no?\""
        #step A, B, C, D
        elif context["Trendsetter"]["stage"] == 0:
            #win
            if context["Trendsetter"]["turn"] > 10:
                context["Trendsetter"]["turn"] = 0
                context["Trendsetter"]["win"] = True
                # Return the user to the entrance of SOUTHERN SQUARE.
                context["status"]=["South","inArea","response"]
                context["Trendsetter"]["stage"] = -1
                if not context["hintIndex"] >= len(context["hints"]):
                    hint = context["hints"][context["hintIndex"]]
                    context["hintIndex"] += 1
                    context["givehint"] = True
                else:
                    hint = ""
                return "The trendsetter goes away from her phone. \"Thanks for "\
                "helping me keep this place lively,\" she says. \"Here\'s what I\'"\
                "ve heard.\" " + hint + " The detective quickly jots"\
                " it down in her notebook, then hurries you back to Central Station."\
                " \"You handled the moderator well,\" she says. "
            #A
            elif self.yes_representation(text, context):
                context["Trendsetter"]["stage"] = 1
                return "\"Great!\" she says, swiping energetically on her phone."\
                " \"I\'ll give you a choice. Do you want me to talk about the top"\
                " trending hashtags on twitter, or would you rather tell me a topic to focus on?"
            #B
            elif self.no_representation(text, context):
                # Return the user to the entrance of SOUTHERN SQUARE.
                context["status"]=["South","inArea","response"]
                context["Trendsetter"]["stage"] = -1
                return "\"Bummer,\" she says, \"but I\'ll be here if you change "\
                "your mind.\" With that, she turns back to her phone. You make "\
                "your way back at the outskirts of southern square. The detective"\
                " turns to you. \"So, who should we talk to?\" she asks, \"The "\
                "Moderator, or the Trendsetter? If you think we should check "\
                "somewhere else, just tell me a direction and we\'ll go there.\""
            #C
            else:
                return "The Trendsetter raises an eyebrow. \"Umm, sorry, what "\
                "was that?\" she asks confusedly. \"Yes, you want to hear some "\
                "tweets, or no, you don\'t?\""
        #a,b,c
        elif context["Trendsetter"]["stage"] == 1:
            #a
            if True in [(w in self.trend) for w in word_tokenize(text.lower())]:
                context["twitter"]["stage"] = 0
                context["Trendsetter"]["stage"] = 2
                context["Trendsetter"]["func"] = "trend"
                return self.twitter.response(text, context)
            #b
            elif True in [(w in self.topic) for w in word_tokenize(text.lower())]:
                context["Trendsetter"]["func"] = "news"
                context["Trendsetter"]["stage"] = 2
                return "\"Do you want to hear about a general topic, or something specific?\""
            #c
            else:
                return "The Trendsetter raises an eyebrow. \"Umm, sorry, what was"\
                " that?\" she asks confusedly. \"Do you want to hear about the top"\
                " trending hashtags, or tell me a topic to focus on?\""
        #i,ii
        elif context["Trendsetter"]["stage"] == 2:
            #a i,ii
            if context["Trendsetter"]["func"] == "trend":
                #i
                if self.yes_representation(text, context):
                    context["twitter"]["stage"] = 1
                    context["Trendsetter"]["stage"] = 3
                    return self.twitter.response(text, context) + " she says. \"Want to hear another one?\""
                #ii
                else:
                    context["twitter"]["stage"] = 0
                    return self.twitter.response(text, context)
            #b  i, ii, iii
            elif context["Trendsetter"]["func"] == "news":
                if True in [(w in self.general) for w in word_tokenize(text.lower())]:
                    context["Trendsetter"]["func"] = "general"
                    context["Trendsetter"]["stage"] = 3
                    general_topic = self.module.categories
                    index = random.sample(range(len(general_topic)), 3)
                    context["Trendsetter"]["topic_list"] = [general_topic[index[0]], general_topic[index[1]], general_topic[index[2]]]
                    return " \"Okay!\" she says, looking down to her phone, \"do"\
                    " you want to hear about\" %s, %s, or %s?" % (general_topic[index[0]], general_topic[index[1]], general_topic[index[2]])
                elif True in [(w in self.specific) for w in word_tokenize(text.lower())]:
                    context["Trendsetter"]["func"] = "specific"
                    context["Trendsetter"]["stage"] = 3
                    return " \"Okay!\" she says, looking down at her phone. \"Go"\
                    " ahead and tell me the topic you want to hear about.\""
                else:
                    return "The Trendsetter raises an eyebrow. \"Umm, sorry, what"\
                    " was that?\" she asks confusedly. \"General, you want to hear "\
                    "a general topic; or specific, you want to a specific one?\""
        #1,2
        elif context["Trendsetter"]["stage"] == 3:
            #a i 1,2
            if context["Trendsetter"]["func"] == "trend":
                #1
                if self.yes_representation(text, context):
                    context["twitter"]["stage"] = 2
                    return self.twitter.response(text, context) + " she says. \"Want to hear another one?\""
                #2
                else:
                    context["twitter"]["stage"] = 0
                    context["Trendsetter"]["stage"] = 2
                    return self.twitter.response(text, context)
            #b i 1,2,3
            elif context["Trendsetter"]["func"] == "general":
                #2
                if self.no_representation(text, context):
                    context["Trendsetter"]["func"] = "general_no"
                    context["Trendsetter"]["stage"] = 4
                    return " \"Oh, well that\'s okay,\" she says, sounding just "\
                    "the slightest bit disappointed. \"Want to tell me a specific topic instead? Yes, or no?\""
                #2,3
                else:
                    if "first" in text.lower():
                        text = context["Trendsetter"]["topic_list"][0]
                    elif "second" in text.lower():
                        text = context["Trendsetter"]["topic_list"][1]
                    elif "third" in text.lower() or "last" in text.lower():
                        text = context["Trendsetter"]["topic_list"][2]
                    #1
                    if self.module.recommend_categories(text, context):
                        context["Trendsetter"]["stage"] = 4
                        context["Trendsetter"]["func"] = "tweet_general"
                        context["twitter_search"]["func"] = "title"
                        return "\"Ooo, that\'s a good one,\" she says, swiping "\
                        "on her phone. \"" +self.module.general(text, context)+ "\"Want"\
                        " to hear what people are tweeting about that?\""
                    #3
                    else:
                        return " Sorry, I didn\'t really understand,\" she says."\
                        " \"Do you want to hear about\" %s, %s, or %s, or none of"\
                        " these?\"" % (general_topic[index[0]], general_topic[index[1]], general_topic[index[2]])
            #b ii 1,2,3
            elif context["Trendsetter"]["func"] == "specific":
                context["twitter_search"]["func"] = "title"
                context["Trendsetter"]["func"] = "tweet_specific"
                context["Trendsetter"]["stage"] = 4
                #1
                if self.module.has_response(text, context):
                    return "\"Ooo interesting one,\" she says, swiping up on her"\
                    " phone. \"" +  self.module.response(text, context) + "\"Want"\
                    " to hear what people are tweeting about that?\""
                else:
                    return "\"Oh, umm, I haven\'t really heard anything about "\
                    "that,\" the trendsetter says sheepishly, \"but I have heard"\
                    " something else interesting.\" "+ self.module.recommend(text, context)+ " \""\
                    "Want to hear what people are tweeting about that?\""
        #b i 1,a
        elif context["Trendsetter"]["stage"] == 4:
            # 1 i a,b
            if context["Trendsetter"]["func"] == "tweet_general":
                #a
                if self.yes_representation(text, context):
                    context["Trendsetter"]["stage"] =  5
                    context["twitter_search"]["func"] = "comment"
                    return " \"Great! Here\'s a tweet,\" she says." + self.module.response(text, context) +" \"Want to hear another one?\""
                #b
                else:
                    context["Trendsetter"]["func"] = "general"
                    context["Trendsetter"]["stage"] = 3
                    general_topic = self.module.categories
                    index = random.sample(range(len(general_topic)), 3)
                    context["Trendsetter"]["topic_list"] = [general_topic[index[0]], general_topic[index[1]], general_topic[index[2]]]
                    return " \"Okay!\" she says, looking down to her phone, \"do"\
                    " you want to hear about\" %s, %s, or %s?" % (general_topic[index[0]], general_topic[index[1]], general_topic[index[2]])
            elif context["Trendsetter"]["func"] == "general_no":
                #2 a,b
                #a
                if self.yes_representation(text, context):
                    context["Trendsetter"]["func"] = "specific"
                    context["Trendsetter"]["stage"] = 3
                    return " \"Okay!\" she says, looking down at her phone. \"Go"\
                    " ahead and tell me the topic you want to hear about.\""
                #b
                else:
                    context["Trendsetter"]["stage"] = 1
                    return " \"Oh, that\'s okay too,\" she says, looking a bit "\
                    "confused. \"Great!\" she says, swiping energetically on her"\
                    " phone. \"I\'ll give you a choice. Do you want me to talk about"\
                    " the top trending hashtags on twitter, or would you rather tell"\
                    " me a topic to focus on?"
            #ii 1
            elif context["Trendsetter"]["func"] == "tweet_specific":
                #a
                if self.yes_representation(text, context):
                    context["Trendsetter"]["stage"] =  5
                    context["twitter_search"]["func"] = "comment"
                    return " \"Great! Here\'s a tweet,\" she says." + self.module.response(text, context) +" \"Want to hear another one?\""
                #b
                else:
                    context["Trendsetter"]["func"] = "specific"
                    context["Trendsetter"]["stage"] = 3
                    return " \"Okay!\" she says, looking down at her phone. \"Go"\
                    " ahead and tell me the topic you want to hear about.\""
        #i,ii
        elif context["Trendsetter"]["stage"] == 5:
            if self.yes_representation(text, context) and len(context["twitter_search"]["tweet"]) > 0:
                context["twitter_search"]["func"] = "comment"
                return " \"Great! Here\'s a tweet,\" she says." + self.module.response(text, context) +" \"Want to hear another one?\""
            else:
                if context["Trendsetter"]["func"] == "tweet_general":
                    context["Trendsetter"]["func"] = "general"
                    context["Trendsetter"]["stage"] = 3
                    general_topic = self.module.categories
                    index = random.sample(range(len(general_topic)), 3)
                    context["Trendsetter"]["topic_list"] = [general_topic[index[0]], general_topic[index[1]], general_topic[index[2]]]
                    return " \"Okay!\" she says, looking down to her phone, \"do"\
                    " you want to hear about\" %s, %s, or %s?" % (general_topic[index[0]], general_topic[index[1]], general_topic[index[2]])
                else:
                    context["Trendsetter"]["func"] = "specific"
                    context["Trendsetter"]["stage"] = 3
                    return " \"Okay!\" she says, looking down at her phone. \"Go"\
                    " ahead and tell me the topic you want to hear about.\""

    def repeat(self,text,context):
        return "<prosody rate=\"x-slow\"> "+context["Conversation"][-2]["text"]+"</prosody> "

    def help(self,text,context):
        if context["Trendsetter"]["stage"] == 0:
            help_text = "Hey,\" the detective whispers, \"I think she just wants"\
            " you to say yes or no.\""
        elif context["Trendsetter"]["stage"] == 1:
            help_text = " \"I think she\'s offering to give you some trending "\
            "hashtags or let you pick a topic,\" the detective whispers. \"Just "\
            "tell her either trending, or topics.\""
        elif context["Trendsetter"]["stage"] == 2:
            if context["Trendsetter"]["func"] == "news":
                help_text = "\"Hey,\" the detective whispers, \"she\'s offering "\
                "to focus on either general or specific topics. Just say either general, or specific.\""
        elif context["Trendsetter"]["stage"] == 3:
            if context["Trendsetter"]["func"] == "general":
                help_text = "\"Hmm,\" whispers the detective, \"sounds like she "\
                "wants you to tell her which of those three topics to hear about."\
                " Go ahead and say one of them.\""
            elif context["Trendsetter"]["func"] == "specific":
                help_text = "\"She wants you to tell her a specific topic to talk"\
                " about,\" the detective whispers, gesturing at the trendsetter."\
                " \"Just say whatever you want to hear about.\""
        if help_text == "":
            help_text = "\"Sounds like she wants to know if you want to keep listening "\
            "to what people has to tweet about this issue,\" the detective whispers. \"Just say yes or no.\""
        if context["hintIndex"] >= 3:
            return help_text + "\"By the way,\" the detective continues, \"if "\
            "you want me to read you the hints you\'ve gathered, say, HINT. And "\
            "if you want to accuse The Moderator, just say, ACCUSE.\""
        return help_text

    def pause(self,text,context):
        pause_text = " \"Bummer,\" the trendsetter says, \"but I\'ll be here if "\
        "you change your mind.\" With that, she turns back to her phone. You make"\
        " your way back at the edge of southern square. The detective turns to you."\
        " \"So, who should we talk to?\" she asks, \"The Moderator, or the "\
        "Trendsetter? If you think we should check somewhere else, just tell me a direction and we\'ll go there.\""
        # Return the user to the entrance of SOUTHERN SQUARE.
        context["status"]=["South","inArea","response"]
        context["Trendsetter"]["stage"] = -1
        return pause_text

    def intro(self,text,context):
        if "Trendsetter" not in context.keys():
            context["Trendsetter"] = {}
            context["Trendsetter"]["win"] = False
            context["Trendsetter"]["turn"] = 0
            context["Trendsetter"]["stage"] = 0
            context["Trendsetter"]["topic_list"] = []
            context["Trendsetter"]["func"] = "trend"
            self.twitter.twitter_init(context)
            if "twitter_search" not in context.keys():
                context["twitter_search"] = {}
                context["twitter_search"]["func"] = "title"
                context["twitter_search"]["title"] = ""
            return "You make your way to a busy corner of the square. There, a "\
            "young woman in a business suit with long, curly hair is tapping "\
            "hastily on her phone. The crowd around her is doing the same, "\
            "chatting loudly as they do. She looks up just as you approach. \"Oh,"\
            " hey,\" she says, \"Trendsetter here. Wait, don\'t tell me, the "\
            "chatbot\'s voice, am I right? Well, I\'ve got some things I\'m just"\
            " dying to get trending. Listen to a couple and I\'ll tell you what I know. Sound good? Yes, or no?\""
        elif not context["Trendsetter"]["win"]:
            context["Trendsetter"]["turn"] = 0
            context["Trendsetter"]["stage"] = 0
            return "You find your way back to the Trendsetter\'s corner. She looks"\
            " up briefly to let you know she\'s seen you. \"Hey again,\" she says,"\
            " \"still dying to get these things trending. Listen to a couple and "\
            "I\'ll tell you what I\'ve heard. Sound good? Yes, or no?\""
        else:
            context["Trendsetter"]["turn"] = 0
            context["Trendsetter"]["stage"] = 0
            return "You find your way back to the Trendsetter\'s corner. She looks"\
            " up as you approach and waves cheerily. \"You\'re back!\" she says,"\
            " \"I heard something new about the chatbot\'s voice, and I\'m still"\
            " dying to get these things trending. Listen to a couple and I\'ll "\
            "tell you what I\'ve heard. Sound good? Yes, or no?\""
        return self.module.response(text,context)

    def get_caught(self,context):
        """Returns the text for when the bartender is the thief and gets accused.
            Does the following bookkeeping:
                Notes that the bartender has been removed.
                Brings the user back to central station.
                Starts the first end prompt.
        """

        caught_text = "The detective searches her sport jacket and pulls out"\
        " a small urn. Somehow, you know the chatbot's voice is in there. The"\
        " Trendsetter huffs, but lets the detective cuff her. \"You don't get"\
        " it,\" she says irritatedly, \"I could force the whole world to listen"\
        " to me with that voice. Absolutely everything that I do could be trending!"\
        "\" But before she can say more, the detective leads her off in handcuffs."\
        " \"Nice work,\" she says, \"you caught the thief! Any last words for her?\""

        # Note the removal
        context["removed"] = "Trendsetter"
        # Bring the user back to Central Station
        context["status"]=["Center","inArea","response"]
        context["Trendsetter"]["stage"] = -1
        # Start the first end prompt (on the next turn). Setting the context["end"] variable to 0 will accomplish this in Game.py.
        context["end"] = 0

        return caught_text
#===========================================================================
#                       helper functions

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
