def MakeDrunkVoice(text):
    #for every phrase, make it fast/slow/load/quiet/repeating/add pause
    temp = removeAllSSML(text)
    result = ""
    for e in temp:
        result+=addPause(changePitch(changeSpeed(repeating(e))))
    return result

def changeProsody(text):
    rate = random.choice(["x-slow", "slow", "medium", "fast", "x-fast"])
    pitch = random.choice(["x-low", "low", "medium", "high", "x-high"])
    volume = random.choice(["x-soft", "soft", "medium", "loud", "x-loud"])
    return "<prosody volume=%s>" % (volume) + "<prosody rate=%s>" % (rate) + "<prosody volume=%s>" % (volume) + text + "</prosody>" + "</prosody>" + "</prosody>"
def changeSpeed(text):
    if random.random()>0.5:
        #slow
    else:
        #fast
    return

def changeVolume(text)

def changePitch(text):
    if random.random()>0.5:
        #slow
    else:
        #fast
    return

def repeating(text):
    #repeat 1,2,3 times

def addPause(text):
    #beigining/end/both

def removeAllSSML(text):
    #no <>tags
    return re.sub(r"", "\<.*?\>", text)
