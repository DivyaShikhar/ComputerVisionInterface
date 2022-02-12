import cv2
import numpy as np
import time
import os
from cvzone.HandTrackingModule import HandDetector


#################################################################################
def fingersUp(self):
    fingers = []
    # Thumb
    if self.lmList[self.tipIds[0]][1] < self.lmList[self.tipIds[0] - 1][1]:
        fingers.append(1)
    else:
        fingers.append(0)

    # Fingers
    for id in range(1, 5):
        if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
            fingers.append(1)
        else:
            fingers.append(0)

        # totalFingers = fingers.count(1)

    return fingers


###############################################################


def paint(cap, detector):
    xp, yp = 0, 0
    color = (255, 255, 255)

    imgc = np.zeros((480, 640, 3), np.uint8)

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)

        # Landmarks
        img = detector.findHands(img)
        lmList, _ = detector.findPosition(img, draw=False)

        if lmList:
            l, _, _ = detector.findDistance(8, 12, img)
            x1, y1 = lmList[8]
            x2, y2 = lmList[12]
            if l < 40:
                if 560 < x1 < 610 and 50 < y1 < 100:
                    break

            # Which finger is up
            fingers = detector.fingersUp()

            # If selection mode
            if fingers[1] and fingers[2]:
                cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), color, cv2.FILLED)

                # click checking
                if y1 < 125:
                    if 40 < x1 < 100:
                        color = (0, 255, 0)
                    elif 180 < x1 < 240:
                        color = (0, 0, 255)
                    elif 320 < x1 < 380:
                        color = (255, 0, 0)
                    elif 460 < x1 < 520:
                        color = (255, 255, 255)
                    else:
                        color = (0, 0, 0)
            cv2.rectangle(img, (560, 100), (620, 160), color, cv2.FILLED)

            # If Drawing mode
            if fingers[1] and fingers[2] == False:
                cv2.circle(img, (x1, y1), 15, color, cv2.FILLED)

                if xp == 0 and yp == 0:
                    xp, yp = x1, y1

                cv2.line(img, (xp, yp), (x1, y1), color, 15)
                cv2.line(imgc, (xp, yp), (x1, y1), color, 15)
                xp, yp = x1, y1

        cv2.rectangle(img, (40, 20), (100, 80), (0, 255, 0), cv2.FILLED)
        cv2.rectangle(img, (180, 20), (240, 80), (0, 0, 255), cv2.FILLED)
        cv2.rectangle(img, (320, 20), (380, 80), (255, 0, 0), cv2.FILLED)
        cv2.rectangle(img, (450, 20), (530, 80), (255, 255, 255), cv2.FILLED)
        cv2.putText(img, "RUB", (460, 65), cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 50, 50), 2)

        imgGray = cv2.cvtColor(imgc, cv2.COLOR_BGR2GRAY)
        _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
        imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
        img = cv2.bitwise_and(img, imgInv)
        img = cv2.bitwise_or(img, imgc)
        cv2.rectangle(img, (560, 20), (560 + 50, 20 + 50), (50, 50, 50), cv2.FILLED)
        cv2.putText(img, "X", (570, 65), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255),
                    3)
        # img = cv2.addWeighted(img, 0.5, imgc, 0.5, 0.5)

        cv2.imshow("Interface", imgInv)
        cv2.imshow("Interface", imgc)
        cv2.imshow("Interface", img)
        cv2.waitKey(1)
