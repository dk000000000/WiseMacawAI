from module import module
import redisClient
import random
import searchGame
from nltk.util import ngrams
import re

class ghostAdventure(module):
    def __init__(self):
        super().__init__()
        self.badwords = sorted(open('data/dirty.txt','r').read().split('\n'),key = lambda x:len(x),reverse=True)
        self.redis_ga = redisClient.redisClient("ghostAdventure")

    def intro(self,text,context):
        game = searchGame.searchGame()
        context["ghost adventure"] = []
        context["ghost adventure"].append(False)#0_continue/restart game due to interruption
        context["ghost adventure"].append(2)#1_tutorial(0: init; 1: in tutorial; 2:no tutorial)
        context["ghost adventure"].append(game)#2_game obj
        context["ghost adventure"].append(False)#3_game need restart due to finsh/death
        context["ghost adventure"].append(0)#4_number of round alive
        context["ghost adventure"].append(False)#5_DEBUG_mode(not enabled right now)
        context["ghost adventure"].append(0)#6_count for wrong inputs
        context["ghost adventure"].append(False)#7_comment trigger
        response = "Let's play a ghost adventure game . Say back to exit game <break time=\"700ms\"/> "\
                    "You are awkened by some noises , catch the intruder before 7 AM . "\
                    "You wake up by the noise inside the " + context["ghost adventure"][2].self_get_Pos() + " , you may "\
                    "say hide to find available hiding spots able to be checked , or say door , "\
                    "to find out which door leads to which room . You don't know what is behind each door"

        return response

    def response(self,userInput,context):
        response = ""
        AMAZON_yes = ["AMAZON.ResumeIntent","AMAZON.YesIntent"]
        AMAZON_no = ["AMAZON.NoIntent"]

        selfPos = context["ghost adventure"][2].self_get_Pos()
        ghostPos = context["ghost adventure"][2].ghost_get_Pos()

        if context["ghost adventure"][1] == 0:
            if self.matchingInput(userInput,"restart") or self.matchingInput(userInput,"start") or context["intent"] in AMAZON_yes or \
                self.matchingInput(userInput,"night") or self.matchingInput(userInput,"real") or self.matchingInput(userInput,"skip") or self.matchingInput(userInput,"game"):
                context["ghost adventure"][1] = 2
                context["ghost adventure"][2].init_pos()
                context["ghost adventure"][4] = 0
                selfPos = context["ghost adventure"][2].self_get_Pos()
                response = "You are awkened by some noises , catch the intruder before 7 AM . "\
                            "You wake up by the noise inside the " + selfPos + " , you may "\
                            "say hide to find available hiding spots able to be checked , or say door , "\
                            "to find out which door leads to which room . You don't know what is behind each door"
            else:
                context["status"]=["West","inArea","response"]
                response += "Return when you wish to try again, says the spirit, before its voice fades into the "\
                "darkness around you. You find yourself back at the edge of the western woods. The detective turns "\
                "to you. So, who should we talk to? she asks, The Fortune Teller, or The Spirit? If you think we "\
                "should check somewhere else, just tell me a direction and we'll go there."
            return response,0

        if context["ghost adventure"][0] == True: #been interrupted by other modules(continue or restart)
            context["ghost adventure"][0] = False
            if self.matchingInput(userInput,"restart") or self.matchingInput(userInput,"start") or self.matchingInput(userInput,"again"):#restart game

                context["ghost adventure"][2].init_pos()
                context["ghost adventure"][3] = False
                context["ghost adventure"][4] = 0
                selfPos = context["ghost adventure"][2].self_get_Pos()
                ghostPos = context["ghost adventure"][2].ghost_get_Pos()
                response = "Let's play the game again , wish you good luck on slaying the intruder . Remember , say back to exit game <break time=\"700ms\"/> "\
						"You wake up inside the " + selfPos + " , you may say hide , to find available hiding spots able to be checked , "\
                        "or say door , to find out which door leads to which room"
            elif self.matchingInput(userInput,"keep") or context["intent"] in AMAZON_yes:#continue game
                selfPos = context["ghost adventure"][2].self_get_Pos()
                ghostPos = context["ghost adventure"][2].ghost_get_Pos()
            else:
                context["status"]=["West","inArea","response"]
                response += "Return when you wish to try again, says the spirit, before its voice fades into the "\
                "darkness around you. You find yourself back at the edge of the western woods. The detective turns "\
                "to you. So, who should we talk to? she asks, The Fortune Teller, or The Spirit? If you think we "\
                "should check somewhere else, just tell me a direction and we'll go there."
            return response,0

        if context["ghost adventure"][7] == True and (context["intent"] in AMAZON_no or self.matchingInput(userInput,"no")):
            context["ghost adventure"][7] = False
            context["ghost adventure"][3] = True
            return "That's a pity. Well. ",4
        elif context["ghost adventure"][7] == True:
            context["ghost adventure"][7] = False
            context["ghost adventure"][3] = True
            if self.addMessage(userInput,selfPos) is True:
                return "Your message is recorded. ",4
            else:
                return "Sorry, this message violates Amazon guidelines. ",4

        if context["ghost adventure"][3] == True and (self.matchingInput(userInput,"restart") or self.matchingInput(userInput,"start") or self.matchingInput(userInput,"add") \
                or self.matchingInput(userInput,"ghost adventure") or self.matchingInput(userInput,"again") or context["intent"] in AMAZON_yes):#restart game
            context["ghost adventure"][3] = False
            context["ghost adventure"][2].init_pos()
            context["ghost adventure"][4] = 0

            selfPos = context["ghost adventure"][2].self_get_Pos()
            ghostPos = context["ghost adventure"][2].ghost_get_Pos()
            response = "Let's play the game again , wish you good luck on this time . Remember , say back to exit game <break time=\"700ms\"/> "\
						"You wake up inside the " + selfPos + " , you may say hide , to find available hiding spots able to be checked , "\
                        "or say door , to find out which door leads to which room"
            return response,0
        elif context["ghost adventure"][3] == True:
            context["status"]=["West","inArea","response"]
            response += "Return when you wish to try again, says the spirit, before its voice fades into the "\
                "darkness around you. You find yourself back at the edge of the western woods. The detective turns "\
                "to you. So, who should we talk to? she asks, The Fortune Teller, or The Spirit? If you think we "\
                "should check somewhere else, just tell me a direction and we'll go there."
            context["ghost adventure"][3] = False
            context["ghost adventure"][2].init_pos()
            context["ghost adventure"][4] = 0
            return response,0

        speech_output = ""
        doorOrHideout,choice = context["ghost adventure"][2].ghost_get_ghostAction()

        if self.matchingInput(userInput,context["ghost adventure"][2].get_hideout(selfPos)[0],1):#hideout 1
            situation,speech_output = context["ghost adventure"][2].situation_feedback("hide",context["ghost adventure"][2].get_hideout(selfPos)[0],doorOrHideout,choice)
        elif self.matchingInput(userInput,context["ghost adventure"][2].get_hideout(selfPos)[1],1):#hideout 2
            situation,speech_output = context["ghost adventure"][2].situation_feedback("hide",context["ghost adventure"][2].get_hideout(selfPos)[1],doorOrHideout,choice)
        elif self.matchingInput(userInput,context["ghost adventure"][2].get_hideout(selfPos)[2],1):#hideout 3
            situation,speech_output = context["ghost adventure"][2].situation_feedback("hide",context["ghost adventure"][2].get_hideout(selfPos)[2],doorOrHideout,choice)
        elif self.matchingInput(userInput,"left") and context["ghost adventure"][2].self_door_lastTime == "":#door "left" - 1st round
            situation,speech_output = context["ghost adventure"][2].situation_feedback("door",context["ghost adventure"][2].get_connection(selfPos)[0],doorOrHideout,choice)
        elif self.matchingInput(userInput,"left") and context["ghost adventure"][2].self_door_lastTime != "" and context["ghost adventure"][2].get_connection(selfPos)[2] != "none":#door "left" & previous door
            tmpList = list(context["ghost adventure"][2].get_connection(selfPos))
            tmpList.remove(context["ghost adventure"][2].self_door_lastTime)
            situation,speech_output = context["ghost adventure"][2].situation_feedback("door",tmpList[0],doorOrHideout,choice)
        elif self.matchingInput(userInput,"center") and context["ghost adventure"][2].self_door_lastTime == "" and context["ghost adventure"][2].get_connection(selfPos)[2] != "none":#door "center" - 1st round
            situation,speech_output = context["ghost adventure"][2].situation_feedback("door",context["ghost adventure"][2].get_connection(selfPos)[1],doorOrHideout,choice)
        elif self.matchingInput(userInput,"center") and context["ghost adventure"][2].self_door_lastTime != "" and context["ghost adventure"][2].get_connection(selfPos)[2] == "none":#door "center" & previous door
            tmpList = list(context["ghost adventure"][2].get_connection(selfPos))
            tmpList.remove(context["ghost adventure"][2].self_door_lastTime)
            situation,speech_output = context["ghost adventure"][2].situation_feedback("door",tmpList[0],doorOrHideout,choice)
        elif self.matchingInput(userInput,"right") and context["ghost adventure"][2].self_door_lastTime == "":#door "right" - 1st round
            if context["ghost adventure"][2].get_connection(selfPos)[2] != "none":
                situation,speech_output = context["ghost adventure"][2].situation_feedback("door",context["ghost adventure"][2].get_connection(selfPos)[2],doorOrHideout,choice)
            else:
                situation,speech_output = context["ghost adventure"][2].situation_feedback("door",context["ghost adventure"][2].get_connection(selfPos)[1],doorOrHideout,choice)
        elif self.matchingInput(userInput,"right") and context["ghost adventure"][2].self_door_lastTime != "" and context["ghost adventure"][2].connections[selfPos][2] != "none":#door "right" & previous door
            tmpList = list(context["ghost adventure"][2].get_connection(selfPos))
            tmpList.remove(context["ghost adventure"][2].self_door_lastTime)
            situation,speech_output = context["ghost adventure"][2].situation_feedback("door",tmpList[1],doorOrHideout,choice)#=====================================================
        elif self.matchingInput(userInput,"previous") and context["ghost adventure"][2].self_door_lastTime != "":# previous door
            situation,speech_output = context["ghost adventure"][2].situation_feedback("door",context["ghost adventure"][2].self_door_lastTime,doorOrHideout,choice)
        elif self.matchingInput(userInput,"open") or self.matchingInput(userInput,"door") or self.matchingInput(userInput,"4"):# hideout
            speech_output = "You are able to walk to " + context["ghost adventure"][2].createStr_doorList(selfPos)
            return speech_output,0
        elif self.matchingInput(userInput,"hide") or self.matchingInput(userInput,"hideout") or self.matchingInput(userInput,"hi"):# hideout
            speech_output = "You are able to" + context["ghost adventure"][2].createStr_hideouts(selfPos)
            return speech_output,0
        else:
            speech_output = "Say hide , to find available hiding spots  able to be checked , or say door , to find out which door leads to which room"
            context["ghost adventure"][6] += 1
            if context["ghost adventure"][6] >= 2:
                speech_output += " . You may say back to exit game"
            return speech_output,0

        context["ghost adventure"][6] = 0
        if situation == 0:#intruder is dead
            #self.addDeath(context["ghost adventure"][2].self_get_Pos())
            context["ghost adventure"][7] = True
            speech_output += " Before you go to hibernate , you can carve a message onto the floor . Tell me your message, or say no to cancel"
            return speech_output,0
        else:#survived one round - situation == 1
            context["ghost adventure"][4] += 1
            if random.uniform(0, 1) < 1:
                #speech_output += " .  " + random.choice(self.roomDescription)
                pass
            elif random.uniform(0, 1) < 0.6:
                speech_output = self.createStr_time(context) + speech_output
            elif random.uniform(0, 1) < 0.3:
                speech_output += " . There are " + str(self.readDeath(context["ghost adventure"][2].self_get_Pos())) + " bodies on the floor"

            if context["ghost adventure"][4] < 2:
                speech_output += " <break time=\"700ms\"/> you may say hide , to find available hiding spots , or say door , to find out which door leads to which room . "
            else:
                speech_output += " . hide or go to a door . "

            if context["ghost adventure"][4] >= 7:
                speech_output += "You can not smell the ordor anymore . You know the intruder escaped. "
                context["ghost adventure"][3] = True
                return speech_output,3
            elif context["ghost adventure"][4] >= 5:#survived 5 rounds
                speech_output += "You don't have much time left till sun goes up , find the guy quickly !"
        return speech_output,0

    def help(self,text,context):
        selfPos = context["ghost adventure"][2].self_get_Pos()
        speech_output = "You are able to " + context["ghost adventure"][2].createStr_hideouts(selfPos) + \
               " , or walk to " + context["ghost adventure"][2].createStr_doorList(selfPos) + " . Or , say back to leave the house"
        return speech_output

#===========================================================================
#                       helper functions
#===========================================================================

    def matchingInput(self,parentStr,subStr,stress=0):
        if subStr.find("no where") > -1:
            return False
        firstSubStr = subStr.split()
        if parentStr.find(firstSubStr[stress]) > -1:
            return True
        else:
            return False

    def IsNotClean(self,text):
        if not text:
            return False
        k = " " + text.lower() + " "#THIS IS BECAUSE ASR WILL ALWAYS HAVE SPACE BETWEEN THEM
        for e in self.badwords:
            if " " + e + " " in k:
                return True
        return False

    def addMessage(self,message,roomName):
        if self.IsNotClean(message) is False:
            count = self.redis_ga.getData(roomName,"messageCount")
            self.redis_ga.putData(roomName,"messages:" + count,message)
            self.redis_ga.putData(roomName,"messageCount",str(int(count) + 1))
            return True
        else:
            return False

    def readMessage(self,roomName):
        count = int(self.redis_ga.getData(roomName,"messageCount"))
        randomNum = random.randint(0, count - 1)
        ret = self.redis_ga.getData(roomName,"messages:" + str(randomNum))
        return ret

    def addDeath(self,roomName):
        death = self.redis_ga.getData(roomName,"death")
        self.redis_ga.putData(roomName,"death", str(int(death) + 1))

    def readDeath(self,roomName):
        return int(self.redis_ga.getData(roomName,"death"))

    def createStr_time(self,context):
        if context["ghost adventure"][4] <= 2:
            return str(context["ghost adventure"][4] + 10) + " gongs from the clock . "
        elif (context["ghost adventure"][4] - 2) % 12 >= 2 and (context["ghost adventure"][4] - 2) % 12 <= 4:
            tmp = ""
            for i in range(0,(context["ghost adventure"][4] - 2) % 12):
                tmp += "gong . "
            return tmp
        elif context["ghost adventure"][4] % 12 == 0:
            return "12 gongs from the clock . "
        else:
            return str((context["ghost adventure"][4] - 2) % 12) + " gongs from the clock . "
