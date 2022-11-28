import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

path = 'student_images'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)

def findEncodings(images):
    encodeList =[]
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def mail(em,nm):
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    
    smtp.starttls()
    smtp.login('guthysaiteja1904@gmail.com', 'ewvaizuykookuicq')
    
    def message(subject="",text=""):
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg.attach(MIMEText(text))
        return msg
    
    msg = message("Attendance", f"""Dear Parent,
Your child {nm} has not attended the class today. Please send a letter, email or phone call explaining the reason for absence.""")
    
    
    smtp.sendmail(from_addr="guthysaiteja1904@gmail.com",to_addrs=em, msg=msg.as_string())
    print("\nMail sent successfully!")
    smtp.quit()
    
def markAttendance(names):
    with open('Attendance.csv', 'r+') as f:
        students=['SAI','MODI-IMAGE-FOR-INUTH.jpg','NARENDRA-MODI','SNEHU','VIVEK','SUMA','ravi','abhi','gireesh','saikrishna']
        rollnums=['19010101','19010102','19010103','19010104','19010105','19010106','19010107','19010108','19010109','19010110']
        emails=['gootysaiteja@gmail.com','xyz@gmail.com','xyz@gmail.com','xyz@gmail.com','xyz@gmail.com','xyz@gmail.com','xyz@gmail.com','xyz@gmail.com','xyz@gmail.com','xyz@gmail.com']
        absent=[]
        f.writelines(f'\n{"Name"},{"RollNumber"},{"Attendance"},{"Time"},{"Date"}')
        for i in range(len(students)):
            time_now = datetime.now()
            tString = time_now.strftime('%H:%M:%S')
            dString = time_now.strftime('%d/%m/%Y')
            if students[i] in names:
                f.writelines(f'\n{students[i]},{rollnums[i]},{"Present"},{tString},{dString}')
            else:
                absent.append(rollnums[i][-3:])
                f.writelines(f'\n{students[i]},{rollnums[i]},{"Absent"},{tString},{dString}')
        print("\nabsentees list : \n")
        for j in absent:
            print(j)
        c=input("\nDo you want to make any changes(y/n) : ")
        if c=="y" or c=="Y":
            s=input("\nEnter the roll numbers you want to remove from the list : ")
            k=s.split(" ")
            for i in k:
                absent.remove(i)
        else:
            quit()
        print("\nabsentees list : \n")
        for j in absent:
            print(j)
        for i in absent:
            for j in rollnums:
                if i==j[-3:]:
                    mail(emails[rollnums.index(j)],students[rollnums.index(j)])
                    break
        print()  
encodeListKnown = findEncodings(images)
print('Encoding Complete')

cap = cv2.VideoCapture(0)

names=[]


while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        print(faceDis)
        matchIndex = np.argmin(faceDis)
        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            print(name)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 250, 0), cv2.FILLED)
            cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            if name not in names:
                names.append(name)
    cv2.imshow('webcam', img)
    if cv2.waitKey(10) == 13:
        break
cap.release()
cv2.destroyAllWindows()
markAttendance(names)
