import cv2
from cvzone.HandTrackingModule import HandDetector
from Calc import calc
from paint import paint
import numpy as np
from AR import AR

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8, maxHands=1)
colorR = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
rectText = ['CalC', 'Paint', ' AR']

cx, cy, w, h = 50, 50, 100, 100


class DragRect():
    def __init__(self, posCenter, size=[100, 100]):
        self.posCenter = posCenter
        self.size = size

    def update(self, cursor):
        cx, cy = self.posCenter
        w, h = self.size
        # if the index finger tip is in rectangle area
        if cx - w // 2 < cursor[0] < cx + w // 2 and cy - h // 2 < cursor[1] < cy + h // 2:
            colorR = 0, 255, 0
            self.posCenter = cursor
            print(self.posCenter)


rectList = []
for x in range(3):
    rectList.append(DragRect([100, x * 160 + 80]))

while True:
    success, img = cap.read()
    if success:
        img = cv2.flip(img, 1)
        img = detector.findHands(img)
        lmList, _ = detector.findPosition(img, handNo=0, draw=False)

    if lmList:
        l, _, _ = detector.findDistance(8, 12, img)
        if l < 35:
            cursor = lmList[8]
            # call
            for rect in rectList:
                rect.update(cursor)

    ##DRAW
    m = 0
    for rect in rectList:
        cx, cy = rect.posCenter
        w, h = rect.size
        cv2.rectangle(img, (cx - w // 2, cy - h // 2), (cx + w // 2, cy + h // 2), colorR[m], cv2.FILLED)
        cv2.putText(img, rectText[m], (cx - 40, cy + 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
        m += 1

    if 470 < rectList[0].posCenter[0] < 550 and 150 < rectList[0].posCenter[1] < 300:
        calc(cap, detector)
        m = 0
        rectList = []
        for x in range(3):
            rectList.append(DragRect([100, x * 160 + 80]))

    if 470 < rectList[1].posCenter[0] < 550 and 150 < rectList[1].posCenter[1] < 300:
        paint(cap, detector)
        m = 0
        rectList = []
        for x in range(3):
            rectList.append(DragRect([100, x * 160 + 80]))

    if 470 < rectList[2].posCenter[0] < 550 and 150 < rectList[2].posCenter[1] < 300:
        AR(cap)



    ##Draw Rectangle (BIG ON THE RIGHT)
    cv2.rectangle(img, (400, 150), (550, 300), (255, 255, 255), 2)

    cv2.imshow("Interface", img)
    cv2.waitKey(1)
