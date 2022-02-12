import cv2

class Button:
    def __init__(self, pos, width, height, value):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value

    def draw(self, Img):
        cv2.rectangle(Img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (225, 225, 225), cv2.FILLED)
        cv2.rectangle(Img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (50, 50, 50), 3)
        cv2.putText(Img, self.value, (self.pos[0] + 18, self.pos[1] + 40), cv2.FONT_HERSHEY_PLAIN, 2, (50, 50, 50), 2)

    def checkClick(self, x, y, Img):
        if self.pos[0] < x < self.pos[0] + self.width and self.pos[1] < y < self.pos[1] + self.height:
            cv2.rectangle(Img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (255, 255, 255),
                          cv2.FILLED)
            cv2.rectangle(Img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (0, 0, 0), 3)
            cv2.putText(Img, self.value, (self.pos[0] + 15, self.pos[1] + 40), cv2.FONT_HERSHEY_PLAIN, 3, (50, 50, 50),
                        3)
            return True
        else:
            return False


def calc(cap, detector):
    # button
    val = [['7', '8', '9', '*'],
           ['4', '5', '6', '-'],
           ['1', '2', '3', '+'],
           ['0', '/', '.', '=']]
    buttonList = []
    for x in range(4):
        for y in range(4):
            xpos = x * 50 + 400
            ypos = y * 50 + 150
            buttonList.append(Button((xpos, ypos), 50, 50, val[y][x]))

    eqn = ''
    counter = 0

    while True:
        success, Img = cap.read()
        Img = cv2.flip(Img, 1)
        Img = detector.findHands(Img)
        lmList, _ = detector.findPosition(Img, handNo=0, draw=False)

        # draw buttons
        cv2.rectangle(Img, (400, 50), (400 + 200, 50 + 50), (225, 225, 225), cv2.FILLED)
        cv2.rectangle(Img, (400, 50), (400 + 200, 50 + 50), (50, 50, 50), 3)
        for button in buttonList:
            button.draw(Img)
        cv2.rectangle(Img, (400, 100), (400 + 200, 100 + 50), (225, 225, 225), cv2.FILLED)
        cv2.rectangle(Img, (400, 100), (400 + 200, 100 + 50), (50, 50, 50), 3)
        cv2.putText(Img, "Clear All", (400 + 30, 100 + 35), cv2.FONT_HERSHEY_PLAIN, 2, (50, 50, 50), 2)
        cv2.rectangle(Img, (50, 50), (50 + 50, 50 + 50), (50, 50, 50), cv2.FILLED)
        cv2.putText(Img, "X", (60, 90), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)

        if lmList:
            l, _, _ = detector.findDistance(8, 12, Img)
            x, y = lmList[8]

            if l < 40:
                for i, button in enumerate(buttonList):

                    if button.checkClick(x, y, Img) and counter == 0:

                        value = val[int(i % 4)][int(i / 4)]

                        if value == '=':

                            eqn = str(eval(eqn))
                        else:
                            eqn += value
                        counter = 1
                if 400 < x < 600 and 100 < y < 150:
                    eqn = ''
                if 50 < x < 100 and 50 < y < 100:
                    break

        # Avoid duplicates
        if counter != 0:
            counter += 1
            if counter > 20:
                counter = 0

        # display eqn
        cv2.putText(Img, eqn, (410, 90), cv2.FONT_HERSHEY_PLAIN, 2, (50, 50, 50), 2)
        cv2.imshow("Interface", Img)
        cv2.waitKey(1)
