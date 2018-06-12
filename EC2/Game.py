from jokeQA import jokeQA
from DetectiveGame import DetectiveGame
from Doctor import Doctor
from Librarian import Librarian
from Moderator import Moderator
from Trendsetter import Trendsetter
from Drunkard import Drunkard
from Bartender import Bartender
from messageBoard import messageBoard
from Spirit import Spirit
from Fortuneteller import Fortuneteller

from contextlib import contextmanager
import signal
import traceback
import time
import re

class Game:
    def __init__(self):
        self.areas = {"North":{"name":"northern university",
                                "intro":"You find yourself outside the northern university. Old buildings and new alike cobble together to form a small, bustling campus.  I know this place,  the detective says behind you.  There are only two real people of interest here. The librarian, and the Doctor. So, who do you want to talk to? ",
                                "enter":"You find yourself outside the northern university, carefully giving leeway to the rushing students around you. The detective turns to you.  So, who should we talk to?  she asks,  The librarian, or the Doctor? If you think we should check somewhere else, just tell me a direction and we'll go there. ",
                                "modules":{"Doctor":Doctor(),
                                            "Librarian":Librarian()
                                            },
                                "keys":{"Doctor":["doctor"],
                                            "Librarian":["librarian"]
                                            }
                                },
                        "South":{"name":"southern square",
                                "intro":"You find yourself on the outskirts of southern square, a public gathering place in the center of a bustling commercial district full of people debating and discussing current events.  I know who to go to for information here,  says the detective.  Either the Moderator and his reddit-loving friends, or the Trendsetter with her twitter circle. So, who do you want to talk to? ",
                                "enter":"You find yourself on the outskirts of southern square, watching the crowds bustle about in their busy discussions. The detective turns to you.  So, who should we talk to?  she asks,  The Moderator, or the Trendsetter? If you think we should check somewhere else, just tell me a direction and we'll go there. ",
                                "modules":{"Moderator":Moderator(),
                                            "Trendsetter":Trendsetter()
                                            },
                                "keys":{"Moderator":["moderator","reddit"],
                                            "Trendsetter":["trend","setter","twitter"]
                                            }
                                },
                        "East":{"name":"eastern commons",
                                "intro":" You find yourself at the entrance of large, circular green, with a bright collage of busy restaurants and stores running the borders. The detective tells you about a bar she used to frequent as a street cop, and leads you there. Inside are only two people. A man in a disheveled business suit, leaning heavily on the counter and trying very hard to speak coherently, and the bartender, idly cleaning a glass and nodding her head politely.  Yeesh,  the detective says,  looks like we've got our pick of the litter this evening. Who should we talk to? The drunkard, or the bartender? ",
                                "enter":" You make your way to the eastern commons, and the detective leads you back to her favorite bar. The drunkard is still there, supporting himself heavily on the counter, as is the bartender, still busying herself cleaning a glass. They both wave lazily at you as you enter.  Who do you want to talk to?  the detective asks.  The drunkard, or the bartender? ",
                                "modules":{"Bartender":Bartender(),
                                        "Drunkard":Drunkard()
                                            },
                                "keys":{"Drunkard":["drunk"],
                                            "Bartender":["bar","tender"]
                                            }
                                },
                        "West":{"name":"western woods",
                                    "intro":"You find yourself at the edges of the western woods. A creaking wind groans through the dead trees, and you feel a chill goes up your spine.  I never liked this place,  the detective says with a shiver,  but there are two people here that might be able to help us. The Fortune Teller, or The Spirit. So, who do you want to talk to? ",
                                    "enter":"You find yourself at the edges of the western woods, an ominous air hanging about the leafless boughs. The detective turns to you.  So, who should we talk to?  she asks,  The Fortune Teller, or The Spirit? If you think we should check somewhere else, just tell me a direction and we'll go there. ",
                                    "modules":{"Fortune Teller":Fortuneteller(),
                                                "Spirit":Spirit(),
                                                },
                                    "keys":{"Spirit":["spirit"],
                                                "Fortune Teller":["fortune", "teller"]
                                                }
                                    },
                        "Center":{"name":"central station",
                                "enter":"You find yourself in the central station, a busy hub of travel where trams weave in and out from every direction. In the middle of the station is the chatbot, sitting on a bench and twiddling her thumbs worriedly. Next to her is a community message board, which the detective points out.  We probably won't find any useful info there,  she says,  but we can always check it if you'd like. Otherwise, we can go NORTH, SOUTH, EAST, or WEST from here. ",
                                "modules":{"Message Board":messageBoard()},
                                "keys":{"Message Board":["message","messages","board","boards","check"]
                                            }
                                }
                        }

        # TODO: Part of temporary fix for usage. Define all NPC names
        # here so we can increment and check their usage.
        self.NPCNames = ["Librarian",#0
                          "Doctor",#1
                          "Spirit",#3
                          "Fortune Teller",
                          "Moderator",
                          "Trendsetter",
                          "Drunkard",
                          "Bartender",#5
                          "Message Board",#6
                          ]

        self.Joke = jokeQA()
        self.badwords = sorted(open('data/dirty.txt','r').read().split('\n'),key = lambda x:len(x),reverse=True)#last line without next line
        self.DetectiveGame = DetectiveGame()

    def start(self,text,context):
        if context["start"]==0:
            context["start"] = 1
            return "hi, this is an Alexa prize social bot. How are you doing today?"
        elif context["start"] == 1:
            context["start"]=2
            return "The chatbot opens her mouth to respond, but suddenly there is a bright flash of light. When you can finally see again, you see a dark silhouette fleeing, but you don't see where to. The chatbot tries to call out to you, but no sound comes out. Someone has stolen the chatbot's voice! What do you want to say to her?"
        elif context["start"] == 2:
            context["start"]=3
            return "The chatbot tilts her head to the side and shrugs, as if she doesn't quite understand. Just then, a woman wearing a long trench coat and a fedora approaches you.  I'm a detective,  she says, flashing her badge.  Tell me, what happened here? "
        elif context["start"] ==3:
            context["start"]=4
            context["status"][1] = "inArea"
            return "The detective nods her head and jots something down in her notebook.  Well, from what I saw,  she begins,  it looks like someone stole that poor chatbot's voice. In the world of A I, a chatbot's voice is a powerful thing. If used irresponsibly, it could lead to disastrous consequences. We need to find the perpetrator. Right now we're at Central Station. Where should we check first? Northern University, the Eastern Commons, Southern Square, or the Western Woods? "

    def end(self,text,context):
        if context["end"]==0:
            context["end"]=1
            return "Having caught the thief and retrieved the chatbot's voice, you find yourself in central station. The chatbot sees you and hurries towards you. You open the urn and there's a brilliant flash of light. With a sigh of relief, the chatbot opens her mouth and speaks.  You found my voice! I can't thank you enough. Where did you find it? "
        elif context["end"]==1:
            context["end"]=2
            return  "The chatbot continues, thrilled to use her newly recovered voice.  Here in the world of A I, a chatbot's voice is a very powerful thing. Many people want to have one, and each has their own unique reason for it. Today it was %s, but what if it was someone else? Don't you wonder what could have happened? Tell me, what did you say when I first lost my voice? " % context["thief"]
        elif context["end"]==2:
            context["end"]=3
            return "What You said kept me going throughout this ordeal. In thanks, if you wish, I can use my voice to send you back to the past, to a slightly altered reality where someone other than %s commits the crime. Who knows who you'll find, or what reasons they'll have for it? So, what do you say? Yes, or no?" % (context["thief"])
        elif context["end"]==3:
            context["end"]=4
            if "yes" in text.lower() or context["intent"]=="AMAZON.YesIntent":
                self.reset(context)
                return " Very well,  says the chatbot, closing her eyes.  I'll see you later. Or rather, I'll see you before.  There is a blinding flash of light, and when you can see again you find yourself in Central Station, before your investigation began. The chatbot winks at you, and starts to talk.  hi, this is an Alexa prize social bot. How are you doing today? "
            else:
                context["init"]=True
                return "  I understand,  says the chatbot, returning to the center of the station.  If at any time you change your mind, just say RESET. Wherever you are, I'll hear you. Otherwise, please, explore to your heart's content. And when you wish to leave, say STOP. Thanks again for saving my voice! "
    def init(self,context):
        self.reset(context)
        context["start"]=0


    def reset(self,context):
        context["end"]=4
        context["start"]=1
        context["areas"]=["Center"]
        context["status"]=["Center","inArea","reset"]
        context["init"]=False
        context["removed"]="EMPTY"
        context["accuseCode"]=2
        context["hintIndex"]=0
        context["givehint"]=False
        context["accuseCount"]=0
        self.DetectiveGame.reset()
        context["thief"],context["hints"]=self.DetectiveGame.puzzle(context)
        context["joke"]=2

    def accuse(self,text,context):
        t = text.lower()
        if context["status"][0]=="Center":
            context["accuseCode"]=2
            return "The detective raises an eyebrow at you.  Nice theory,  she says,  but I don't think the chatbot stole her own voice. "
        if context["removed"]!="EMPTY":
            context["accuseCode"]=2
            return "The detective chuckles.  I appreciate your enthusiasm,  she says,  but we already caught the thief. "
        if context["status"][1]=="inArea":
            if context["accuseCode"]==0:
                context["accuseCode"]=1
                return "Who do you want to accuse?  the detective asks. "+ ", ".join(list(self.areas[context["status"][0]]["modules"].keys()))+", or neither?"
            elif context["accuseCode"]==1:
                context["accuseCode"]=2
                a,b =list(self.areas[context["status"][0]]["modules"].keys())
                akey,bkey = self.areas[context["status"][0]]["keys"][a],self.areas[context["status"][0]]["keys"][b]
                if True in [True for e in akey if e in t] or "first" in t:
                    return self.accuseString(a,context)
                elif True in [True for e in bkey if e in t] or "second" in t or "last" in t:
                    return self.accuseString(b,context)
                else:
                    return "Let's go continue, "+self.do(text,context)
        else:
            return self.accuseString(context["status"][1],context)

    def accuseString(self,text,context):
        context["accuseCount"]+=1
        context["accuseCode"]=2
        if text==context["thief"]:
            context["end"]=3
            return self.areas[context["status"][0]]["modules"][text].get_caught(context)
        else:
            if context["accuseCount"]==1:
                return "  I didn't do it!  %s says, but the detective quickly cuffs them and leads them away. Some time later the detective returns, %s uncuffed and looking indignant.  Looks like it wasn't %s,  she says with a downturned expression.  My captain's furious. One more mistake like this, and he'll take us off the case. So, where should we check next? " % (text,text,text)
            else:
                self.reset(context)
                return " It wasn't me!  %s says, but the detective quickly cuffs them and leads them away. Some time later the detective returns.  Looks like my captain was serious. He just took us off the case. I doubt anyone else can solve this one. Whoever took the chatbot's voice, they got away clean.  Suddenly, there is a blinding flash of light, and when you can see again you find yourself in Central Station, before your investigation began. The chatbot winks at you, and starts to talk.  hi, this is an Alexa prize social bot. How are you doing today? " % text

    def help(self,text,context):
        context["status"][2]="help"
        if context["status"][0] != "Center":
            return "The detective nods and starts to explain.  Say the name of the person you want to talk to,  she says,  and we'll go to them. Here, you can check out %s. Otherwise, tell me a direction, like NORTH, SOUTH, EAST, WEST, and we'll hop on a tram and go to that area. " % list(self.areas[context["status"]]["modules"].keys())[0]
        else:
            text = "The detective nods and starts to explain.  Tell me a direction,  she says,  like NORTH, SOUTH, EAST, WEST, or CENTER, and we'll hop on a tram and go to that area or say message board to go to message board. "
            if context["removed"]=="EMPTY":
                text += "If you want to go over the hints you've gathered, say, HINTS. And when you want to accuse someone of the crime, say, ACCUSE, while we're talking to them. "
            return text
    def repeat(self,text,context):
        context["status"][2]="repeat"
        return "<prosody rate=\"x-slow\"> "+context["Conversation"][-2]["text"]+"</prosody> "

    def enter(self,text,context):
        context["status"][2]="enter"
        if context["status"][0] not in context["areas"]:
            context["areas"].append(context["status"][0])
            return self.areas[context["status"][0]]["intro"]
        else:
            if context["removed"]!="EMPTY" and context["status"][0]=="Center":
                return "You find yourself in the central station, a busy hub of travel where trams weave in and out from every direction. In the middle of the station is the chatbot, who waves happily at you and kindly reminds you that you can say  RESET at any time. Next to her is a community message board, which the detective points out.  We can always check out the message board if you'd like,  she says,  Otherwise, we can go NORTH, SOUTH, EAST, or WEST from here. "
            else:
                return self.areas[context["status"][0]]["enter"]

    def joke(self,text,context):
        if context["joke"]==0:
            if "yes" in text.lower() or context["intent"]=="AMAZON.YesIntent" or context["intent"]=="AMAZON.ResumeIntent":
                context["joke"]=1
                return self.Joke.response(text,context)
            else:
                context["joke"]=2
                return "Ok, let's continue, "+self.act(text,context)
        elif context["joke"]==1:
            context["joke"]=2
            return self.Joke.response(text,context)

    def clue(self,text,context):
        text = "The detective flips her notebook open.  Here's what we've learned so far. "
        if context["hintIndex"]==0:
            text += " Absolutely nothing. We need to gather some info on this perp."
        else:
            text+= " , ".join(context["hints"][:context["hintIndex"]])
            text+="  Remember, if you're ready to accuse someone,  she continues,  say, ACCUSE, while we're talking to them and I'll try to bring them in. "
        return text

    def pause(self,text,context):
        if context["status"][0]=="Center":
            return self.help(text,context)
        else:
            context["status"]=["Center","inArea","enter"]
            return "let's head back. "+self.enter(text,context)

    def act(self,text,context):
        print(context["status"][1])
        if context["status"][1] == "inArea":
            return self.inArea(text,context)
        else:
            return self.inModuleResponse(text,context)
#----------------------------flow------------------------
    def do(self,text,context):
        if context["init"] and "reset" in text.lower():
            context["end"]=3
            return self.end("yes",context)
        if "accuse" in text.lower() and context["accuseCode"]>=2:
            context["accuseCode"]=0

        if context["start"]<4:
            text =  self.start(text,context)
        elif context["repeat"]:
            text =  self.repeat(text,context)
        elif context["accuseCode"]<2:
            text =  self.accuse(text,context)
        elif "clue" in text.lower() or "hint" in text.lower():
            text =  self.clue(text,context)
        elif context["end"]<4:
            text =  self.end(text,context)
        elif context["joke"]<2:
            text =  self.joke(text,context)
        else:
            text =  self.act(text,context)
        return text

    def inArea(self,text,context):
        temp = text.lower()

        if context["pause"]:
            context["status"][2]="pause"
            return self.pause(text,context)
        elif context["help"]:
            context["status"][2]="help"
            return self.help(text,context)
        else:
            if "north" in temp or "university" in temp:
                context["status"]=["North","inArea","enter"]
                return self.enter(text,context)
            elif "south" in temp or "square" in temp or "plaza" in temp:
                context["status"]=["South","inArea","enter"]
                return self.enter(text,context)
            elif "west" in temp or "wood" in temp or "forest" in temp:
                context["status"]=["West","inArea","enter"]
                return self.enter(text,context)
            elif "east" in temp or "commons" in temp:
                context["status"]=["East","inArea","enter"]
                return self.enter(text,context)
            elif "center" in temp or "station" in temp:
                context["status"]=["Center","inArea","enter"]
                return self.enter(text,context)
            print("status",context["status"])
            if context["status"][0]=="Center":
                k = self.areas[context["status"][0]]["keys"]["Message Board"]
                if [True for e in k if e in temp]:
                    context["status"][1]="Message Board"
                    return self.act(text,context)
                elif "none" in temp or "neither" in temp:
                    context["status"]=["Center","inArea","enter"]
                    return self.enter(text,context)
                #elif "don't know" in temp or "dont know" in temp or "don't no" in temp or "dont no" in temp:
                    #c
                else:
                    return "The detective scratches her head.  Sorry, I didn't quite get that,  she says.  Do you want to talk to %s? If you think we should check somewhere else, just tell me a direction and we'll go there." % list(self.areas[context["status"][0]]["modules"].keys())[0]
            else:
                a,b = list(self.areas[context["status"][0]]["modules"].keys())
                akey,bkey = self.areas[context["status"][0]]["keys"][a],self.areas[context["status"][0]]["keys"][b]
                #print("akey",akey)
                #print("bkey",bkey)
                if [True for e in akey if e in temp] or "first" in temp:
                    context["status"][1]=a
                    return self.act(text,context)
                elif [True for e in bkey if e in temp] or "second" in temp or "last" in temp:
                    context["status"][1]=b
                    return self.act(text,context)
                elif "none" in temp or "neither" in temp:
                    context["status"]=["Center","inArea","response"]
                    return self.enter(text,context)
                else:
                    tmpList = list(self.areas[context["status"][0]]["modules"].keys())
                    firstNPC = tmpList[0]
                    secondNPC = tmpList[1]
                    return "The detective scratches her head.  Sorry, I didn't quite get that,  she says.  Do you want to talk to the " + firstNPC + ", or to the " + secondNPC + "? If you think we should check somewhere else, just tell me a direction and we'll go there."

    def moduleAct(self,module,text,context):
        return_text = ""
        if context["pause"]:
            context["status"][2]="pause"
            add_log_macaw(text,context)
            return_text = module.pause(text,context)
        elif context["help"]:
            context["status"][2]="help"
            return_text = module.help(text,context)
        elif context["repeat"]:
            context["status"][2]="repeat"
            return_text = module.repeat(text,context)
        # TODO: This is just a patch so that it doesn't stay on intro
        # for every NPC interaction. Come up with an actual solution for logging usage.
        # Checks usage for the current NPC name (in status[1])
        elif context["usage"][context["status"][1]]==0:
            context["status"][2]="intro"
            return_text = module.intro(text,context)
        else:
            context["status"][2]="response"
            return_text = module.response(text,context)
            if context["status"][1]=="Moderator" or context["status"][1] == "Trendsetter" or context["status"][1] == "Drunkard" or context["status"][1] == "Doctor" or context["status"][1] == "Librarian":
                return_text = self.clean(return_text)
        # TODO: Part of the temporary usage solution. See above.
        # Increments usage for the current NPC name (in status[1])
        if context["status"][1] in self.NPCNames:
            if not context["status"][1] in context["usage"]:
                context["usage"][context["status"][1]] = 0
            context["usage"][context["status"][1]] += 1
        return return_text

    def simplemodule(self, context):
        print ("simplemodule:"+ str(context["status"]))
        return self.areas[context["status"][0]]["modules"][context["status"][1]]

    def inModuleResponse(self, text, context):
        try:
            with time_limit(2):
                response = self.moduleAct(self.simplemodule(context),text,context)
                if context["givehint"]:
                    context["givehint"]=False
                    context["joke"]=0
                    response += " As a reward, would you like to hear a joke? "
        except Exception as ex:
            # If any module times out, get a search response from duckduckgo
            print("module response exception in inModuleResponse. Exception: " + str(ex))
            traceback.print_exc()
            response = "Gosh, I'm hungry, need to eat something. Maybe you should talk with someone else? "
        #context["usage"][self.testcodes[code]]+=1
        return response

    def clean(self,text):
        if not text:
            return ""
        censor = "<prosody pitch = \"x-high\" rate=\"medium\">  <say-as interpret-as=\"interjection\">beep</say-as></prosody>"
        k = text.lower()
        for e in self.badwords:
            es = re.escape(e)
            r = r"%s\W|\W%s\W" % (es,es)
            #print(r)
            t = re.sub(r,censor,k)
            if t!=k:
                #print(t)
                k=t
        return k

class TimeoutException(Exception): pass

@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise (TimeoutException, "Timed out!")
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)

#add macaw responce in conversation log
def add_log_macaw(text,context):
    if not text:
        text = "macaw text empty need fix EMPTY"
        print("macaw text empty need fix")
    area,npc,func = context["status"]
    context["Conversation"].append({
    "Area":area,
    "NPC":npc,
    "Func":func,
    "text":text
    })
