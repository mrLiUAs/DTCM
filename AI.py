from ultralytics import YOLO
from PIL import Image
from pathlib import Path
# from IPython.display import display, Image
# from IPython import display
import os
import cv2 as cv
import numpy as np

def Tongue_AI_analysis(in_pic):
    things_found = []

    # # Clear previous outputs
    # display.clear_output()

    # # Run YOLO checks
    # os.system("yolo checks")

    # Load the custom model of segmenting the tongue
    model = YOLO("./models/segment/best.pt")

    # Directory to save the segmented masks
    # output_directory = "D:/coding/TongueAI/output/cropped"

    # Predict with the model 
    res = model.predict(in_pic)

    # Iterate through the results
    for r in res:
        img = np.copy(r.orig_img)
        img_name = Path(r.path).stem
        # r.save(filename=f"{output_directory}/{img_name}_tongue_mask.png")

        # iterate each object contour 
        for ci, c in enumerate(r):
            label = c.names[c.boxes.cls.tolist().pop()]

            b_mask = np.zeros(img.shape[:2], np.uint8)

            # Create contour mask 
            contour = c.masks.xy.pop().astype(np.int32).reshape(-1, 1, 2)
            _ = cv.drawContours(b_mask, [contour], -1, (255, 255, 255), cv.FILLED)
            mask3ch = cv.cvtColor(b_mask, cv.COLOR_GRAY2BGR)
            isolated = cv.bitwise_and(mask3ch, img)
            # Save the segmented mask
            # save_path = os.path.join(output_directory, f"{img_name}_segmented_mask_{ci}.png")
            # cv.imwrite(save_path, isolated)
            processed_img = isolated

    # print("cropped tongue saved to:", output_directory, "as", f"{img_name}_segmented_mask_{ci}.png")

    # processed_img =  f"{output_directory}/{img_name}_segmented_mask_{ci}.png"

    # Load the custom model of dot spike declaration
    model = YOLO("./models/detect/tongue-color/best.pt")

    # Predict with the model 
    res = model.predict(processed_img, conf=0.3)

    names = model.names

    # Loop through the detected results
    for r in res:
        for c in r.boxes.cls:
            print(names[int(c)])
            things_found.append(names[int(c)])

    # Load the custom model of dot spike declaration
    model = YOLO("./models/detect/dot-spike/best.pt")


    # Predict with the model 
    res = model.predict(processed_img, conf=0.3)

    names = model.names

    # Loop through the detected results
    for r in res:
        for c in r.boxes.cls:
            print(names[int(c)])
            things_found.append(names[int(c)])

    # Load the custom model of dot spike declaration
    model = YOLO("./models/detect/tongue-crack/best.pt")


    # Predict with the model 
    res = model.predict(processed_img, conf=0.3)

    names = model.names

    # Loop through the detected results
    for r in res:
        for c in r.boxes.cls:
            print(names[int(c)])
            things_found.append(names[int(c)])

    # Load the custom model of dot spike declaration
    model = YOLO("./models/detect/teeth-mark/best.pt")

    # Predict with the model 
    res = model.predict(processed_img, conf=0.3)

    names = model.names

    # Loop through the detected results
    for r in res:
        for c in r.boxes.cls:
            print(names[int(c)])
            things_found.append(names[int(c)])

    # Load the custom model of dot spike declaration
    model = YOLO("./models/detect/coat-thickness/best.pt")

    # Predict with the model 
    res = model.predict(processed_img, conf=0.3)

    names = model.names

    # Loop through the detected results
    for r in res:
        for c in r.boxes.cls:
            print(names[int(c)])
            things_found.append(names[int(c)])

    # Load the custom model of dot spike declaration
    model = YOLO("./models/detect/ni-fu/best.pt")

    # Predict with the model 
    res = model.predict(processed_img, conf=0.3)

    names = model.names

    # Loop through the detected results
    for r in res:
        for c in r.boxes.cls:
            print(names[int(c)])
            things_found.append(names[int(c)])

    # Load the custom model of dot spike declaration
    model = YOLO("./models/detect/coat-break-down/best.pt")

    # Predict with the model 
    res = model.predict(processed_img, conf=0.3)

    names = model.names

    # Loop through the detected results
    for r in res:
        for c in r.boxes.cls:
            print(names[int(c)])
            things_found.append(names[int(c)])
            break

    # Load the custom model of dot spike declaration
    model = YOLO("./models/detect/tongue-coat-color/best.pt")

    # Predict with the model 
    res = model.predict(processed_img, conf=0.3)

    names = model.names

    # Loop through the detected results
    for r in res:
        for c in r.boxes.cls:
            print(names[int(c)])
            things_found.append(names[int(c)])

    return(things_found)

# D:\coding\TongueAI\predict_data\test.png
# "C:\Users\~owo~\Downloads\20240223_210537.jpg"

# print(Tongue_AI_analysis(img))

# 表里	寒熱	虛實	陰陽	病位	六淫	輕重	備註

def diagnose(img) -> dict:
    diag = {
        "表": 0,
        "里": 0,
        "寒": 0,
        "熱": 0,
        "虛": 0,
        "實": 0,
        "陰": 0,
        "陽": 0,
        "血": 0,
        "脾": 0,
        "胃": 0,
        "濕": 0,
        "風": 0,
        "輕": 0,
        "重": 0
    }
    lotte = {

    }
    result = Tongue_AI_analysis(img)

    tongue = result[0]
    if "light-red" == tongue:
        diag["輕"] = 1
    elif "light-white" == tongue:
        diag["虛"] = 1
    elif "red" in result: # 實熱(舌苔黃)、虛熱(苔薄)
        diag["熱"] = 1
    elif "dark-red" == tongue:
        diag["熱"] = 1
        diag["陰"] = 1
        diag["虛"] = 1
    elif "purple" == tongue:
        diag["備註"] += "血不暢"

    if "spike" == result[1] and not tongue == "light-red":
        diag["陽"] = 1
        diag["熱"] = 1

    if "crack" == result[2] and not tongue == "light-red":
        if tongue == "red" or tongue == "dark-red":
            diag["熱"] += 0.5

            diag["陰"] += 0.5
            if "陰" in lotte: lotte["陰"].append("虛")
            else: lotte["陰"] = ["虛"]
            if "虛" in lotte: diag["虛"].append("陰")
            else: diag["虛"] = ["陰"]
        elif tongue == "lgiht-white":
            diag["血"] = 1
            diag["虛"] = 1

    if "teeth-mark" == result[3] and not tongue == "light-red":
        diag["脾"] = 1 # 熱、陰虛

    if "thick"  == result[4]:
        diag["里"] = 1
    elif "thin" == result[4]:
        diag["表"] = 1

    if "ni" == result[5]:
        diag["濕"] = 1
    elif "fu" ==  result[5]:
        diag["熱"] += 0.5
        lotte["熱"] += ["胃", "虛"]
        diag["胃"] += 0.5
        lotte["熱"] += ["胃", "虛"]
        diag["陰"] += 0.5
        lotte["陰"] += ["熱", "胃", "虛"]
        diag["虛"] += 0.5
        lotte["虛"] += ["熱", "胃"]
        # 熱胃虛、熱胃陰虛

    if "剝落" == result[6]:
        diag["胃"] += 0.5
        if "胃" in lotte: lotte["胃"] += ["虛"]
        else: lotte["胃"] = ["虛"]
        diag["虛"] += 0.5
        if "虛" in lotte: lotte["虛"] += ["胃"]
        else: lotte["虛"] = ["胃"]
        diag["陰"] += 0.5
        if "陰" in lotte: lotte["陰"] += ["胃", "虛"]
        lotte["陰"] = ["胃", "虛"]
        # 胃虛、胃陰虛

    if "white" == result[7]:
        if not "crack" == result[2]: diag["寒熱"] = "寒"
        elif "thin" == result[4]:
            diag["風"] = 1
            diag["濕"] = 1 # 風濕表
            diag["表"] = 1
        elif "crack" == result[2]:
            diag["濕"] = 1
            diag["熱"] = 1
    elif "yellow" == result[7]:
        diag["熱"] = 1
    elif "grey" == result[7] or "black" == result[7]:
        if "crack" == result[2]:
            diag["熱"] = 1
        else:
            diag["寒"] = 1

    ans = {
        "表里": "",
        "寒熱": "",
        "虛實": "",
        "陰陽": "",
        "病位": "",
        "六淫": "",
        "輕重": "",
        "備註": ""
    }
    
    for i in range(5):
        for k, v in diag.items():
            if v >= 1:
                for x in lotte.get(k, []):
                    diag[x] = 1
    
    flag = 1
    tag =  ""
    for k, v in diag.items():
        if flag == 1:
            if k == "血":
                if diag["血"] >= 1: ans["病位"] += "血"
                if diag["脾"] >= 1: ans["病位"] += "脾"
                if diag["胃"] >= 1: ans["病位"] += "胃"
                flag = 3
            elif k == "濕":
                if diag["濕"] >= 1: ans["六淫"] += "濕"
                if diag["風"] >= 1: ans["六淫"] += "風"
                flag = 2
            else:
                if tag == "":
                    tag = k
                else:
                    # print(tag, k, diag[tag], diag[k])
                    if diag[tag] >= 1:
                        if v < 1:
                            ans[tag+k] = tag
                    else:
                        if v >= 1:
                            ans[tag+k] = k
                    tag = ""

        elif flag == 0:
            flag = 1
        else:
            flag -= 1

    print(ans)
    return ans
