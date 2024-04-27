import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

# face_recognition install hiihed
# ...Dlib-main>pip install dlib-19.22.99-cp39-cp39-win_amd64.whl
# ...Dlib-main>pip install cmake
# ...Dlib-main>pip install face_recognition

#Zuragnii zam todorhoilno
path = "datas/face's"

#Baij boloh huvisagchiig todorhoilno
images = []
class_Names = []

#Img name
myList = os.listdir(path)

for cl in myList :
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    class_Names.append(os.path.splitext(cl)[0])

def findEncodings (images) :
    encodeList = []
    for img in images :
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList

#tsagaa bvrtguulne
def markAttendance (name) :
    with open('datas/Attendance.csv', 'r+') as f :
        myDataList = f.readlines()
        nameList = []
        for line in myDataList :
            entry = line.split(',')
            nameList.append(entry[0])
            print(entry[0],'====',entry[1])
        if name not in nameList :
            now = datetime.now()
            dtString = now.strftime('%Y/%m/%d %H:%M:%S')
            print(dtString)
            f.writelines(f'\n{name},{dtString}')

def get_period_of_day():
    # Одоогийн цагийг аваарай
    current_hour = datetime.now().hour

    # Define the time ranges for each period of the day
    morning_range = range(6, 12)  # 6:00 AM to 11:59 AM
    afternoon_range = range(12, 18)  # 12:00 PM to 5:59 PM
    evening_range = range(18, 22)  # 6:00 PM to 9:59 PM
    night_range = [*range(22, 24), *range(0, 6)]  # 10:00 PM to 5:59 AM

    # Өдрийн цаг бүрийн цаг хугацааны хязгаарыг тодорхойл
    if current_hour in morning_range:
        return "morning"
    elif current_hour in afternoon_range:
        return "afternoon"
    elif current_hour in evening_range:
        return "evening"
    else:
        return "night"

encodeListKnow = findEncodings(images)

print(myList)
print(class_Names)

print('Complete encode . ')

cap = cv2.VideoCapture(0)

while True :
    success, img = cap.read()
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS,faceCurFrame)

    for encodeFace, faceLog in zip(encodesCurFrame,faceCurFrame) :
        matches = face_recognition.compare_faces(encodeListKnow, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnow, encodeFace)

        print(faceDis)

        matchIndex = np.argmin(faceDis)

        if matches[matchIndex] :
            name = class_Names[matchIndex].upper()
            print(name)

            y1,x2,y2,x1 = faceLog
            y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)

            markAttendance(name)

    cv2.imshow('Webcam',img)
    cv2.waitKey(1)