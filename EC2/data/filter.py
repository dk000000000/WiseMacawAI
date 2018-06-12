badwords = open('dirty.txt','r').read().split('\n')[:-1]
origin = open('profanity_blacklist.txt','r').read().split('\n')[:-1]
left = [x for x in origin if not x in badwords]
fo = open("dirty.txt", "a")
for l in left:
    fo.write(l + "\n")
fo.close()
