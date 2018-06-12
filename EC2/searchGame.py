import random
import operator
class searchGame(object):
    def __init__(self):
        self.connections = {}
        self.hideouts = {}
        self.self_pos = ""
        self.ghost_pos = ""
        self.self_hideout_lastTime = ""
        self.self_door_lastTime = ""
        self.ghost_hideout = ""
        self.ghost_hideout_lastTime = ""

        self.init_map()
        self.init_pos()

#=========================================
#               map part
#=========================================
    
    def get_connection(self,roomName):
        return self.connections[roomName]

    def get_hideout(self,roomName):
        return list(self.hideouts[roomName].keys())

    def init_pos(self):
        self_startRoom = random.sample(self.hideouts.keys(),1)
        ghostStartList = list(self.hideouts.keys())
        ghostStartList.remove(self_startRoom[0])
        ghostStartList = list(filter(lambda x: x not in self.connections[self_startRoom[0]], ghostStartList))
        ghost_startRoom = random.sample(ghostStartList,1)
        self.self_pos = self_startRoom[0]
        self.ghost_pos = ghost_startRoom[0]
        self.ghost_hideout = ""
        self.ghost_hideout_lastTime = ""
        self.self_hideout_lastTime = ""
        self.self_door_lastTime = ""
        tmpList = list(self.hideouts.keys())
        for m in tmpList:
            for n in self.hideouts[m].keys():
                self.hideouts[m][n]["count"] = 0

    def situation_feedback(self,self_doorOrHideout,self_target,ghost_doorOrHideout,ghost_choice):#ghost_choice probably have problem
        selfPos = self.self_pos#selfPos-start room | self_target-end room/action
        ghostPos = self.ghost_pos#ghostPos-start room | ghost_choice-end room/action

        situation,feedback = 1,""
        if self_doorOrHideout == "door" and ghost_doorOrHideout == "door":
            if self_target == ghostPos and ghost_choice == selfPos:#cross into each other-death
                feedback += " The sense of flesh is so close . You open the door . "\
                   "The frightened man is shivering there . You engulfed him <break time=\"1000ms\"/>"
                situation = 0
            elif selfPos == ghostPos:#move while ghost start in same room-death
                feedback += " You noticed some movements behind you . A man is sneaking around . "\
                   "You engulfed him <break time=\"1000ms\"/>"
                situation = 0
            elif self_target == ghost_choice:#both go into same room-death
                feedback += "You walk through " + self.createStr_door(self_target) + " , a frightened man "\
                   "enters the room from another door . He is screaming . You engulfed him . <break time=\"1000ms\"/>"
                situation = 0
            else:#each one going its own way
                feedback += "You walk through " + self.createStr_door(self_target) + " , it is the " + self_target
                self.self_door_lastTime = selfPos
                self.ghost_pos = ghost_choice
                self.self_hideout_lastTime = ""
            self.self_pos = self_target
            self.self_hideout_lastTime = self.self_hideout = ""
            self.ghost_hideout_lastTime = self.ghost_hideout = ""
        elif self_doorOrHideout == "door" and ghost_doorOrHideout == "hide":
            if selfPos == ghostPos:#start in the same room-death
                feedback += " You noticed some movements behind you . A man is sneaking behind you . "\
                   "You engulfed him <break time=\"1000ms\"/>"
                situation = 0
            elif self_target == ghostPos:#bump into ghost-death
                feedback += "You walk through " + self.createStr_door(self_target) + " , the scared man bumps into you . "\
                            "He start screaming . You engulfed him . <break time=\"1000ms\"/>"
                situation = 0
            else:#each one going its own way
                feedback += "You walk through " + self.createStr_door(self_target) + " , it is the " + self_target
                self.self_door_lastTime = selfPos
                self.self_hideout_lastTime = ""
            self.self_pos = self_target
            self.self_hideout_lastTime = self.self_hideout = ""
            self.ghost_hideout_lastTime = self.ghost_hideout = ghost_choice
        elif self_doorOrHideout == "hide" and ghost_doorOrHideout == "door":
            self.ghost_pos = ghost_choice
            if self.self_hideout_lastTime != self_target and self.self_hideout_lastTime != "":
                tmp = self.self_hideout_lastTime.partition(' ')[2]
                tmp2 = self_target.partition(' ')[2]
                feedback += "You left " + tmp + " and start checking " + tmp2 + " . "
            else:
                if self.self_hideout_lastTime == self_target:
                    feedback += "You keep searching " + self_target + " . "
                else:
                    feedback += "You search " + self_target + " . "
            if selfPos == ghostPos:#start in the same room
                feedback += " You noticed some movements behind you . A man is sneaking behind you . "\
                   "You engulfed him <break time=\"1000ms\"/>"
            elif selfPos == ghost_choice:#ghost move into my room
                feedback += "A frightened man enters the room from another door . He is screaming . You engulfed him . <break time=\"1000ms\"/>"
            else:#just hear sound
                feedback += "You find nothing here"
                if random.uniform(0, 1) < 0.8:
                    feedback += " . There are some noises from " + self.createStr_door(ghost_choice)
            self.self_hideout_lastTime = self.self_hideout = self_target
            self.ghost_hideout_lastTime = self.ghost_hideout = ""
        elif self_doorOrHideout == "hide" and ghost_doorOrHideout == "hide":
            self.hideouts[selfPos][self_target]["count"] += 1
            if selfPos == ghostPos:#in the same room
                if self.ghost_hideout_lastTime != ghost_choice and self.ghost_hideout_lastTime != "":#try to hide somewhere else while ghost checking hideouts in same room-death
                    feedback += " You noticed some movements behind you . A man is sneaking behind you . You engulfed him <break time=\"1000ms\"/>"
                    situation = 0
                    return situation,feedback
                elif self.self_hideout_lastTime == self_target:
                    feedback += "You keep checking " + self_target
                else:
                    feedback += "You start checking " + self_target
                tmp = self_target.partition(' ')[2]
                if tmp == ghost_choice:#ghost check my hideout-death
                    feedback += " . You walk towards " + ghost_choice + " . You find a shivering man inside .  <break time=\"700ms\"/> You engulfed him <break time=\"1000ms\"/>"
                    situation = 0
                    return situation,feedback
                else:#ghost not check my hideout
                    feedback += " . But you find nothing"
            else:#not in same room (just hear sound)
                if self.self_hideout_lastTime == self_target:
                    feedback += "You double check " 
                else:
                    feedback += "You check "
                feedback += self_target + " . But nothing inside"
            self.self_hideout_lastTime = self.self_hideout = self_target
            self.ghost_hideout_lastTime = self.ghost_hideout = ghost_choice
        return situation,feedback
       
#=========================================
#           self part
#=========================================

    def self_get_Pos(self):
        return self.self_pos

#=========================================
#           ghost part
#=========================================

    def ghost_get_Pos(self):
        return self.ghost_pos

    def ghost_set_Pos(self,newPos):
        self.ghost_pos = newPos

    def ghost_set_hideout(self,hideout):
        self.ghost_hideout = hideout

    def ghost_get_ghostAction(self):
        doorOrHideout = random.uniform(0, 1)
        if doorOrHideout < 0.5:#door
            return self.ghost_get_ghostAction_openDoor()
        else:#hideout
            return self.ghost_get_ghostAction_openHideout()

    def ghost_get_ghostAction_openDoor(self):
        tmp = list(filter(lambda x: x != "none", self.connections[self.self_pos]))
        target = random.sample(tmp,1)
        doorOrHideout = "door"
        return doorOrHideout,target[0]

    def ghost_get_ghostAction_openHideout(self):
        tmp = list(filter(lambda x: x != "no where", self.hideouts[self.self_pos]))
        target = random.sample(tmp,1)
        doorOrHideout = "hide"
        return doorOrHideout,target[0]

#=========================================
#           helper part
#=========================================

    def matchingInput(self,parentStr,subStr,stress=0):
        firstSubStr = subStr.split()
        if parentStr.find(firstSubStr[stress]) > -1:
            return True
        else:
           return False

    def createStr_door(self,doorChoice):
        tmp_str = ""
        if self.self_door_lastTime == "":
            if self.connections[self.self_pos][0] == doorChoice:
                tmp_str = "the left door"
            elif self.connections[self.self_pos][1] == doorChoice:
                if self.connections[self.self_pos][2] != "none":
                    tmp_str = "the center door"
                else:
                    tmp_str = "the right door"
            elif self.connections[self.self_pos][2] == doorChoice:
                tmp_str = "the right door"
            else:
                tmp_str = "somewhere far away"
        else:
            tmpList = list(self.connections[self.self_pos])
            tmpList.remove(self.self_door_lastTime)
            tmpList = list(filter(lambda x: x != "none", tmpList))
            if self.self_door_lastTime == doorChoice:
                tmp_str = "the previous door"
            elif len(tmpList) == 1 and tmpList[0] == doorChoice:
                tmp_str = "the center door"
            elif len(tmpList) == 1:
                tmp_str = "somewhere far away"
            else:#len(tmpList) == 2:
                if tmpList[0] == doorChoice:
                    tmp_str = "the left door"
                elif tmpList[1] == doorChoice:
                    tmp_str = "the right door"
                else:
                    tmp_str = "somewhere far away"
        return tmp_str

    def createStr_suggestions(self,roomName,stay=False):
        tmp_str = " . You may " + self.createStr_hideouts(roomName,stay) + \
                " . Or you may open , " + \
               self.createStr_doorList(roomName)
        return tmp_str

    def createStr_hideouts(self,roomName,stay=False):
        strList = list(self.hideouts[roomName].keys())
        if stay == False:
            tmp_str = " check "

        for i in range(0,len(strList)):
            if self.matchingInput(strList[i],"no where"):
                pass
            else:
                tmp_str += strList[i] + " . or "
        return tmp_str[:-4]

    def createStr_doorList(self,roomName):
        if self.self_door_lastTime == "":
            tmp = self.connections[roomName]
            tmpList = list(filter(lambda x: x != "none", tmp))
            if len(tmpList) == 3:
                tmp_str = "left , , center or right door"
            elif len(tmpList) == 2:
                tmp_str = "left or right door"
            else:
                tmp_str = "the only door"
        else:
            tmp = self.connections[roomName]
            tmpList = list(filter(lambda x: x != "none", tmp))
            if len(tmpList) == 3:
                tmp_str = "previous , , left or right door"
            elif len(tmpList) == 2:
                tmp_str = "previous door or center door"
            else:
                tmp_str = "the previous door"
        return tmp_str

    def getNumofDoors(self,roomName):
        tmp = self.connections[roomName]
        tmpList = list(filter(lambda x: x != "none", tmp))
        return str(len(tmpList))

    #shall not access by user
    def init_map(self):
        data_rooms = open("data/rooms_8_v2_ghost.list","r").read().splitlines()
        for i in range(0, len(data_rooms)):
            line = data_rooms[i]
            listwords = line.split(".")
            listwords2 = listwords[1].split("|")
            listwords3 = listwords[2].split("|")
            listwords4 = listwords[3].split("|")
            if line[0] == '#' or line == "":
                continue
            tmpDict0 = {"warning":listwords3[0],"count":0,"death":listwords4[0]}
            tmpDict1 = {"warning":listwords3[1],"count":0,"death":listwords4[1]}
            tmpDict2 = {"warning":listwords3[2],"count":0,"death":listwords4[2]}
            self.hideouts[listwords[0]] = {listwords2[0]:tmpDict0,listwords2[1]:tmpDict1,listwords2[2]:tmpDict2}
        roomList = list(self.hideouts.keys())
        random.shuffle(roomList)
        if len(roomList) != 8:
            raise ValueError('room list should be 8 before using this algorithm!')
        self.connections[roomList[0]] = [roomList[1],roomList[7],roomList[6]]
        self.connections[roomList[1]] = [roomList[0],roomList[2],roomList[3]]
        self.connections[roomList[2]] = [roomList[1],roomList[3],"none"]
        self.connections[roomList[3]] = [roomList[1],roomList[2],roomList[4]]
        self.connections[roomList[4]] = [roomList[3],roomList[5],"none"]
        self.connections[roomList[5]] = [roomList[4],roomList[6],"none"]
        self.connections[roomList[6]] = [roomList[0],roomList[5],roomList[7]]
        self.connections[roomList[7]] = [roomList[0],roomList[6],"none"]