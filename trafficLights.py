import cv2
import numpy as np
import datetime


def nothing(x):
    pass

cap = cv2.VideoCapture("videoplayback.mp4")


redTime = []
greenTime = []

while True:
    ret, frame = cap.read()
    if ret is False:
        break
    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_red = np.array([122, 153, 91], dtype=np.uint8)
    upper_red = np.array([180, 255, 255], dtype=np.uint8)
    lower_green = np.array([48, 142, 82], dtype=np.uint8)
    upper_green = np.array([160, 255, 255], dtype=np.uint8)

    mask = cv2.inRange(hsv, lower_red, upper_red)
    maskGreen = cv2.inRange(hsv, lower_green, upper_green)

    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel)
    maskGreen = cv2.erode(maskGreen, kernel)

    contours, ret = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contoursGreen, ret = cv2.findContours(maskGreen, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        epsilon = 0.02*cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)

        x = approx.ravel()[0]
        y = approx.ravel()[1]

        redTimeStarting = int(0)
        if area > 200:
            time1 = str(datetime.datetime.now().strftime('%M:%S:%f')[3:-7])
            redTime.append(time1)


    for cntGreen in contoursGreen:
        areaGreen = cv2.contourArea(cntGreen)
        epsilonGreen = 0.02*cv2.arcLength(cntGreen, True)
        approxGreen = cv2.approxPolyDP(cntGreen, epsilonGreen, True)

        xGreen = approxGreen.ravel()[0]
        yGreen = approxGreen.ravel()[1]

        if areaGreen > 200:
            time1 = str(datetime.datetime.now().strftime('%M:%S:%f')[3:-7])
            greenTime.append(time1)

    cv2.imshow("frame", frame)
    cv2.imshow("mask", mask)
    cv2.imshow("greenMask", maskGreen)

    if cv2.waitKey(5) & 0xFF == ord("q"):
        break


redTimeAll = []
lastValue = 0
firstValue = 0
counter = 0
temp = 0
for x in redTime:
    if counter == 0:
        lastValue = x
        counter = 1
    else:
        if int(x) - int(lastValue) > 2 and len(redTimeAll) == 0:
            firstValue = redTime[0]
            temp = int(lastValue) - int(firstValue)
            if temp < 0:
                temp = temp + 60
                redTimeAll.append("Red light " + str(temp) + " seconds")
            else:
                redTimeAll.append("Red light " + str(temp) + " seconds")
            firstValue = x
            lastValue = x
        elif int(x) - int(lastValue) > 2 and len(redTimeAll) != 0:
            temp = int(lastValue) - int(firstValue)
            if temp < 0:
                temp = temp + 60
                redTimeAll.append("Red light " + str(temp) + " seconds")
            else:
                redTimeAll.append("Red light " + str(temp) + " seconds")
            firstValue = x
            lastValue = x
        else:
            lastValue = x

if firstValue == 0:
    firstValue = redTime[0]
    temp = int(lastValue) - int(firstValue)
    if temp < 0:
        temp = temp + 60
        redTimeAll.append("Red light " + str(temp) + " seconds")

    else:
        redTimeAll.append("Red light " + str(temp) + " seconds")

else:
    temp = int(lastValue) - int(firstValue)
    if temp < 0:
        temp = temp + 60
        redTimeAll.append("Red light " + str(temp) + " seconds")

    else:
        redTimeAll.append("Red light " + str(temp) + " seconds")



greenTimeAll = []
lastValue = 0
firstValue = 0
counter = 0
temp = 0
for x in greenTime:
    if counter == 0:
        lastValue = x
        counter = 1
    else:
        if int(x) - int(lastValue) > 2 and len(greenTimeAll) == 0:
            firstValue = greenTime[0]
            temp = int(lastValue) - int(firstValue)
            if temp < 0:
                temp = temp + 60
                greenTimeAll.append("Green light " + str(temp) + " seconds")
            else:
                greenTimeAll.append("Green light " + str(temp) + " seconds")
            firstValue = x
            lastValue = x
        elif int(x) - int(lastValue) > 2 and len(greenTimeAll) != 0:
            temp = int(lastValue) - int(firstValue)
            if temp < 0:
                temp = temp + 60
                greenTimeAll.append("Green light " + str(temp) + " seconds")
            else:
                greenTimeAll.append("Green light " + str(temp) + " seconds")
            firstValue = x
            lastValue = x
        else:
            lastValue = x

if firstValue == 0:
    firstValue = greenTime[0]
    temp = int(lastValue) - int(firstValue)
    if temp < 0:
        temp = temp + 60
        greenTimeAll.append("Green light " + str(temp) + " seconds")
    else:
        greenTimeAll.append("Green light " + str(temp) + " seconds")
else:
    temp = int(lastValue) - int(firstValue)
    if temp < 0:
        temp = temp + 60
        greenTimeAll.append("Green light " + str(temp) + " seconds")
    else:
        greenTimeAll.append("Green light " + str(temp) + " seconds")

greenTimeLength = len(greenTimeAll)
redTimeLength = len(redTimeAll)
legthCalculate = int(redTimeLength) - int(greenTimeLength)

if legthCalculate < 0:
    a = 0
    while len(redTimeAll):
        print(redTimeAll[a])
        print(greenTimeAll[a])
        a = a + 1
    print(greenTimeAll[len(greenTimeAll) - 1])
elif legthCalculate > 0:
    b = 0
    while len(greenTimeAll):
        print(redTimeAll[b])
        print(greenTimeAll[b])
        b = b + 1
    print(redTimeAll[len(redTimeAll) - 1])

cap.release()
cv2.destroyAllWindows()