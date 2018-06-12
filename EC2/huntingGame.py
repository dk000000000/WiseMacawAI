import random
import operator
class huntingGame(object):
    def __init__(self):
        self.connections = {}
        self.hideouts = {}
        self.ghost_preferList = []
        self.ghost_preferList_room = {}
        self.self_pos = ""
        self.ghost_pos = ""
        self.self_hideout = ""
        self.self_hideout_lastTime = ""
        self.self_door_lastTime = ""
        self.exits = []

        self.init_map()
        self.init_pos()

#=========================================
#               map part
#=========================================
    
    def get_connection(self,roomName):
        return self.connections[roomName]

    def get_hideout(self,roomName):
        return list(self.hideouts[roomName].keys())

    def openExits(self):
        tmpList = list(self.connections)
        tmpList.remove(self.self_pos)
        self.exits = random.sample(tmpList,2)

    def init_pos(self):
        self_startRoom = random.sample(self.hideouts.keys(),1)
        ghostStartList = list(self.hideouts.keys())
        ghostStartList.remove(self_startRoom[0])
        ghostStartList = list(filter(lambda x: x not in self.connections[self_startRoom[0]], ghostStartList))
        ghost_startRoom = random.sample(ghostStartList,1)
        self.self_pos = self_startRoom[0]
        self.ghost_pos = ghost_startRoom[0]
        self.self_hideout = ""
        self.self_hideout_lastTime = ""
        self.self_door_lastTime = ""
        self.exits = []
        tmpList = list(self.hideouts.keys())
        self.ghost_preferList_room = {tmpList[0]:0,tmpList[1]:0,tmpList[2]:0,tmpList[3]:0,\
            tmpList[4]:0,tmpList[5]:0,tmpList[6]:0,tmpList[7]:0}
        for m in tmpList:
            for n in self.hideouts[m].keys():
                self.hideouts[m][n]["count"] = 0

    def situation_feedback(self,self_doorOrHideout,self_target,ghost_doorOrHideout,ghost_choice):#ghost_choice probably have problem
        selfPos = self.self_pos#selfPos-start room | self_target-end room/action
        ghostPos = self.ghost_pos#ghostPos-start room | ghost_choice-end room/action

        situation,feedback,suggestion = 1,"",""
        if self_doorOrHideout == "door" and len(self.exits) != 0 and self_target in self.exits:
            situation = 2
            feedback += "You sneak through  " + self.createStr_door(self_target) + " . "
            return situation,feedback,suggestion#survived !!!

        if self_doorOrHideout == "door" and ghost_doorOrHideout == "door":
            if self_target == ghostPos and ghost_choice == selfPos:#cross into each other-death
                feedback += "You approach the door . The door automatically opens . "\
                   "uh oh . The black smoke engulfs you . You , are , dead <break time=\"1000ms\"/>"
                situation = 0
            elif selfPos == ghostPos:#move while ghost start in same room-death
                feedback += "dun dun dun . You try to reach the door ,"\
                   " but the black smoke surrounds you . You , are , dead <break time=\"1000ms\"/>"
                situation = 0
            elif self_target == ghost_choice:#both go into same room-death
                feedback += "You sneak through " + self.createStr_door(self_target) + " , a man surrounded "\
                   "by black smoke enters the room from another door . yikes . "\
                   "Black smoke surrounds you . You , are , dead <break time=\"1000ms\"/>"
                situation = 0
            else:#each one going its own way
                feedback += "You sneak through " + self.createStr_door(self_target) + " , it is the " + self_target
                self.self_door_lastTime = selfPos
                suggestion += self.createStr_suggestions(self.self_pos)
                self.ghost_pos = ghost_choice
                self.self_hideout_lastTime = ""
            self.self_pos = self_target
        elif self_doorOrHideout == "door" and ghost_doorOrHideout == "hide":
            if selfPos == ghostPos:#start in the same room-death
                feedback += "You try to reach the door , but the black smoke surrounds you . You , are , dead <break time=\"1000ms\"/>"
                situation = 0
            elif self_target == ghostPos:#bump into ghost-death
                feedback += "You sneak through " + self.createStr_door(self_target) + " , the man surrounded "\
                   "by blacke smoke is just in front of you . uh oh . "\
                   "He walks near . He grabs your neck <break time=\"700ms\"/> You , are , dead <break time=\"1000ms\"/>"
                situation = 0
            else:#each one going its own way
                feedback += "You sneak through " + self.createStr_door(self_target) + " , it is the " + self_target
                self.self_door_lastTime = selfPos
                suggestion += self.createStr_suggestions(self.self_pos)
                self.self_hideout_lastTime = ""
            self.self_pos = self_target
        elif self_doorOrHideout == "hide" and ghost_doorOrHideout == "door":
            self.ghost_pos = ghost_choice
            if self.self_hideout_lastTime != self_target and self.self_hideout_lastTime != "":
                tmp = self.self_hideout_lastTime.partition(' ')[2]
                tmp2 = self_target.partition(' ')[2]
                feedback += "You leave " + tmp + " and sneak to " + tmp2 + " . "
            else:
                if self.self_hideout_lastTime == self_target:
                    feedback += "You stay " + self_target + " . "
                else:
                    feedback += "You hide " + self_target + " . "
            self.hideouts[selfPos][self_target]["count"] += 1
            if self.hideouts[selfPos][self_target]["count"] == 3:
                feedback += self.hideouts[selfPos][self_target]["warning"] + " . "
            elif self.hideouts[selfPos][self_target]["count"] > 3:
                feedback += self.hideouts[selfPos][self_target]["death"] + " . "
                situation = 0
                return situation,feedback,suggestion
            self.self_hideout_lastTime = self.self_hideout#for later suggestion
            if selfPos == ghostPos:#start in the same room->see ghost move to which door
                if selfPos != ghost_choice:
                    feedback += "The shadow walks to " + self.createStr_door(ghost_choice) + " . It leaves a trail of black smoke" + self.createStr_suggestions(selfPos,True)
                else:
                    feedback += "The shadow stays in " + ghost_choice + " . Black smoke engulfs the room" + " . You better stay " + self_target
            elif selfPos == ghost_choice:#ghost move into my room
                feedback += "The shadow walks into " + selfPos + " . It is covered in black smoke" + " . You better stay " + self_target
            else:#just hear sound
                if random.uniform(0, 1) < 0.8:
                    feedback += "There are some squeaky noises from " + self.createStr_door(ghost_choice)
                else:
                    feedback += "It is chilling here"
                suggestion += self.createStr_suggestions(selfPos,True)
        elif self_doorOrHideout == "hide" and ghost_doorOrHideout == "hide":
            self.hideouts[selfPos][self_target]["count"] += 1
            if selfPos == ghostPos:#in the same room
                if self.self_hideout_lastTime != self_target and self.self_hideout_lastTime != "":#try to hide somewhere else while ghost checking hideouts in same room-death
                    tmp = self.self_hideout_lastTime.partition(' ')[2]
                    feedback += "The man in smoke notices your movement . You can not see anything but black smoke <break time=\"700ms\"/> You , are , dead <break time=\"1000ms\"/>"
                    situation = 0
                    return situation,feedback,suggestion
                elif self.self_hideout_lastTime == self_target:
                    feedback += "You stay " + self_target + " . "
                else:
                    feedback += "You hide " + self_target + " . "
                if self.hideouts[selfPos][self_target]["count"] == 3:
                    feedback += self.hideouts[selfPos][self_target]["warning"] + " . "
                tmp = self_target.partition(' ')[2]
                if tmp == ghost_choice or self.hideouts[selfPos][self_target]["count"] >= 3:#ghost check my hideout-death
                    feedback += "The shadow walks towards " + ghost_choice + " . He grabs you <break time=\"700ms\"/> You , are , dead <break time=\"1000ms\"/>"
                    situation = 0
                    return situation,feedback,suggestion
                else:#ghost not check my hideout
                    feedback += "The shadow is examining the " + ghost_choice + " . You better stay " + self_target
            else:#not in same room (just hear sound)
                if self.self_hideout_lastTime == self_target:
                    feedback += "You stay " 
                else:
                    feedback += "You hide "
                feedback += self_target + " . "
                if self.hideouts[selfPos][self_target]["count"] == 3:
                    feedback += self.hideouts[selfPos][self_target]["warning"] + " . "
                elif self.hideouts[selfPos][self_target]["count"] > 3:
                    feedback += self.hideouts[selfPos][self_target]["death"] + " . "
                    situation = 0
                    return situation,feedback,suggestion
                self.self_hideout_lastTime = self.self_hideout#for later suggestion
                if random.uniform(0, 1) < 0.8:
                    feedback += "There are some scratching noises from " + self.createStr_door(self.ghost_pos)
                else:
                    feedback += "It is chilling here"
                suggestion += self.createStr_suggestions(selfPos,True)#stay in same hideout
            self.self_hideout_lastTime = self.self_hideout
        return situation,feedback,suggestion
       
#=========================================
#           self part
#=========================================

    def self_get_Pos(self):
        return self.self_pos

    def self_set_hideout(self,hideout):
        self.self_hideout = hideout

#=========================================
#           ghost part
#=========================================

    def ghost_get_Pos(self):
        return self.ghost_pos

    def ghost_set_Pos(self,newPos):
        self.ghost_pos = newPos

    def ghost_get_ghostAction(self):
        for x in self.ghost_preferList_room:
            self.ghost_preferList_room[x] = 0
        self.ghost_preferList_room[self.self_pos] = 2
        for x in self.connections[self.self_pos]:
            if x != "none":
                self.ghost_preferList_room[x] = 1
        doorOrHideout = random.uniform(0, 1)
        if doorOrHideout < 0.5:#door 0.5
            return self.ghost_get_ghostAction_openDoor()
        else:#hideout
            if len(self.ghost_preferList) == 0:#1st step won't check its own room
                return self.ghost_get_ghostAction_openDoor()
            return self.ghost_get_ghostAction_openHideout()

    def ghost_get_ghostAction_openDoor(self):
        tmp = sorted(self.ghost_preferList_room, key=self.ghost_preferList_room.get,reverse=True)
        whichdoor = random.uniform(0, 1)
        if whichdoor < 0.4:
            target = tmp[0]
        elif whichdoor < 0.5:
            target = tmp[1]
        elif whichdoor < 0.6:
            target = tmp[2]
        elif whichdoor < 0.7:
            target = tmp[3]
        elif whichdoor < 0.8:
            target = tmp[4]
        elif whichdoor < 0.9:
            target = tmp[5]
        else:
            target = tmp[6]
        doorOrHideout = "door"
        return doorOrHideout,target

    def ghost_get_ghostAction_openHideout(self):
        self.ghost_preferList_room[self.ghost_pos] // 3
        randHideout = random.randint(0,len(self.ghost_preferList) - 1)
        target = self.ghost_preferList.pop(randHideout)
        target_revise = target.partition(' ')[2]
        doorOrHideout = "hide"
        return doorOrHideout,target_revise

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
            tmp_str = "hide "
        else:
            tmp_str = "stay " + self.self_hideout_lastTime + " . or "
            strList.remove(self.self_hideout_lastTime)

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
        data_rooms = open("data/rooms_8_v2.list","r").read().splitlines()
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