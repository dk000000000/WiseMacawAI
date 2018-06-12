from start import start
from chitchat import chitchat
from easyQA import easyQA
from jokeQA import jokeQA
from wordGame import wordGame
from textAdventure import textAdventure
from ghostAdventure import ghostAdventure
from aimlbot import aimlbot
from search import search
from board import board
from riddle import riddle
from reddit_news import reddit_news
from horoscope import horoscope
from twitter_news import twitter_news
from twitter_menu import twitter_menu

from flowControler import flowControler
from intentDetectMenu import intentDetectMenu

import time
import random
import os
import signal
import traceback
from contextlib import contextmanager
import re
import json
import redisClient

class WiseMacawMenu:
    def __init__(self):
        self.SessionData = {}

        self.modules = [wordGame(),
                        reddit_news(),
                        twitter_news(),
                        twitter_menu(),
                        easyQA(),
                        jokeQA(),
                        chitchat(),
                        aimlbot(),
                        textAdventure(),
                        ghostAdventure(),
                        horoscope(),
                        riddle(),
                        board(),
                        search(),
                        start()
                        ]

        # TODO: Part of temporary fix for usage. Define all NPC names
        # here so we can increment and check their usage.
        self.moduleNames = ["word game",
                            "reddit news",
                            "twitter news",
                            "twitter trend",
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

        self.badwords = sorted(open('data/dirty.txt','r').read().split('\n'),key = lambda x:len(x),reverse=True)
        self.deflecting = open('data/deflect.txt','r').read().split('\n')#last line without next line
        self.LogTable = redisClient.redisClient("menuLog")
        self.flowControler = flowControler()
        self.IntentDetector = intentDetectMenu()

    def Handle_Session(self,data):
        Session = data["session"]
        Request = data["request"]
        #if session new call NewSession
        if ("intent" in Request and Request["intent"]["name"]=="AMAZON.StopIntent") or Request["type"]=="SessionEndedRequest" or "stop" in self.userInput(Request,None):
            return self.EndSession(Session,Request)
        else:#other call InSession
            return self.InSession(Session,Request)

    def initSession(self,Session):
        self.SessionData[str(Session["sessionId"])]={"UserID":Session["user"]["userId"],
                                                "Conversation":[],
                                                "intent":"Launch",
                                                "ConversationID":"EMPTY",
                                                "flow":[self.moduleNames.index("startModule"),1],
                                                "usage":{tcode:0 for tcode in self.moduleNames},
                                                "hold":False,
                                                "credit":0,
                                                "pause":False,
                                                "help":False,
                                                "repeat":False,
                                                "randomAssign":False,
                                                "no_intro":False
                                                }


    def InSession(self,Session,Request):
        #s = time.time()
        sessionId = str(Session["sessionId"])
        if Session["new"] or sessionId not in self.SessionData:
            self.initSession(Session)
            print("Start Session",str(Session["sessionId"]))
        print ("==================At start of InSession.=================")
        try:
            print("sessionId",str(Session["sessionId"]))
            context = self.SessionData[sessionId]
        except:
            #print(e)
            traceback.print_exc()
            print("InSession context exception")
            #print(self.SessionData)
            self.initSession(Session)
            context = self.SessionData[sessionId]
        try:
            if "intent" in Request:
                context["intent"] = Request["intent"]["name"]
            else:
                context["intent"] = Request["type"]
        except Exception as e:
            traceback.print_exc()
            print("insession intent exception")
            print(e)
            print(Request)
            context["intent"] = "ERROR"
        except:
            traceback.print_exc()
            print("insession intent exception")
            #print(self.SessionData)
            context["intent"] = "ERROR"

        # Get user input
        user_input = self.userInput(Request,context)
        print("userInput",user_input)
        response = self.changeIntent(Request,context, user_input)

        # Log inputs
        #print("before response status: "+str(context["status"]))
        add_log_user(Request,user_input,context)

        response,flag = self.flowControler.flowChange(Request,context,user_input)
        code, turns = context["flow"]

        print("flow",self.moduleNames[context["flow"][0]],context["flow"][1])
        print("hold",context["hold"])
        if "intent" in Request:
            print("intent",Request["intent"]["name"])
        # First, check the flag. If it is true, then that means the input was a command
        # which the bot cannot perform. Response currently holds whatever response was set by flowChange.
        # Use whatever response text was set by flowChange.
        if not flag:
            if response == None or response == "":
                response = self.clean(self.inModuleResponse(Request, context, user_input, code))
            else:
                response += " . " + self.clean(self.inModuleResponse(Request, context, user_input, code))

        print("flowAfter response",self.moduleNames[context["flow"][0]],context["flow"][1])
        add_log_macaw(0,1,code,response,context)
        #print("low macaw",time.time()-s)


        response=self.flowControler.AssignFlow(context,response)
        print("flowAfter AssignFlow",self.moduleNames[context["flow"][0]],context["flow"][1])

        context["credit"]+=1
        # Reset all universal intent flags
        context["pause"]=False
        context["help"]=False
        context["repeat"]=False

        print ("final Response: " + response)
        print ("==================At end of InSession.=================")
        print()
        #print("assign low",time.time()-s)
        return build_response({},build_ssml_response(response,False))

    def EndSession(self,Session,Request):
        try:
            print("End Session",str(Session["sessionId"]))
            context = self.SessionData[str(Session["sessionId"])]
            user_input = self.userInput(Request,context)
            add_log_user(Request,user_input,context)
            response = "#END#"
            add_log_macaw(response,context)
            self.LogSession(str(Session["sessionId"]),Request["timestamp"],context["ConversationID"],context["usage"])
            print()
        except:
            traceback.print_exc()
            print("end SEssion exception")
        return build_response({},build_speechlet_response(None,True))

    def LogSession(self,ID,Time,ConversationID,usage):
        if ID in self.SessionData:
            CurrentEndSession = self.SessionData.pop(ID)
            try:
                Item = {
                    'SessionEndTime':Time,
                    'SessionID':ID,
                    'UserID':CurrentEndSession["UserID"],
                    'ConversationID':ConversationID,
                    'Conversation':CurrentEndSession["Conversation"],
                    'usage':usage
                }
                self.LogTable.putData("sessionData",str(ID)+" "+str(Time),json.dumps(Item))
            except Exception as e:
                traceback.print_exc()
                with open("MenuSession%s.json" % ID,"w") as f:
                    f.write(json.dumps(CurrentEndSession))
                    print("Menusession %s write to Session%s.json" % (ID,ID))
                #print(e)
                print("Logging failed")
                print('SessionID',ID)
                print('UserID',CurrentEndSession["UserID"])
                print('ConversationID',ConversationID)
                print('sessionAttributes',CurrentEndSession["Conversation"])
        else:
            print("SessionID "+str(ID) +" lost, ERROR")

    def changeIntent(self, Request, context, user_input):
        #if "intent" in Request:
            #print("original intent ",Request["intent"]["name"])
        # DEBUG: Do not detect intents again if the default text is given...
        if not user_input == "how are you":
            detected_intent = self.IntentDetector.detect_intent(user_input, context)
            if not detected_intent == "":
                if not "intent" in Request:
                    Request["intent"] = {}
                Request["intent"]["name"] = detected_intent

    def moduleAct(self,moduleCode,text,context):
        if context["pause"]:
            return "Alright, let's do something else. " + self.modules[moduleCode].pause(text,context)
        elif context["help"]:
            return "need help? "+self.modules[moduleCode].help(text,context)
        elif context["repeat"]:
            return "Let me say that again, "+self.modules[moduleCode].repeat(text,context)
        elif context["usage"][self.moduleNames[moduleCode]]==0 and context["no_intro"] == False:
            return self.modules[moduleCode].intro(text,context)
        else:
            if moduleCode in self.getcodes(["riddle game","word game","text adventure","ghost adventure","horoscope"]):
                return self.modules[moduleCode].response(text,context)[0]
            else:
                return self.modules[moduleCode].response(text,context)

    # Corresponds to the IN_MODULE state.
    # Retrieves a context["flow"] from a module.
    def inModuleResponse(self, Request, context, user_input, code):
        try:
            with time_limit(2):
                # For QA and chitchat, go through templated responses first.
                if (code == self.moduleNames.index("chitchat")
                    or code == self.moduleNames.index("ask question")):
                    # Try templated response first
                    response = self.moduleAct(self.moduleNames.index("chat"), user_input, context)
                    # If there is no templated response, get the response for QA
                    if not response or (response == "" or response == " "):
                        try:
                            response = self.moduleAct(self.moduleNames.index("ask question"), user_input, context)
                            code = self.moduleNames.index("ask question")
                        # If there is no QA response, get the response for chitchat
                        except Exception as ex:
                            traceback.print_exc()
                            print ("No templated response or ask question response. Returning chitchat response. Exception: " + str(ex))
                            response = self.moduleAct(self.moduleNames.index("chitchat"), user_input, context)
                            code = self.moduleNames.index("chitchat")
                    else:
                        code = self.moduleNames.index("chat")
                # For templated response, go to chitchat if it fails.
                elif (code == self.moduleNames.index("chat")):
                    # Try templated response first
                    response = self.moduleAct(self.moduleNames.index("chat"), user_input, context)
                    print ("Templated response: " + response)
                    # If there is no templated response, get the response for chitchat.
                    if not response or (response == "" or response == " "):
                        print ("No templated response. Returning chitchat response.")
                        response = self.moduleAct(self.moduleNames.index("chitchat"), user_input, context)
                        code = self.moduleNames.index("chitchat")
                else:
                    response = self.moduleAct(code,user_input,context)
        except Exception as ex:
            # If any module times out, get a search response from duckduckgo
            print("module response exception in inModuleResponse. Exception: " + str(ex))
            traceback.print_exc()
            try:
                with time_limit(1):
                    response = self.moduleAct(self.moduleNames.index("search"),user_input,context)
                    code = self.moduleNames.index("search")
            except:
                traceback.print_exc()
                response = "Sorry, your question was harder than I thought. Maybe ask something else?"
                print("Search result response exception")
        if context["flow"][0]!=code:
            self.flowControler.changeflow(self.moduleNames[code],context)
        context["usage"][self.moduleNames[code]]+=1
        return response


        #self badwords have to sorted from long to short
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
    def getcodes(self,codenames):
        return [self.moduleNames.index(name) for name in codenames]
#self badwords have to sorted from long to short
    def IsNotClean(self,text):
        if not text:
            return False
        k = " "+text.lower()+" "#THIS IS BECAUSE ASR WILL ALWAYS HAVE SPACE BETWEEN THEM
        for e in self.badwords:
            if " "+e+" " in k:
                return True
        return False

    def userInput(self,request,context):
      text = ""
      if "intent" in request:
          #IF EMPTY SLOTS
          try:
              if "speechRecognition" in request and "hypotheses" in request["speechRecognition"] and request["speechRecognition"]["hypotheses"]:
                  #print(request["speechRecognition"])
                  h = request["speechRecognition"]["hypotheses"][0]["tokens"]
                  for i in range(len(h)):
                      if i!=0:
                          text +=" "
                      text +=h[i]["value"]
              else:
                  if "slots" not in request["intent"] or not request["intent"]["slots"]:
                      text = "how are you"
                  else:
                      if len(request["intent"]["slots"])==2:
                          if "assertiveWords" in request["intent"]["slots"]:
                              text += request["intent"]["slots"]["assertiveWords"]["value"]
                          elif "newsWords" in request["intent"]["slots"]:
                              text += request["intent"]["slots"]["newsWords"]["value"]
                          elif "InterestWords" in request["intent"]["slots"]:
                              text += request["intent"]["slots"]["InterestWords"]["value"]
                          text +=" "+request["intent"]["slots"]["RawText"]["value"]
                      else:
                          if "SmallTalkWords" in request["intent"]["slots"]:
                            text = request["intent"]["slots"]["SmallTalkWords"]["value"]
                          else:
                            text = request["intent"]["slots"]["RawText"]["value"]
          except:
              traceback.print_exc()
              print("exception in userInput")
              text = "ping"
              #print(request)
      else:
          text = "hi"
      return text

#--------------- Helpers that build all of the responses ----------------------
def build_speechlet_response(output, should_end_session):
  return {
      'outputSpeech': {
          'type': 'PlainText',
          'text': output
      },
      'reprompt': {
          'outputSpeech': {
              'type': 'PlainText',
              'text': output
          }
      },
      'shouldEndSession': should_end_session
  }

def build_ssml_response(output, should_end_session):
    return {
    'outputSpeech': {
        'type': 'SSML',
        'ssml': "<speak>" +output+"</speak>"
    },
    'reprompt': {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': "<speak>" +output+"</speak>"
        }
    },
    'shouldEndSession': should_end_session

    }


def build_response(session_attributes, speechlet_response):
  return {
      'version': '1.0',
      'sessionAttributes': session_attributes,
      'response': speechlet_response
  }
# --------------- Helpers that build all session logs ----------------------
#add macaw responce in conversation log
def add_log_macaw(macawStatus,voice,functionality,text,session_attributes):
    if not text:
        text = "macaw text empty need fix EMPTY"
        print("macaw text empty need fix")
    session_attributes["Conversation"].append({
    "MacawStatus":macawStatus,
    "voice":voice,
    "functionality":functionality,
    "text":text
    })

#add user input in conversation log
def add_log_user(request,inputs,session_attributes):
  intent = ""
  text = inputs
  if "intent" in request:
      #IF EMPTY SLOTS
      intent = request["intent"]["name"]
          #print(request)
  else:
      intent = request["type"]
      text = "Text Not Available"
  if not intent:
      intent =  "user intent empty need fix EMPTY"
      print("user intent empty need fix")
  if not text:
      text = "user text empty need fix EMPTY"
      print("user text empty need fix")

  session_attributes["Conversation"].append(
      {
    "Userintent":intent,
    "text":text
    })

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
