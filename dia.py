import pymongo
from bson.objectid import ObjectId

dia = pymongo.MongoClient("mongodb://localhost:27017/")["DTCM"]["dia"]
binxing = dia.find_one({"_id": ObjectId("66efbbf243347a1eeb1599bd")})
del binxing["_id"]

def ask1(cc: list) -> list:
    ask_back = []
    for sym in binxing.values():
        for c in cc:
            if c in sym:
                s = sym.copy()
                s.remove(c)
                ask_back += s
                break
        
    ask_back = list(set(ask_back))
    
    return ask_back

def ask2(cc: list, dcc: list):
    res = ""
    max = 0

    for ill, sym in binxing.items():
        cnt = 0
        for c in cc:
            if c in sym:
                cnt += 1
                
                break
        
        for c in dcc:
            if c in sym:
                cnt += 0.9
                
                break

        if cnt > max:
            max = cnt
            res = ill
        
    print(res)