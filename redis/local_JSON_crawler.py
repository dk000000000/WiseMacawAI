import redisClient
import json

def main():
    log()
    exceptions()
    reddit()
    twitter()
    messageBoard()
    textAdventure()
    ghostAdventure()
    return

#========================
def log():
    pass

def exceptions():
    redis = redisClient.redisClient("exceptions")
    redis.putData("messageBoard","expCount",str(0))

def reddit():
    pass

def twitter():
    pass

def messageBoard():
    redis = redisClient.redisClient("messageBoard")
    with open('messageBoard.json','r') as t:
        f = json.load(t)
    data = []
    for item in f:
        parsed_context = processJson_messageBaord(item)
        data.append(parsed_context)
    i = 0
    for item in data:
        x = redis.putData(item["message"],"time",item["time"])
        x = redis.putData(item["message"],"votes",item["votes"])

def textAdventure():
    redis = redisClient.redisClient("textAdventure")
    with open('textAdventure.json','r') as t:
        f = json.load(t)
    data = []
    for item in f:
        parsed_context = processJson_textAdventure(item)
        data.append(parsed_context)
    for item in data:
        for i in range(len(item["messages"])):
            x = redis.putData(item["roomName"],"messages:" + str(i),item["messages"][i])
        x = redis.putData(item["roomName"],"death",item["death"])
        x = redis.putData(item["roomName"],"messageCount",len(item["messages"]))

def ghostAdventure():
    redis = redisClient.redisClient("ghostAdventure")
    with open('ghostAdventure.json','r') as t:
        f = json.load(t)
    data = []
    for item in f:
        parsed_context = processJson_ghostAdventure(item)
        data.append(parsed_context)
    for item in data:
        for i in range(len(item["messages"])):
            x = redis.putData(item["roomName"],"messages:" + str(i),item["messages"][i])
        x = redis.putData(item["roomName"],"death",item["death"])
        x = redis.putData(item["roomName"],"messageCount",len(item["messages"]))
#========================

#========================
def processJson_messageBaord(item):
      return {"message": item["message"]["S"],"time":item["time"]["S"],"votes": item["votes"]["N"]}

def processJson_textAdventure(item):
    ret = {}
    ret["death"] = item["death"]["N"]
    ret["roomName"] = item["roomName"]["S"]
    ret["messages"] = []
    for x in item["messages"]["L"]:
        ret["messages"].append(x["S"])
    return ret

def processJson_ghostAdventure(item):
    ret = {}
    ret["death"] = item["death"]["N"]
    ret["roomName"] = item["roomName"]["S"]
    ret["messages"] = []
    for x in item["messages"]["L"]:
        ret["messages"].append(x["S"])
    return ret

#========================
if __name__ == "__main__":
    main()
