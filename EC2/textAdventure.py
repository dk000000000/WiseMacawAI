from module import module
import redisClient
import random
import huntingGame
from nltk.util import ngrams
import re

class textAdventure(module):
    def __init__(self):
        super().__init__()
        self.badwords = sorted(open('data/dirty.txt','r').read().split('\n'),key = lambda x:len(x),reverse=True)
        self.roomDescription = open('data/room_descriptions.list','r').read().split('\n')
        self.roomDescription.pop()
        self.roomDescription = list(filter(lambda x: x[0] != "#", self.roomDescription))
        self.redis_ta = redisClient.redisClient("textAdventure")

    def intro(self,text,context):
        game = huntingGame.huntingGame()
        context["adventure"] = []
        context["adventure"].append(False)#0_continue/restart game due to interruption
        context["adventure"].append(0)#1_tutorial(0: init; 1: in tutorial; 2:no tutorial)
        context["adventure"].append(game)#2_game obj
        context["adventure"].append(False)#3_game need restart due to finsh/death
        context["adventure"].append(0)#4_number of round alive
        context["adventure"].append(False)#5_DEBUG_mode(not enabled right now)
        context["adventure"].append(0)#6_count for wrong inputs
        context["adventure"].append(False)#7_comment trigger
        response = "Let's play a text adventure game . Say back to exit game <break time=\"700ms\"/>  " \
                   "Do you want to survery the house first? Or skip to night time"
        
        return response

    def response(self,userInput,context):
        response = ""
        AMAZON_yes = ["AMAZON.ResumeIntent","AMAZON.YesIntent"]
        AMAZON_no = ["AMAZON.NoIntent"]

        selfPos = context["adventure"][2].self_get_Pos()
        ghostPos = context["adventure"][2].ghost_get_Pos()

        if context["adventure"][1] == 0:
            if self.matchingInput(userInput,"survey") or self.matchingInput(userInput,"restart") or self.matchingInput(userInput,"start") or context["intent"] in AMAZON_yes:
                context["adventure"][1] = 1
                context["adventure"][2].init_pos()
                context["adventure"][4] = 0
                selfPos = context["adventure"][2].self_get_Pos()
                response = "You are inside a haunted house in the morning, explore the house before 2 PM . "\
						"You wake up inside the " + selfPos + " on the floor , you may "\
                        "say hide to find available hiding spots , or say door , "\
                        "to find out which door leads to which room . You don't know what is behind each door"
            elif self.matchingInput(userInput,"night") or self.matchingInput(userInput,"real") or self.matchingInput(userInput,"skip") or self.matchingInput(userInput,"game"):
                context["adventure"][1] = 2
                context["adventure"][2].init_pos()
                context["adventure"][4] = 0
                selfPos = context["adventure"][2].self_get_Pos()
                response = "You are inside a haunted house at dusk , try to survive till 3 AM . "\
						"You wake up inside the " + selfPos + " on the floor , you may "\
                        "say hide to find available hiding spots , or say door , "\
                        "to find out which door leads to which room . You don't know what is behind each door"
            else:
                context["status"] = ["West","inArea","response"]
                response += "Return when you wish to try again, says the spirit, before its voice fades into the "\
                "darkness around you. You find yourself back at the edge of the western woods. The detective turns "\
                "to you. So, who should we talk to? she asks, The Fortune Teller, or The Spirit? If you think we "\
                "should check somewhere else, just tell me a direction and we'll go there."
            return response,0

        if context["adventure"][0] == True: #been interrupted by other modules(continue or restart)
            context["adventure"][0] = False
            if self.matchingInput(userInput,"restart") or self.matchingInput(userInput,"start") or self.matchingInput(userInput,"again"):#restart game

                context["adventure"][2].init_pos()
                context["adventure"][3] = False
                context["adventure"][4] = 0
                selfPos = context["adventure"][2].self_get_Pos()
                ghostPos = context["adventure"][2].ghost_get_Pos()
                response = "Let's play the game again , wish you good luck on this time . Remember , say back to exit game <break time=\"700ms\"/> "\
						"You wake up inside the " + selfPos + " on the floor , you may say hide , to find available hiding spots , "\
                        "or say door , to find out which door leads to which room"
                return response,0
            elif self.matchingInput(userInput,"keep") or context["intent"] in AMAZON_yes:#continue game

                selfPos = context["adventure"][2].self_get_Pos()
                ghostPos = context["adventure"][2].ghost_get_Pos()
            else:
                context["status"] = ["West","inArea","response"]
                response += "Return when you wish to try again, says the spirit, before its voice fades into the "\
                "darkness around you. You find yourself back at the edge of the western woods. The detective turns "\
                "to you. So, who should we talk to? she asks, The Fortune Teller, or The Spirit? If you think we "\
                "should check somewhere else, just tell me a direction and we'll go there."

                return response,0

        if context["adventure"][7] == True and (context["intent"] in AMAZON_no or self.matchingInput(userInput,"no")):
            context["adventure"][7] = False
            #context["adventure"][3] = True
            return "That's a pity. Well.",1
        elif context["adventure"][7] == True:
            context["adventure"][7] = False
            #context["adventure"][3] = True
            if self.addMessage(userInput,selfPos) is True:
                return "Your message is recorded.",1
            else:
                return "Sorry, this message violates Amazon guidelines.",1

        if context["adventure"][3] == True and (self.matchingInput(userInput,"restart") or self.matchingInput(userInput,"start") or self.matchingInput(userInput,"add") \
                or self.matchingInput(userInput,"adventure") or self.matchingInput(userInput,"again") or context["intent"] in AMAZON_yes):#restart game
            context["adventure"][3] = False
            context["adventure"][2].init_pos()
            context["adventure"][4] = 0

            selfPos = context["adventure"][2].self_get_Pos()
            ghostPos = context["adventure"][2].ghost_get_Pos()
            response += "Let's play the game again , wish you good luck on this time . Remember , say back to exit game <break time=\"700ms\"/> " \
						"You wake up inside the " + selfPos + " on the floor , you may say hide , to find available hiding spots , "\
                        "or say door , to find out which door leads to which room"
            return response,0
        elif context["adventure"][3] == True and (self.matchingInput(userInput,"survey") or self.matchingInput(userInput,"practice")):
            context["adventure"][1] = 1
            context["adventure"][2].init_pos()
            context["adventure"][3] = False
            context["adventure"][4] = 0
            selfPos = context["adventure"][2].self_get_Pos()
            response += "You are inside a haunted house in morning, explore the house before 2 PM . "\
						"You wake up inside the " + selfPos + " on the floor , you may "\
                        "say hide , to find available hide locations , or say door , "\
                        "to find out available doors . You don't know what is behind each door"
            return response,0
        elif context["adventure"][3] == True:
            context["status"] = ["West","inArea","response"]
            response += "Return when you wish to try again, says the spirit, before its voice fades into the "\
            "darkness around you. You find yourself back at the edge of the western woods. The detective turns "\
            "to you. So, who should we talk to? she asks, The Fortune Teller, or The Spirit? If you think we "\
            "should check somewhere else, just tell me a direction and we'll go there."
            context["adventure"][3] = False
            context["adventure"][2].init_pos()
            context["adventure"][4] = 0

            return response,0

        speech_output,stage = "",0
        if context["adventure"][1] == 1:#in tutorial
            leftDoor = context["adventure"][2].get_connection(selfPos)[0]
            ghostPosList = list(filter(lambda x: x not in selfPos and x not in context["adventure"][2].get_connection(selfPos),\
               context["adventure"][2].get_connection(leftDoor)))
            ghostPos = random.sample(ghostPosList,1)
            context["adventure"][2].ghost_set_Pos(ghostPos[0])
            doorOrHideout,choice = "hide",context["adventure"][2].get_hideout(ghostPos[0])[0]
        elif context["adventure"][4] < 1:#user won't die in 1st round
            doorOrHideout,choice = "hide",context["adventure"][2].get_hideout(ghostPos)[0]
        elif context["adventure"][4] % 3 != 0:#normal ghost
            doorOrHideout,choice = context["adventure"][2].ghost_get_ghostAction()
        else:#three rounds teleport
            specialAbility = random.uniform(0, 1)
            if specialAbility < 0.6:#likelihood to teleport
                doorOrHideout,choice = "door",context["adventure"][2].ghost_get_Pos()
            else:
                doorOrHideout,choice = context["adventure"][2].ghost_get_ghostAction()

        if self.matchingInput(userInput,context["adventure"][2].get_hideout(selfPos)[0],2):#hideout 1
            context["adventure"][2].self_set_hideout(context["adventure"][2].get_hideout(selfPos)[0])
            situation,speech_output,suggestion = context["adventure"][2].situation_feedback("hide",context["adventure"][2].get_hideout(selfPos)[0],doorOrHideout,choice)
        elif self.matchingInput(userInput,context["adventure"][2].get_hideout(selfPos)[1],2):#hideout 2
            context["adventure"][2].self_set_hideout(context["adventure"][2].get_hideout(selfPos)[1])
            situation,speech_output,suggestion = context["adventure"][2].situation_feedback("hide",context["adventure"][2].get_hideout(selfPos)[1],doorOrHideout,choice)
        elif self.matchingInput(userInput,context["adventure"][2].get_hideout(selfPos)[2],2):#hideout 3
            context["adventure"][2].self_set_hideout(context["adventure"][2].get_hideout(selfPos)[2])
            situation,speech_output,suggestion = context["adventure"][2].situation_feedback("hide",context["adventure"][2].get_hideout(selfPos)[2],doorOrHideout,choice)
        elif self.matchingInput(userInput,"left") and context["adventure"][2].self_door_lastTime == "":#door "left" - 1st round
            situation,speech_output,suggestion = context["adventure"][2].situation_feedback("door",context["adventure"][2].get_connection(selfPos)[0],doorOrHideout,choice)
        elif self.matchingInput(userInput,"left") and context["adventure"][2].self_door_lastTime != "" and context["adventure"][2].get_connection(selfPos)[2] != "none":#door "left" & previous door
            tmpList = list(context["adventure"][2].get_connection(selfPos))
            tmpList.remove(context["adventure"][2].self_door_lastTime)#???
            situation,speech_output,suggestion = context["adventure"][2].situation_feedback("door",tmpList[0],doorOrHideout,choice)
        elif self.matchingInput(userInput,"center") and context["adventure"][2].self_door_lastTime == "" and context["adventure"][2].get_connection(selfPos)[2] != "none":#door "center" - 1st round
            situation,speech_output,suggestion = context["adventure"][2].situation_feedback("door",context["adventure"][2].get_connection(selfPos)[1],doorOrHideout,choice)
        elif self.matchingInput(userInput,"center") and context["adventure"][2].self_door_lastTime != "" and context["adventure"][2].get_connection(selfPos)[2] == "none":#door "center" & previous door
            tmpList = list(context["adventure"][2].get_connection(selfPos))
            tmpList.remove(context["adventure"][2].self_door_lastTime)
            situation,speech_output,suggestion = context["adventure"][2].situation_feedback("door",tmpList[0],doorOrHideout,choice)
        elif self.matchingInput(userInput,"right") and context["adventure"][2].self_door_lastTime == "":#door "right" - 1st round
            if context["adventure"][2].get_connection(selfPos)[2] != "none":
                situation,speech_output,suggestion = context["adventure"][2].situation_feedback("door",context["adventure"][2].get_connection(selfPos)[2],doorOrHideout,choice)
            else:
                situation,speech_output,suggestion = context["adventure"][2].situation_feedback("door",context["adventure"][2].get_connection(selfPos)[1],doorOrHideout,choice)
        elif self.matchingInput(userInput,"right") and context["adventure"][2].self_door_lastTime != "" and context["adventure"][2].connections[selfPos][2] != "none":#door "right" & previous door
            tmpList = list(context["adventure"][2].get_connection(selfPos))
            tmpList.remove(context["adventure"][2].self_door_lastTime)
            situation,speech_output,suggestion = context["adventure"][2].situation_feedback("door",tmpList[1],doorOrHideout,choice)#=====================================================
        elif self.matchingInput(userInput,"previous") and context["adventure"][2].self_door_lastTime != "":# previous door
            situation,speech_output,suggestion = context["adventure"][2].situation_feedback("door",context["adventure"][2].self_door_lastTime,doorOrHideout,choice)
        elif self.matchingInput(userInput,"stay"):# stay in hideout
            context["adventure"][2].self_set_hideout(context["adventure"][2].self_hideout_lastTime)
            situation,speech_output,suggestion = context["adventure"][2].situation_feedback("hide",context["adventure"][2].self_hideout_lastTime,doorOrHideout,choice)
        elif self.matchingInput(userInput,"open") or self.matchingInput(userInput,"door") or self.matchingInput(userInput,"4"):# hideout
            speech_output = "You are able to escape to " + context["adventure"][2].createStr_doorList(selfPos)
            return speech_output,0
        elif self.matchingInput(userInput,"hide") or self.matchingInput(userInput,"hideout") or self.matchingInput(userInput,"hi"):# hideout
            speech_output = "You are able to " + context["adventure"][2].createStr_hideouts(selfPos)
            return speech_output,0
        else:
            speech_output = "Say hide , to find available hiding spots , or say door , to find out which door leads to which room"
            context["adventure"][6] += 1
            if context["adventure"][6] >= 2:
                speech_output += " . You may say back to exit game"
            return speech_output,0

        context["adventure"][6] = 0
        if situation == 0 and context["adventure"][1] == 1:#player is dead in tutorial
            self.addDeath(context["adventure"][2].self_get_Pos())
            speech_output += ""
            context["adventure"][1] = 0
            stage = 5
        elif situation == 0:#player is dead
            self.addDeath(context["adventure"][2].self_get_Pos())
            context["adventure"][7] = True
            speech_output += " Before you die , you can carve a message onto the wall . Tell me your message, or say no to cancel"
        elif situation == 1:#survived one round
            context["adventure"][4] += 1
            if random.uniform(0, 1) < 1:
                speech_output += " . " + random.choice(self.roomDescription)
            elif random.uniform(0, 1) < 0.6:
                speech_output = self.createStr_time(context) + speech_output
            elif random.uniform(0, 1) < 0.3:
                speech_output += " . There are " + str(self.readDeath(context["adventure"][2].self_get_Pos())) + " bodies on the floor"

            if random.uniform(0, 1) < 0.6:
                randomDescription = ["written on the wall","engraved on the floor","painted on celling"]
                speech_output += " . There is something " + random.choice(randomDescription) + " <break time=\"1200ms\"/> <prosody pitch=\"low\">" + self.readMessage(selfPos) + "</prosody>"

            if context["adventure"][4] < 2:
                speech_output += " <break time=\"700ms\"/> you may say hide , to find available hiding spots , or say door , to find out which door leads to which room"
            else:
                speech_output += " . hide or go to a door"

            if context["adventure"][4] == 4 and context["adventure"][1] == 1:#tutorial exit
                context["adventure"][1] = 0
                stage = 5
                speech_output += " <break time=\"700ms\"/> Time to leave the house."
            if context["adventure"][4] >= 5:#survived 5 rounds
                context["adventure"][2].openExits()
                speech_output += " <break time=\"700ms\"/> The emergency exits are opened , get there quickly !"
        elif situation == 2:#reached the exit
            speech_output += "hurray, you reached the exit."
            context["adventure"][3] = True
            stage = 2
        return speech_output,stage

    def help(self,text,context):
        selfPos = context["adventure"][2].self_get_Pos()
        speech_output = "You are able to " + context["adventure"][2].createStr_hideouts(selfPos) + \
               " , or escape to " + context["adventure"][2].createStr_doorList(selfPos) + " . Or , say back to try something else"
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
            count = self.redis_ta.getData(roomName,"messageCount")
            self.redis_ta.putData(roomName,"messages:" + count,message)
            self.redis_ta.putData(roomName,"messageCount",str(int(count) + 1))
            return True
        else:
            return False

    def readMessage(self,roomName):
        count = int(self.redis_ta.getData(roomName,"messageCount"))
        randomNum = random.randint(0, count - 1)
        ret = self.redis_ta.getData(roomName,"messages:" + str(randomNum))
        return ret

    def addDeath(self,roomName):
        death = self.redis_ta.getData(roomName,"death")
        self.redis_ta.putData(roomName,"death", str(int(death) + 1))

    def readDeath(self,roomName):
        return int(self.redis_ta.getData(roomName,"death"))

    def createStr_time(self,context):
        if context["adventure"][4] <= 2:
            return str(context["adventure"][4] + 10) + " gongs from the clock . "
        elif (context["adventure"][4] - 2) % 12 >= 2 and (context["adventure"][4] - 2) % 12 <= 4:
            tmp = ""
            for i in range(0,(context["adventure"][4] - 2) % 12):
                tmp += "gong . "
            return tmp
        elif context["adventure"][4] % 12 == 0:
            return "12 gongs from the clock . "
        else:
            return str((context["adventure"][4] - 2) % 12) + " gongs from the clock . "
