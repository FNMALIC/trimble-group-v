
import cv2
import time
import mediapipe as mp


class faceDetection:
    def __init__(self, minconf=0.5) -> None:
        self.minconf = minconf
        self.mpDraw = mp.solutions.drawing_utils
        self.mpFaceDetection = mp.solutions.face_detection
        self.faceDetection = self.mpFaceDetection.FaceDetection(self.minconf)

    def findFace(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.faceDetection.process(imgRGB)

        bboxs = []

        if (self.results.detections):
            # print(results.pose_landmarks)

            #     mpDraw.draw_landmarks(img, results.pose_landmarks,mpPose.POSE_CONNECTIONS)

            for id, detection in enumerate(self.results.detections):
                # mpDraw.draw_detection(img,detection)
                # print(id,detections )
                # print(id,detections.score)
                # print(id,detection.location_data.relative_bounding_box)

                bboxC = detection.location_data.relative_bounding_box
                ih, iw, ic = img.shape
                bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                    int(bboxC.width * iw), int(bboxC.height * ih)
                bboxs.append([id, bbox, detection.score])
                # img = self.fancyDraw(img,bbox)
                # img = self.blurFace(img, bbox)
                if draw:
                    img = self.fancyDraw(img, bbox)
                    cv2.putText(img, str(int(
                        detection.score[0] * 100)), (bbox[0], bbox[1]-20), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 2)
        return img, bboxs

    def fancyDraw(self, img, bbox, l=30, t=10):
        x, y, w, h = bbox
        x1, y2 = x+w, y+h
        cv2.rectangle(img, bbox, (255, 0, 255, 2), 2)
        cv2.line(img, (x, y), (x+l, y),(255, 0, 255), t)
        return img
    
    
    def blurFace(self, img, bboxs):
        for bbox in bboxs:
            x, y, w, h = bbox[1]
            if 0 <= x < img.shape[1] and 0 <= y < img.shape[0]:
                roi = img[y:y+h, x:x+w]
                if roi.size != 0:
                    blurred_roi = cv2.GaussianBlur(roi, (99, 99), 30)
                    img[y:y+h, x:x+w] = blurred_roi
        return img

def main():
    cap = cv2.VideoCapture(0)
    # pTime = 0
    detector = faceDetection()

    while True:
        success, img = cap.read()

        img, bboxs = detector.findFace(img,draw=False)
        # lmList = detector.getPosition(img)
        # if len(lmList) != 0:
        # print(lmList[4])
        # cv2.circle(img, (lmList[4][1],lmList[4][2]),5,(0,0,255),cv2.FILLED)
        img = detector.blurFace(img, bboxs)

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (70, 50),
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == "__main__":
    main()
