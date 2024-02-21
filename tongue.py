# 表里	寒熱	虛實	陰陽	病位	六淫	輕重	備註

def diagnose(img) -> dict:
    diag = {
        "表里": "",
        "寒熱": "",
        "虛實": "",
        "陰陽": "",
        "病位": "",
        "六淫": "",
        "輕重": "",
        "備註": ""
    }
    result = []
    possi = {
        "表里": {"表": (0, [("", "")]), "里": (0, [("", "")])},
        "寒熱": {"寒": 0, "熱": 0},
        "虛實": {"虛": 0, "實": 0},
        "陰陽": {"陰": 0, "陽": 0},
        # "病位": {"肝": 0, "心": 0, "脾": 0, "肺": 0, "腎": 0, "血": 0},
        "六淫": {},
        "輕重": {"輕": 0, "重": 0}
    }

    tongue = result[0]
    if "light-red" == tongue:
        diag["輕重"] = "輕"
    elif "light-white" == tongue:
        diag["虛實"] = "虛"
    elif "red" in result: # 實熱(舌苔黃)、虛熱(苔薄)
        diag["寒熱"] = "熱"
    elif "dark-red" == tongue:
        diag["寒熱"] = "熱"
        diag["陰陽"] = "陰"
        diag["虛實"] = "虛"
    elif "purple" == tongue:
        diag["備註"] += "血不暢"

    if "spike" == result[1] and not tongue == "light-red":
        diag["陰陽"] = "陽"
        diag["寒熱"] = "熱"

    if "crack" == result[2] and not tongue == "light-red":
        if tongue == "red" or tongue == "dark-red":
            possi["寒熱"]["熱"] += 0.5
            diag["寒熱"] = "熱" # 熱、陰虛
        elif tongue == "lgiht-white":
            if "血" not in diag["病位"]: diag["病位"] += "血"
            diag["虛實"] = "虛"

    if "teeth-mark" == result[3] and not tongue == "light-red":
        diag["病位"] = "脾" # 熱、陰虛

    if "thick"  == result[4]:
        diag["表里"] = "里"
    elif "thin" == result[4]:
        diag["表里"] = "表"

    if "ni" == result[5]:
        diag["六淫"] = "濕"
    elif "fu" ==  result[5]:
        diag["寒熱"] = "熱"
        if "胃" not in diag["病位"]: diag["病位"] += "胃"
        diag["陰陽"] = "陰"
        # 熱胃虛、熱胃陰虛

    if "剝落" == result[6]:
        if "胃" not in diag["病位"]: diag["病位"] += "胃"
        diag["虛實"] = "虛"
        # 胃虛、胃陰虛

    if "white" == result[7]:
        if not "crack" == result[2]: diag["寒熱"] = "寒"
        elif "thin" == result[4]:
            diag["六淫"] = "濕" # 風濕表
            diag["表里"] = "表"
        elif "crack" == result[2]:
            diag["六淫"] = "濕" # 風濕表
            diag["寒熱"] = "熱"]
    elif "yellow" == result[7]:
        diag["陰陽"] = "陽"
        diag["虛實"] = "虛"
        diag["寒熱"] = "寒"
        diag["六淫"] = "濕"
    elif "grey" == result[7] or "black" == result[7]:
        if "crack" == result[2]:
            diag["寒熱"] = "熱"
        else:
            diag["寒熱"] = "寒"

    return diag


