import cv2
import mediapipe as mp
import time



class handDetector():
    def __init__(self, static_image_mode=False,
               max_num_hands=2,
               model_complexity=1,
               min_detection_confidence=0.5,
               min_tracking_confidence=0.5):  
        self.static_image_mode = static_image_mode
        self.max_num_hands = max_num_hands
        self.model_complexity = model_complexity
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands( self.static_image_mode,self.max_num_hands,self.model_complexity,self.min_detection_confidence,self.min_tracking_confidence)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4,8,12,16,20]

    def findhands(self,img,draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img,handLms, self.mpHands.HAND_CONNECTIONS)
        # print(results)
        return img

    def findPosition(self ,img , handNo=0, draw= True):
        self.lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id,lm in enumerate(myHand.landmark):
                # print(id,lm)
                h,w,c = img.shape
                cx ,cy = int(lm.x*w),int(lm.y*h)
                # print(id,cx,cy)
                self.lmList.append([id,cx,cy])
                if draw:
                    cv2.circle(img,(cx,cy),5,(255,0,255),cv2.FILLED)
        return self.lmList
    
    def fingerUp(self):
        fingers = []

        if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        for id in range(1,5):
            # print(self.lmList[self.tipIds[id]])
            
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers

def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    # if not cap.isOpened():
    #     print("Error: Cannot open camera.")
    #     return
    # while True:
    #     ret, img = cap.read()
    #     # if not ret:
    #     #     print("Error: Failed to receive frame.")
    #     #     break

    #     # img = detector.findhands(img=img)
    #     # lmList = detector.findPosition(img)
    #     # if len(lmList) != 0:
    #         # print(lmList[4])

    #     # cTime = time.time()
    #     # fps = 1/(cTime - pTime)
    #     # pTime=cTime
    #     # cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,1,(255,0,255),3)
    #     cv2.imshow("Camera", img)

    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break


    #     cap.release()
    #     cv2.destroyAllWindows()
    # cap = cv2.VideoCapture(0)  # Open default camera
    while True:
        ret, img = cap.read()

        img = detector.findhands(img=img)
        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            print(lmList[4])
        cv2.imshow("Camera", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()