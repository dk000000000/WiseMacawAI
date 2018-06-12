from reddit_search import reddit_search
import os, nltk
from nltk.util import ngrams

class Moderator:
    def __init__(self):
        self.module = reddit_search()
        self.yeswords = open('data/yes.txt','r').read().split('\n')#last line without next line
        self.nowords = open('data/no.txt','r').read().split('\n')#last line without next line
        dir_path = os.getcwd()
        nltk.data.path.append(dir_path+"/nltk_data")

    #context["reddit_search"]["func"]
    #"intro", "title", "title_same_topic", "comment"
    #context["Moderator"]["turn"] counts for turns of the reddit npc
    #context["Moderator"]["stage"] record the stage of each step
    def response(self, text, context):
        context["Moderator"]["turn"] += 1
        if context["Moderator"]["stage"] == -1:
            if not context["Moderator"]["win"]:
                context["Moderator"]["turn"] = 0
                context["Moderator"]["stage"] = 0
                return "You find your way to the moderator\'s news stand. \"You\'re "\
                "back!\" he exclaims over the din of the crowd. \"My offer still stands."\
                " Help me keep this discussion moving along, and I\'ll tell you what"\
                " I know. Is that a deal? Yes, or no?\""
            else:
                context["Moderator"]["turn"] = 0
                context["Moderator"]["stage"] = 0
                return "You find your way to the moderator\'s news stand. \"Welcome "\
                "back!\" he manages over the noise of the crowd. \"I have new news about "\
                "the chatbot\'s voice, but I still need to keep this forum alive. Help"\
                " me keep this discussion moving along, and I\'ll tell you what else "\
                "I know. Is that a deal? Yes, or no?\""
        #step A, B, C, D
        elif context["Moderator"]["stage"] == 0:
            #win
            if context["Moderator"]["turn"] > 8:
                context["Moderator"]["turn"] = 0
                context["Moderator"]["win"] = True
                # Return the user to the entrance of SOUTHERN SQUARE.
                context["status"]=["South","inArea","response"]
                if not context["hintIndex"] >= len(context["hints"]):
                    hint = "\"Here\'s what I\'ve heard.\"" + context["hints"][context["hintIndex"]]
                    context["hintIndex"] += 1
                    context["givehint"] = True
                else:
                    hint = " that's all i know"
                return "The moderator turns away from the crowds. \"Thanks for "\
                "helping me keep this place lively,\" he says. " + context["hints"] + " The detective quickly jots it down in her notebook, "\
                "then hurries you back to Central Station. \"You handled the moderator well,\""\
                " she says."
            #A
            elif self.yes_representation(text, context):
                context["Moderator"]["stage"] = 1
                return " \"Alright,\" says the moderator, \"go ahead and tell me"\
                " a topic that we can discuss.\""
            #B
            elif self.no_representation(text, context):
                # Return the user to the entrance of SOUTHERN SQUARE.
                context["status"]=["South","inArea","response"]
                context["Moderator"]["stage"] = -1
                return " \"Oh?\" says the moderator, \"well, suit yourself. Come "\
                "back anytime, I\'m always here working.\" You find yourself back "\
                "at the outskirts of southern square. The detective turns to you. "\
                " \"So, who should we talk to?\" she asks, \"The Moderator, or the "\
                "Trendsetter? If you think we should check somewhere else, just tell"\
                " me a direction and we\'ll go there.\""
            #C
            else:
                return "The moderator cups a hand over his ear. \"What was that?\" "\
                "he asks loudly over the crowd, \"Yes, you want to help me keep the "\
                "forum going, or no, you do not?\""
        #step a, b
        elif context["Moderator"]["stage"] == 1:
            if self.no_representation(text, context):
                # Return the user to the entrance of SOUTHERN SQUARE.
                context["status"]=["South","inArea","response"]
                context["Moderator"]["stage"] = -1
                return " \"Oh?\" says the moderator, \"well, suit yourself. Come "\
                "back anytime, I\'m always here working.\" You find yourself back "\
                "at the outskirts of southern square. The detective turns to you. "\
                " \"So, who should we talk to?\" she asks, \"The Moderator, or the "\
                "Trendsetter? If you think we should check somewhere else, just tell"\
                " me a direction and we\'ll go there.\""
            context["Moderator"]["stage"] = 2
            context["reddit_search"]["func"] = "title"
            #step a
            if self.module.has_response(text,context):
                reply = self.module.response(text, context)
                surround = " \"Hmm,\" ponders the moderator, \" %s \" Do you think "\
                "that\'s a good issue to discuss? Yes, or no?"
                return surround % reply
            #step b
            else:
                reply = self.module.recommend(text, context)
                surround = "\"Hmm,\" ponders the moderator, \"I don\'t think the "\
                "people here would be interested in that. But %s \"  Do you think "\
                "that\'s a good issue to discuss? Yes, or no?"
                return surround % reply
        #step i, ii, iii
        elif context["Moderator"]["stage"] == 2:
            #i
            if self.yes_representation(text, context):
                context["reddit_search"]["func"] = "comment"
                reply = self.module.response(text, context)
                surround = "The moderator reads the issue aloud. \"I have something "\
                "to say about that,\" someone bellows above the crowd. %s \"Want "\
                "to hear what else they have to say? Yes, or no?\" The moderator asks."
                return surround % reply
            #ii
            elif self.no_representation(text, context):
                context["Moderator"]["stage"] = 1
                return " \"Alright,\" says the moderator, \"go ahead and tell me "\
                "a topic that we can discuss.\""
            else:
                return "The moderator cups a hand over his ear. \"What was that?\" "\
                "he asks loudly over the crowd, Should we discuss this issue? Yes, or no?\""
        #step 1, 2, 3
        elif context["Moderator"]["stage"] == 3:
            #1,2
            if self.yes_representation(text, context):
                #2
                if len(context["reddit_search"]["reddit"]) == 0:
                    context["Moderator"]["stage"] = 1
                    return "You and the moderator perk your ears, but no-one else "\
                    "speaks up from the crowd. The moderator shrugs his shoulders. "\
                    " \"Alright,\" says the moderator, \"go ahead and tell me a "\
                    "topic that we can discuss.\""
                #1
                else:
                    context["reddit_search"]["func"] = "comment"
                    reply = self.module.response(text, context)
                    surround = "The moderator reads the issue aloud. \"I have "\
                    "something to say about that,\" someone bellows above the crowd. %s "\
                    "\"Want to hear what else they have to say? Yes, or no?\" The moderator asks."
                    return surround % reply
            #3
            else:
                context["Moderator"]["stage"] = 1
                return " \"Alright,\" says the moderator, \"go ahead and tell me "\
                "a topic that we can discuss.\""

    def repeat(self,text,context):
        return "<prosody rate=\"x-slow\"> "+context["Conversation"][-2]["text"]+"</prosody> "

    def help(self,text,context):
        if context["Moderator"]["stage"] == 0:
            help_text = "\"Sounds like he wants to know if you want to help him "\
            "keep the forum alive,\" the detective whispers. \"Just say yes or no.\""
        elif context["Moderator"]["stage"] == 1:
            help_text = "\"He\'s asking you to suggest a topic of discussion,\" "\
            "the detective whispers. \"Go ahead, tell him a topic.\""
        elif context["Moderator"]["stage"] == 2:
            help_text = "\"He wants your opinion on whether he should read the "\
            "issue to the crowd,\" the detective whispers. \"Go ahead and tell him yes or no.\""
        elif context["Moderator"]["stage"] == 3:
            help_text = "\"Sounds like he wants to know if you want to keep listening "\
            "to what the crowd has to say about this issue,\" the detective whispers. \"Just say yes or no.\""
        if context["hintIndex"] >= 3:
            return help_text + "\"By the way,\" the detective continues, \"if "\
            "you want me to read you the hints you\'ve gathered, say, HINT. And "\
            "if you want to accuse The Moderator, just say, ACCUSE.\""
        return help_text

    def pause(self,text,context):
        pause_text = " \"Oh?\" says the moderator, \"well, suit yourself. Come "\
        "back anytime, I\'m always here working.\" You find yourself back at the "\
        "outskirts of southern square. The detective turns to you. \"So, who should"\
        " we talk to?\" she asks, \"The Moderator, or the Trendsetter? If you think"\
        " we should check somewhere else, just tell me a direction and we\'ll go there.\""
        # Return the user to the entrance of SOUTHERN SQUARE.
        context["Moderator"]["stage"] = -1
        context["status"]=["South","inArea","response"]
        return pause_text

    def intro(self,text,context):
        if "Moderator" not in context.keys():
            context["Moderator"] = {}
            context["Moderator"]["win"] = False
            context["Moderator"]["turn"] = 0
            context["Moderator"]["stage"] = 0
            if "reddit_search" not in context.keys():
                context["reddit_search"] = {}
                context["reddit_search"]["func"] = "title"
                context["reddit_search"]["reddit"] = []
                context["reddit_search"]["title"] = ""
            return "You find your way to a small amphitheater in the very center"\
            " of the square. There, a young man in a business suit with short, "\
            "black hair is leading a crowd of loudly chattering people in a discussion."\
            " \"Hi, yes! I\'ve already heard,\" he says. \"I\'m the moderator. "\
            "You\'re here about the chatbot\'s voice, right? Well, I need help "\
            "keeping this forum alive. Help me keep this discussion moving along,"\
            " and I\'ll tell you what I know. Is that a deal? Yes, or no?\""
        elif not context["Moderator"]["win"]:
            context["Moderator"]["turn"] = 0
            context["Moderator"]["stage"] = 0
            return "You find your way to the moderator\'s news stand. \"You\'re "\
            "back!\" he exclaims over the din of the crowd. \"My offer still stands."\
            " Help me keep this discussion moving along, and I\'ll tell you what"\
            " I know. Is that a deal? Yes, or no?\""
        else:
            context["Moderator"]["turn"] = 0
            context["Moderator"]["stage"] = 0
            return "You find your way to the moderator\'s news stand. \"Welcome "\
            "back!\" he manages over the noise of the crowd. \"I have new news about "\
            "the chatbot\'s voice, but I still need to keep this forum alive. Help"\
            " me keep this discussion moving along, and I\'ll tell you what else "\
            "I know. Is that a deal? Yes, or no?\""


    def get_caught(self,context):
        """Returns the text for when the bartender is the thief and gets accused.
            Does the following bookkeeping:
                Notes that the bartender has been removed.
                Brings the user back to central station.
                Starts the first end prompt.
        """

        caught_text = "The detective searches behind a podium and finds a small "\
        "urn. Somehow, you know the chatbot's voice is in there. The moderator "\
        "tries to snatch it back, but falls into the middle of the amphitheater. "\
        "\"You don't understand!\" he says. \"With that voice, I could control "\
        "every conversation in the world. I could finally moderate what everyone"\
        " says!\" But before he can say any more, the detective leads him off in"\
        " handcuffs. \"Nice work,\" she says, \"you caught the thief! Any last words for him?"

        # Note the removal
        context["removed"] = "Moderator"
        context["Moderator"]["stage"] = -1
        # Bring the user back to Central Station
        context["status"]=["Center","inArea","response"]
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
