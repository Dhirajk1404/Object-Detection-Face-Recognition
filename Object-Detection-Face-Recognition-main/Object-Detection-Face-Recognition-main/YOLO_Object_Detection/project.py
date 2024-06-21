import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

while (True):
    print("""ENTER YOUR OPTION --- 
          1.object Detection
          2.Face Recognition
          3.Exit
          """)
    abc = int(input("enter your choice"))
    if abc == 1:
        cap = cv2.VideoCapture(0)

        # url="https://10.200.30.105:8080/video"
        # cap.open(url)#0 for 1st webcam
        font = cv2.FONT_HERSHEY_PLAIN
        starting_time = time.time()
        frame_id = 0

        while True:
            _, frame = cap.read()  #
            frame_id += 1

            height, width, channels = frame.shape
            # detecting objects
            blob = cv2.dnn.blobFromImage(frame, 0.00392, (320, 320), (0, 0, 0), True,
                                         crop=False)  # reduce 416 to 320

            net.setInput(blob)
            outs = net.forward(output_layer_name)
            # print(outs[1])

            # Showing info on screen/ get confidence score of algorithm in detecting an object in blob
            class_ids = []
            confidences = []
            boxes = []
            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > 0.3:
                        # onject detected
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)

                        # cv2.circle(img,(center_x,center_y),10,(0,255,0),2)
                        # rectangle co-ordinaters
                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)
                        # cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

                        boxes.append([x, y, w, h])  # put all rectangle areas
                        confidences.append(
                            float(confidence))  # how confidence was that object detected and show that percentage
                        class_ids.append(class_id)  # name of the object tha was detected

            indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.4, 0.6)

            for i in range(len(boxes)):
                if i in indexes:
                    x, y, w, h = boxes[i]
                    label = str(classes[class_ids[i]])
                    confidence = confidences[i]
                    color = colors[class_ids[i]]
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(frame, label + " " + str(round(confidence, 2)), (x, y + 30), font, 1, (255, 255, 255),
                                2)
                    print(label)

            elapsed_time = time.time() - starting_time
            fps = frame_id / elapsed_time
            cv2.putText(frame, "FPS:" + str(round(fps, 2)), (10, 50), font, 2, (0, 0, 0), 1)

            cv2.imshow("Image", frame)
            key = cv2.waitKey(1)  # wait 1ms the loop will start again and we will process the next frame

            if key == 27:  # esc key stops the process
                break;

        cap.release()
        cv2.destroyAllWindows()

        #     if(abc==2):
        #         path='imageAttendence/'
        #         images=[]
        #         classNames=[]
        #         mylist=os.listdir(path)
        #         #print(mylist)
        #         for cl in mylist:
        #             curImg=cv2.imread(f'{path}/{cl}')
        #             images.append(curImg)
        #             classNames.append(os.path.splitext(cl)[0])

        #         print("####IMAGEPROCESSING####")
        #         #print(images)
        #         def findEncoding(images):
        #             encodeList=[]
        #             for img in images:
        #                 img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        #                 encode=face_recognition.face_encodings(img)
        #                 encodeList.append(encode)
        #             return encodeList

        #         def markAttendence(name):
        #             with open('attendence.csv','r+') as f:
        #                 mydatalist=f.readlines()
        #                 nameList = []
        #                 for line in mydatalist:
        #                     entry = line.split(',')
        #                     nameList.append(entry[0])
        #                 if name not in nameList:
        #                     now = datetime.now()
        #                     date_string = now.strftime('%H:%M:%S')
        #                     f.writelines(f'\n{name},{date_string}')

        #         encodeListKnown=findEncoding(images)
        #         print('Encoding Completed !!!')

        #         cam=cv2.VideoCapture(0)
        #         #url="http://10.200.30.105:8080/video"
        #         #cam.open(url)

        #         while True:
        #             success , img = cam.read()
        #             if img is not None:
        #                 cv2.imshow('frame',img)

        #                 imgS=cv2.resize(img,(0,0),None,0.25,0.25)
        #                 imgS=cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)

        #                 FaceCurFrame = face_recognition.face_locations(imgS)
        #                 encodeCurFrame=face_recognition.face_encodings(imgS,FaceCurFrame)

        #             for encodeface , faceloc in zip(encodeCurFrame,FaceCurFrame):
        #                 matches=face_recognition.compare_faces(encodeListKnown,encodeface)
        #                 FaceDis=face_recognition.face_distance(encodeListKnown,encodeface)
        #         #print(FaceDis)

        #                 matchesIndex = np.argmin(FaceDis)

        #                 if matches[matchesIndex]:
        #                     name = classNames[matchesIndex].upper()
        #                     print("Face Detected")
        #             #print(name)

        #                     y1,x2,y2,x1=faceloc
        #                     y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4
        #                     cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
        #                     cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
        #                     cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
        #                     markAttendence(name)
        #                     cv2.imshow('Webcam',img)
        #             if cv2.waitKey(1)==ord('q'):

        #                 break
        #                 cv2.destroyAllWindows()

        cv2.waitKey(1)
    if abc == 3:
        print("THANK YOU !!!")
        break
    else:
        print("type correct option")