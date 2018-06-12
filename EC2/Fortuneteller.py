import horoscope
from nltk.util import ngrams

class Fortuneteller:
    def __init__(self):
        self.yeswords = open('data/yes.txt', 'r').read().split('\n')
        self.nowords = open('data/no.txt', 'r').read().split('\n')
        self.horoscope = horoscope.horoscope()

    def intro(self,text,context):
        if "Fortuneteller" not in context:
            context["Fortuneteller"] = {}
            context["Fortuneteller"]["status"] = 0
            context["Fortuneteller"]["intro"] = False
            context["Fortuneteller"]["start"] = False
            return "You make your way to a small clearing in the forest. In the middle is a small old woman with long, "\
                   "black hair. Hello there, young one. She says with a grin, I saw your coming. You want to know about "\
                   "the chatbot's voice, hmm? Well, allow this old woman to tell your fortune, and I'll tell you all I "\
                   "know about it. Does that sound good? Yes,or no? "

           
    def response(self,text,context):

        if context["Fortuneteller"]["intro"] == True:
            context["Fortuneteller"]["intro"] = False
            context["Fortuneteller"]["start"] = False
            if context["Fortuneteller"]["status"] == 1:
                return "You find your way back to the fortune teller's clearing. She smiles and invites you over. Hello "\
                       "again, young one, she says, still grinning. Allow this old woman to tell your fortune, and I'll "\
                       "tell you all I know about the chatbot's voice. Does that sound good? Yes, or no? "

            elif context["Fortuneteller"]["status"] == 2:
                return "You find your way back to the fortune teller's clearing. She smiles and invites you over. I've " \
                       "already told you all I know, she says, surprised, did you come here to hear your fortune again. "\
                       "Yes, or no? "



        if context["Fortuneteller"]["start"] == True:
            response, completion = self.horoscope.response(text,context)
            if completion == True:
                context["status"] = ["Center", "inArea", "response"]
                context["Fortuneteller"]["start"] = False
                context["Fortuneteller"]["intro"] = True
                context["Fortuneteller"]["status"] = 2

                if context["hintIndex"] < len(context["hints"]):
                    context["hintIndex"] += 1
                    tmpindex = context["hintIndex"]
                else:
                    tmpindex = len(context["hints"])-1

                hintStr = context["hints"][tmpindex]
                response += "The fortune teller laughs creakily, a huge grin on her face. Thank you for humoring an old "\
                            "woman, she says. Here's what I've seen about the chatbot's voice. "\
                            +hintStr+\
                            "The detective quickly jots it down in her notebook, then hurries you back to Central " \
                            "Station. You handled that old woman well, she says. "
                context["givehint"] = True

            return response

        else:
            if self.yes_representation(text, context):
                if context["Fortuneteller"]["status"] == 0:
                    context["Fortuneteller"]["status"] = 1
                context["Fortuneteller"]["start"] = True
                return "I knew you'd say that, the fortune teller says with a smile " + self.horoscope.intro(text, context)

            elif self.no_representation(text,context):
                context["status"] = ["Center", "inArea", "response"]
                return "I see, she says, a bit disappointed. If you change your mind, I'll still be here. With that, you " \
                       "take your leave. You find yourself back at the edge of the western woods. The detective turns to " \
                       "you. So, who should we talk to? she asks, The Fortune Teller, or The Spirit? If you think we should" \
                       " check somewhere else, just tell me a direction and we'll go there. "

            else:
                return "The fortune teller shakily cups her ear with a hand. I'm sorry dearie, she says, but I'm afraid I " \
                       "didn't quite get that. Yes, you wish to hear your fortune, or no, you do not? "



    def help(self, text, context):
        if context["Fortuneteller"]["start"] == True:
            return self.horoscope.help(text, context)
        else:
            text = "Huh. I think she just wants to read your fortune, the detective whispers. Tell her either yes or no. "
        if (context["hintIndex"]>=2):
            text += "By the way, the detective continues, if you want me to read you the hints you've gathered, say, " \
                   "HINT. And if you want to accuse The Fortune Teller, just say, ACCUSE. "
        
        return text


    def get_caught(self,context):
        context["removed"] = "Fortuneteller"
        context["status"] = ["Center","inArea","response"]
        context["end"] = 0
        return "The detective reaches under the fortune teller's rickety table and pulls out a small urn. Somehow, you " \
               "know the chatbot's voice is in there. The old woman chuckles, and lets the detective cuff her. I see " \
               "you've found it, she says, a quaver in her voice. With that voice, I could have called far into the past" \
               " and the future. I could have seen anything, and predicted everything! But before she can say more, the" \
               " detective leads her off in handcuffs. Nice work, she says, you caught the thief! Any last words for her? "



    def pause(self, text, context):
        context["status"] = ["West","inArea","response"]
        context["Fortuneteller"]["intro"] = True
        return "I see, she says, a bit disappointed. If you change your mind, I'll still be here. With that, you take " \
               "your leave. You find yourself back at the edge of the western woods. The detective turns to you. So, " \
               "who should we talk to? she asks, The Fortune Teller, or The Spirit? If you think we should check " \
               "somewhere else, just tell me a direction and we'll go there. "



    def repeat(self, text, context):
        return context["conversation"][-2]["text"]



    def no_representation(self, text, context):
        text = text.lower()
        if (text == "how are you"):
            if (context["intent"] == "AMAZON.NoIntent"):
                return True
            else:
                return False
        if True in [tuple(b.lower().split()) in list(ngrams(text.lower().split(), len(b.lower().split()))) for b
                    in self.nowords]:
            return True
        return False

    def yes_representation(self, text, context):
        text = text.lower()
        if (text == "how are you"):
            if (context["intent"] == "AMAZON.YesIntent"):
                return True
            else:
                return False
        if True in [tuple(b.lower().split()) in list(ngrams(text.lower().split(), len(b.lower().split()))) for b
                    in self.yeswords]:
            return True
        return False
