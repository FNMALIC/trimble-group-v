import cv2
import numpy as np
import time
import os
import HandTrackingModule as htm
from canvas_component import CanvasComponent

def newW():
    # CanvasComponent.test()
    folderPath = "images"
    myList = os.listdir(folderPath)
    print(myList)
    overlayList = []

    for imPath in myList:
        image = cv2.imread(f"{folderPath}/{imPath}")
        # Resize the image to match webcam resolution
        image = cv2.resize(image, (150, 480))
        overlayList.append(image)

    print(len(overlayList))

    brushThickness = 10
    header = overlayList[0]

    # Get the dimensions (height and width) of the overlay image
    overlay_height, overlay_width, _ = header.shape

    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    pTime = 0
    cTime = 0
    lmList = []
    xp, yp = 0, 0
    drawcolor = (0, 0, 0)

    imgCanvas = np.zeros((480, 640, 3), np.uint8)

    detector = htm.handDetector(min_detection_confidence=0.5)
    print(header)
    while True:
        ret, img = cap.read()
        img = cv2.flip(img, 1)

        # 2

        img = detector.findhands(img)
        lmList = detector.findPosition(img, draw=False)

        if len(lmList) != 0:
            # print(lmList)
            x1, y1 = lmList[8][1:]
            x2, y2 = lmList[12][1:]
        # 3

            fingers = detector.fingerUp()
            # print(fingers)
        # 4
            if fingers[1] and fingers[2]:
                # print(x1)
                if x1 < 150:
                    # print(y1)
                    if 0 < y1 < 60:
                        header = overlayList[0]
                        drawcolor = (200, 200, 0)
                        overlay_height, overlay_width, _ = header.shape
                        print("you are on pen")

                    elif 80 < y1 < 120:
                        header = overlayList[1]
                        drawcolor = (0, 0, 255)
                        overlay_height, overlay_width, _ = header.shape
                        print("you are on brush")

                    elif 130 < y1 < 190:
                        header = overlayList[2]
                        drawcolor = (255, 0, 0)
                        overlay_height, overlay_width, _ = header.shape
                        print("you are on brush")

                    elif 200 < y1 < 260:
                        header = overlayList[3]
                        drawcolor = (0, 255, 0)
                        overlay_height, overlay_width, _ = header.shape
                        print("you are on brush")

                    elif 280 < y1 < 330:
                        header = overlayList[4]
                        drawcolor = (0, 0, 0)
                        overlay_height, overlay_width, _ = header.shape
                        print("you are on brush")

                cv2.rectangle(img, (x1, y1-15), (x2, y2+15),
                              drawcolor, cv2.FILLED)
                xp, yp = x1, y1
                # pr
                # print("selection Mode")
        # 5
            elif fingers[1] and fingers[2] == False:
                cv2.circle(img, (x1, y1), 15, drawcolor, cv2.FILLED)
                if xp == 0 and yp == 0:
                    xp, yp = x1, y1
                if drawcolor == (0, 0, 0):
                    cv2.line(img, (xp, yp), (x1, y1), drawcolor, 30)
                    cv2.line(imgCanvas, (xp, yp), (x1, y1), drawcolor, 30)
                else:
                    cv2.line(img, (xp, yp), (x1, y1),
                             drawcolor, brushThickness)
                    cv2.line(imgCanvas, (xp, yp), (x1, y1),
                             drawcolor, brushThickness)
            # elif
                xp, yp = x1, y1
                print("Drawing Mode")

        imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
        _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
        imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
        img = cv2.bitwise_and(img, imgInv)
        img = cv2.bitwise_or(img, imgCanvas)

        # Overlay the resized image on the webcam frame
        # img[0:720, 0:150] = header
        # img = cv2.addWeighted(img,0.5,imgCanvas,0.5,0)
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.resize(imgCanvas, (img.shape[1], img.shape[0]))
        img[0:720, 0:150] = header

        print(imgCanvas.shape, img.shape)

        if imgCanvas.shape == img.shape:
            img = cv2.addWeighted(img, 0.5, imgCanvas, 0.5, 0)
        else:
            print("Dimensions of img and imgCanvas do not match!")

        cv2.putText(img, str(int(fps)), (10, 70),
                    cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 3)
        cv2.imshow("Camera", img)
        cv2.imshow("canva", imgCanvas)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            # CanvasComponent.resolve(img)
            break
    cap.release()
    cv2.destroyAllWindows()
