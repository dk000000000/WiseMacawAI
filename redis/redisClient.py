import redis

class redisClient():
    def __init__(self,table):
        if table == "log":
            self.client = redis.Redis('localhost',port=6400)
        elif table == "exceptions":
            self.client = redis.Redis('localhost',port=6401)
        elif table == "reddit":
            self.client = redis.Redis('localhost',port=6402)
        elif table == "twitter":
            self.client = redis.Redis('localhost',port=6403)
        elif table == "messageBoard":
            self.client = redis.Redis('localhost',port=6404)
        elif table == "textAdventure":
            self.client = redis.Redis('localhost',port=6405)
        elif table == "ghostAdventure":
            self.client = redis.Redis('localhost',port=6406)
        elif table == "menuLog":
            self.client = redis.Redis('localhost',port=6407)
        else:
            raise Exception("no matched table found")

	#sessionData is the data belongs to user with corresponding sessionId
    def putData(self,field,subField,data):
        #field: "sessionData","adventure,"news","exceptions"...etc
        return self.client.hset(field,subField,data)

    def getData(self,field,subField):
        tmp = self.client.hget(field,subField)
        if tmp is None:
            raise Exception("no data exist on field & subfield")
        else:
            tmp = self.client.hget(field,subField).decode("utf-8")
            return tmp

    def delData(self,field,subField):
        if self.client.hdel(field,subField) is 0:
            raise Exception("no data exist on same field & subfield")

    def getField(self):
        list = []
        cursor = 0
        while True:
            tmp = self.client.scan(cursor)
            list += tmp[1]
            if tmp[0] == 0:
                break
            else:
                cursor = tmp[0]
        list = [x.decode("utf-8") for x in list]
        return list

    def getSubField(self,field):
        list = []
        cursor = 0
        while True:
            tmp = self.client.hscan(field,cursor)
            list += tmp[1]
            if tmp[0] == 0:
                break
            else:
                cursor = tmp[0]
        list = [x.decode("utf-8") for x in list]
        return list
