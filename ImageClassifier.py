link = "http://1ee53eb92e02.ngrok.io"   # 실행 결과에 나온 링크로 반드시 변경할 것!
copy = True                                                    # 복사: True, 이동: False

import os
import shutil

startFolder = "images/"
resultFolder = "result/"
imgext = [".jpeg", ".jpg", ".png", ".gif"]
numOfSuccess = 0
numOfImages = 0

def classify(img):
    global numOfSuccess
    global numOfImages

    stream = os.popen("curl -X POST -F file=@" + startFolder + img + " " + link)
    outputs = stream.readlines()
    result = "error"

    if '"class_name":"' in outputs[0]:
        result = outputs[0].split('"class_name":"')[1].split('"}')[0]

    if not os.path.isdir(resultFolder):
        os.makedirs(resultFolder)
    
    if not os.path.isdir(resultFolder + result):
        os.makedirs(resultFolder + result)

    startPath = startFolder + img
    resultPath = resultFolder + result + "/"+ img

    if copy:
        shutil.copy(startPath, resultPath)
    else:
        shutil.move(startPath, resultPath)
        
    numOfImages += 1

    if result == "error":
        print("Error:", img, ": 분류 실패")
    else:
        numOfSuccess += 1
        print(img, ":", result, "폴더로 분류")


if not os.path.isdir(startFolder):
    print("Error: images 폴더를 생성하고 이미지들을 넣어주세요.")
else:
    for file in os.listdir(startFolder):
        if os.path.isfile(startFolder + "/" + file):
            isImage = False
            for i in range(0, len(imgext), 1):
                if imgext[i] in file:
                    isImage = True
                    break

            if isImage:
                classify(file)

    print()
    print("이미지 분류 작업이 끝났습니다!")
    print(str(numOfImages) + "개 중 " + str(numOfSuccess) + "개 성공, (" + "{:.1f}".format(numOfSuccess / numOfImages * 100) + "%)")
