from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

dia = MongoClient(os.getenv("MONGO_DB_URI"))["DTCM"]["dia"]
binxing = dia.find_one({"_id": ObjectId(os.getenv("BINXING"))})
binway = dia.find_one({"_id": ObjectId(os.getenv("BINWAY"))})
del binxing["_id"]
del binway["_id"]

def ask1(cc: list) -> list:
    """
    binxing find possible dcc and ask patient
    """

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
    """
    find the most possible binxing and then ask3 and then ask back again
    """

    res = ""
    maxi = 0

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

        if cnt > maxi:
            maxi = cnt
            res = ill
        
    return ask3(cc, dcc, res)

def ask3(cc: list, dcc: list, ccill: str) -> list:
    """
    find top 5 binway
    """
    
    scores = {}

    for place, v in binway.items():
        sym = v["sym"]
        ill = v["ill"]

        cnt = 0
        for c in cc:
            if c in sym:
                cnt += 1
                
                break
        
        for c in dcc:
            if c in sym:
                cnt += 0.9
                
                break

        if ccill in ill:
            cnt += 1

        scores[place] = cnt

    res = sorted(scores.items(), key=lambda item: item[1], reverse=True)[:5]
        
    return res

def ask4(bws: list) -> list:
    res = []
    for bw in bws:
        res += binway[bw]["sym"]

    return res