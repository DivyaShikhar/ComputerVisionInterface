import cv2
import numpy as np
# cap = cv2.VideoCapture(0)

def AR(cap):
    imgTarget = cv2.imread("img/ball.jpg")
    myVid = cv2.VideoCapture("img/Earth_Zoom_Out.mov")

    detection = False
    fc = 0

    success, imgVid = myVid.read()
    h, w, c = imgTarget.shape
    imgVid = cv2.resize(imgVid, (w, h))

    orb = cv2.ORB_create(nfeatures=1000)
    kp1, des1 = orb.detectAndCompute(imgTarget, None)

    while True:
        success, imgCam = cap.read()

        imgAug = imgCam.copy()

        kp2, des2 = orb.detectAndCompute(imgCam, None)
        # imgCam=cv2.drawKeypoints(imgCam, kp2, None)

        if detection == False:
            myVid.set(cv2.CAP_PROP_POS_FRAMES, 0)
            fc = 0
        else:
            if fc == myVid.get(cv2.CAP_PROP_FRAME_COUNT):
                print(myVid.get(cv2.CAP_PROP_FRAME_COUNT))
                myVid.set(cv2.CAP_PROP_POS_FRAMES, 0)
                fc = 0
            success, imgVid = myVid.read()
            imgVid = cv2.resize(imgVid, (w, h))

        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des1, des2, k=2)
        good = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good.append(m)
        print(len(good))
        #imgFeatures = cv2.drawMatches(imgTarget, kp1, imgCam, kp2, good, None, flags=2)

        if len(good) > 15:
            detection = True
            src = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
            dst = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
            matrix, mask = cv2.findHomography(src, dst, cv2.RANSAC, 5)
            print(matrix)

            pts = np.float32([[0, 0], [0, h], [w, h], [w, 0]]).reshape(-1, 1, 2)
            dst = cv2.perspectiveTransform(pts, matrix)
            img2 = cv2.polylines(imgCam, [np.int32(dst)], True, (255, 0, 255), 3)

            imgWarp = cv2.warpPerspective(imgVid, matrix, (imgCam.shape[1], imgCam.shape[0]))

            maskNew = np.zeros((imgCam.shape[0], imgCam.shape[1]), np.uint8)
            cv2.fillPoly(maskNew, [np.int32(dst)], (255, 255, 255))
            maskInv = cv2.bitwise_not(maskNew)
            imgAug = cv2.bitwise_and(imgAug, imgAug, mask=maskInv)
            imgAug = cv2.bitwise_or(imgWarp, imgAug)

        #cv2.imshow("imgwarp", imgWarp)
        cv2.imshow("Interface", imgAug)
        # cv2.imshow("img2", img2)
        # cv2.imshow("imgFeatures", imgFeatures)
        # cv2.imshow("img", imgTarget)
        #cv2.imshow("vid", myVid)
        # cv2.imshow("Cam", imgCam)

        cv2.waitKey(1)
        fc += 1
        # print(fc)
