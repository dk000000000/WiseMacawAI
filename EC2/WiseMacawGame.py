from Game import Game
import time
import random
import os
import signal
import traceback
from contextlib import contextmanager
import re
import json
from intentDetect import intentDetect
import redisClient

class WiseMacawGame:
    def __init__(self, Table="GameMacawLOG"):
        self.SessionData = {}
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
        self.Game = Game()

        self.deflecting = open('data/deflect.txt','r').read().split('\n')#last line without next line
        self.LogTable = redisClient.redisClient("log")
        self.IntentDetector = intentDetect()

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
                                                "status":["Center","intro","start"],
                                                "start":0,
                                                "areas":[],
                                                "intent":"Launch",
                                                "ConversationID":"EMPTY",
                                                "usage":{tcode:0 for tcode in self.NPCNames},
                                                "credit":0,
                                                "pause":False,
                                                "help":False,
                                                "repeat":False,
                                                }
        self.Game.init(self.SessionData[str(Session["sessionId"])])


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
        print("thief",context["thief"])
        response = self.changeIntent(context, user_input,Request)

        # Log inputs
        print("before response status: "+str(context["status"]))
        add_log_user(Request,user_input,context)
        print("intent: ",context["intent"])
        if not response:
            response = self.Game.do(user_input,context)
        print("after response status: "+str(context["status"]))
        add_log_macaw(response,context)

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
                with open("GameSession%s.json" % ID,"w") as f:
                    f.write(json.dumps(CurrentEndSession))
                    print("Gamesession %s write to Session%s.json" % (ID,ID))
                #print(e)
                print("Logging failed")
                print('SessionID',ID)
                print('UserID',CurrentEndSession["UserID"])
                print('ConversationID',ConversationID)
                print('sessionAttributes',CurrentEndSession["Conversation"])
        else:
            print("SessionID "+str(ID) +" lost, ERROR")

    # Determines intent from user input and returns detected intent name.
    # Returns empty string if no intents are found.
    def changeIntent(self, context, user_input,Request):
        response = None
        context["intent"]=self.IntentDetector.detect_intent(user_input, context,Request)
        if context["intent"]=="ID" and context["status"][1]!="inArea":
            response = "Sorry, that I do not know. "
        return response
        '''
        if "intent" in Request:
            print("original intent ",Request["intent"]["name"])
        # DEBUG: Do not detect intents again if the default text is given...
        if not user_input == "how are you":
            detected_intent = self.IntentDetector.detect_intent(user_input, context)
            if not detected_intent == "":
                if not "intent" in Request:
                    Request["intent"] = {}
                Request["intent"]["name"] = detected_intent
        '''

        #self badwords have to sorted from long to short

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
