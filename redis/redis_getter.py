import redisClient
#import json
def main():
    redis = redisClient.redisClient("messageBoard")
    x = redis.getField()
    #y = redis.getField("stay in the good world")
    
    print(x)

    return

def processJson_messageBaord(item):
    return {"message": item["message"]["S"],"time":item["time"]["S"],"votes": item["votes"]["N"]}

if __name__ == "__main__":
    main()