import os
import tkinter as tk
import cv2
import numpy as np
from PIL import Image
from Backend.OTPGenerator import Otp
from Backend.sendMail import SendMail
from Database.MPdatabase import PMPDatabase


class SetupFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.primaryColor = '#4479ff'
        self.backgroundColor = '#000000'
        self.surface1Color = '#121212'
        self.surface2Color = '#212121'
        self.successColor = '#03dac6'
        self.errorColor = '#cf6679'
        self.priTextColor = '#000000'
        self.secTextColor = '#ffffff'
        self.faceregistered = False
        self.entryFont = ("Rockwell", 12)
        self.labelFont = ("Rockwell", 12, "bold")
        self.controller = controller
        otpObj = Otp()
        self.generatedOTP = otpObj.generateOTP()
        self.setupFrame = tk.LabelFrame(self, text="Setup", bg=self.backgroundColor, fg=self.secTextColor)
        self.setupFrame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.titleLabel = tk.Label(self.setupFrame, text='Setup', bg=self.backgroundColor, fg=self.secTextColor,
                                   font=("Rockwell", 18, "bold"))
        self.titleLabel.place(relx=0.25, rely=0.05, relheight=0.1, relwidth=0.5)
        self.emailLabel = tk.Label(self.setupFrame, bd=2, text="Email", bg=self.backgroundColor, fg=self.secTextColor,
                                   font=self.labelFont)
        self.emailLabel.place(relx=0.25, rely=0.15, relwidth=0.5, relheight=0.07)
        self.emailentry = tk.Entry(self.setupFrame, width=20, font=self.entryFont, bg=self.surface1Color,
                                   fg=self.priTextColor)
        self.emailentry.place(relx=0.25, rely=0.21, relwidth=0.5, relheight=0.05)
        self.emailentry.delete(0, 'end')
        self.sendOtpButton = tk.Button(self.setupFrame, text="Send OTP", command=self.sendOtp, bg=self.primaryColor,
                                       fg=self.secTextColor, font=self.labelFont)
        self.sendOtpButton.place(relx=0.35, rely=0.28, relwidth=0.3, relheight=0.07)
        self.otpLabel = tk.Label(self.setupFrame, bd=2, text="OTP", bg=self.backgroundColor, fg=self.secTextColor,
                                 font=self.labelFont)
        self.otpLabel.place(relx=0.25, rely=0.36, relwidth=0.5, relheight=0.07)
        self.otpentry = tk.Entry(self.setupFrame, width=20, font=self.entryFont, bg=self.surface1Color,
                                 fg=self.priTextColor)
        self.otpentry.place(relx=0.25, rely=0.425, relwidth=0.5, relheight=0.05)
        self.otpentry.delete(0, 'end')
        self.otpEnterButton = tk.Button(self.setupFrame, text="Check OTP", command=lambda: [self.checkOTP()],
                                        font=self.labelFont, bg=self.primaryColor, fg=self.secTextColor)
        self.otpEnterButton.place(relx=0.35, rely=0.50, relwidth=0.3, relheight=0.06)
        self.faceButton = tk.Button(self.setupFrame, bd=2, font=self.labelFont, text="Register Faceprint",
                                    command=lambda: self.insertFace(),  bg=self.primaryColor, fg=self.secTextColor)
        self.faceButton.place(relx=0.25, rely=0.60, relwidth=0.5, relheight=0.07)
        self.passLabel = tk.Label(self.setupFrame, text="Master Password", font=self.labelFont, bg=self.backgroundColor,
                                  fg=self.secTextColor)
        self.passLabel.place(relx=0.25, rely=0.68, relwidth=0.5, relheight=0.07)
        self.passentry = tk.Entry(self.setupFrame, show="*", width=20, bd=2, font=self.entryFont, bg=self.surface1Color,
                                  fg=self.priTextColor)
        self.passentry.place(relx=0.25, rely=0.75, relwidth=0.5, relheight=0.05)
        self.passentry.delete(0, 'end')
        self.enter = tk.Button(self.setupFrame, text="Enter", bg=self.primaryColor, fg=self.secTextColor,
                               font=self.labelFont, command=lambda: [self.insertPass(self.checkOTP())])
        self.enter.place(relx=0.35, rely=0.82, relwidth=0.3, relheight=0.07)

    def insertFace(self):
        try:
            self.record_faces()
            self.recognize_face()


        except Exception as e:
            errorInsertLabel = tk.Label(self.setupFrame, text=str(e), bg=self.errorColor,
                                        fg=self.priTextColor, font=self.labelFont)
            errorInsertLabel.place(relx=0.16, rely=0.02, relwidth=0.7, relheight=0.05)
            errorInsertLabel.after(2000, errorInsertLabel.destroy)

    def record_faces(self):
        try:
            if not os.path.exists('Database/training-data'):
                os.makedirs('Database/training-data')
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
            cap = cv2.VideoCapture(0)
            sampleNum = 0
            while True:
                ret, img = cap.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    sampleNum = sampleNum + 1
                    cv2.imwrite("Database/training-data/User.1." + str(sampleNum) + ".jpg",
                                gray[y:y + h, x:x + w])
                    cv2.waitKey(10)
                cv2.waitKey(1)
                if sampleNum > 20:
                    break
            cap.release()
            cv2.destroyAllWindows()

        except Exception as e:
            errorLabel = tk.Label(self.setupFrame, text="Error! Try again!!\n"+e+"", font=self.labelFont,
                                  bg=self.errorColor, fg=self.priTextColor)
            errorLabel.place(relx=0.16, rely=0.02, relwidth=0.7, relheight=0.05)
            errorLabel.after(2000, errorLabel.destroy)

    def recognize_face(self):
        try:
            recognizer = cv2.face.LBPHFaceRecognizer_create()
            path = 'Database/training-data'
            if not os.path.exists('Database/recognizer'):
                os.makedirs('Database/recognizer')

            def getImagesWithID(path):
                imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
                faces = []
                IDs = []
                for imagePath in imagePaths:
                    faceImg = Image.open(imagePath).convert("L")
                    faceNp = np.array(faceImg, 'uint8')
                    ID = int(os.path.split(imagePath)[-1].split('.')[1])
                    faces.append(faceNp)
                    IDs.append(ID)
                    cv2.waitKey(10)
                return np.array(IDs), faces
            Ids, faces = getImagesWithID(path)
            recognizer.train(faces, Ids)
            recognizer.save('Database/recognizer/trainingData.yml')
            import shutil
            shutil.rmtree("Database/training-data")
            self.faceregistered = True
            cv2.destroyAllWindows()
            errorLabel = tk.Label(self.setupFrame, text="Thank you for registering!!", font=self.labelFont,
                                  bg=self.successColor, fg=self.priTextColor)
            errorLabel.place(relx=0.16, rely=0.02, relwidth=0.7, relheight=0.05)
            errorLabel.after(2000, errorLabel.destroy)
        except Exception as e:
            errorLabel = tk.Label(self.setupFrame, text="Error! Try again!!\n"+e+"", font=self.labelFont,
                                  bg=self.errorColor, fg=self.priTextColor)
            errorLabel.place(relx=0.16, rely=0.02, relwidth=0.7, relheight=0.05)
            errorLabel.after(2000, errorLabel.destroy)

    def insertPass(self, otpStatus):
        from Frames.loginFrame import LoginFrame
        try:
            db = PMPDatabase()
            em = self.emailentry.get()
            mp = self.passentry.get()
            if otpStatus & self.faceregistered:
                db.insertIntoTable(mp, em)
                confirmInsertLabel = tk.Label(self.setupFrame, text="Successful", bg=self.successColor,
                                              fg=self.priTextColor, font=self.labelFont)
                confirmInsertLabel.place(relx=0.16, rely=0.02, relwidth=0.7, relheight=0.05)
                confirmInsertLabel.after(2000, confirmInsertLabel.destroy)
                self.controller.show_frame(LoginFrame)
            else:
                errorInsertLabel = tk.Label(self.setupFrame, text="Try again!", bg=self.errorColor,
                                            fg=self.priTextColor, font=self.labelFont)
                errorInsertLabel.place(relx=0.16, rely=0.02, relwidth=0.7, relheight=0.05)
                errorInsertLabel.after(2000, errorInsertLabel.destroy)
                self.emailentry.delete(0, 'end')
                self.passentry.delete(0, 'end')
                self.otpentry.delete(0, 'end')
        except:
            errorInsertLabel = tk.Label(self.setupFrame, text="Database Error Try again", bg=self.errorColor,
                                        fg=self.priTextColor, font=self.labelFont)
            errorInsertLabel.place(relx=0.16, rely=0.02, relwidth=0.7, relheight=0.05)
            errorInsertLabel.after(2000, errorInsertLabel.destroy)
        finally:
            self.emailentry.delete(0, 'end')
            self.passentry.delete(0, 'end')
            self.otpentry.delete(0, 'end')

    def checkOTP(self):
        enteredOTP = self.otpentry.get()
        if enteredOTP == self.generatedOTP:
            confirmOtpLabel = tk.Label(self.setupFrame, text="OTP Correct", bg=self.successColor, fg=self.priTextColor,
                                       font=self.labelFont)
            confirmOtpLabel.place(relx=0.16, rely=0.02, relwidth=0.7, relheight=0.05)
            confirmOtpLabel.after(2000, confirmOtpLabel.destroy)
            return True
        else:
            wrongOtpLabel = tk.Label(self.setupFrame, text="OTP Incorrect", bg=self.errorColor, fg=self.priTextColor,
                                     font=self.labelFont)
            wrongOtpLabel.place(relx=0.16, rely=0.02, relwidth=0.7, relheight=0.05)
            wrongOtpLabel.after(2000, wrongOtpLabel.destroy)
            return False

    def sendOtp(self):
        try:
            subject = 'PasswordManager: Registering of a new account'
            message = "Dear customer,\n\tThank you for using our product. Your OTP for Password Manager is:\t" + \
                      str(self.generatedOTP) + "\nDo not disclose this to anyone and delete the message after " \
                                               "use. If OTP not requested by you, ignore this mail. \n\nThank you. "
            SendMail().send(str(self.emailentry.get()), subject, message)
            mailLabel = tk.Label(self.setupFrame, text="Otp Sent Successfully", font=self.labelFont, bg=self.successColor,
                                 fg=self.priTextColor)
            mailLabel.place(relx=0.16, rely=0.02, relwidth=0.7, relheight=0.05)
            mailLabel.after(6000, mailLabel.destroy())
        except:
            mailErrorLabel = tk.Label(self.setupFrame, text="OTP NOT SENT !!", font=self.labelFont,
                                      bg=self.errorColor, fg=self.priTextColor)
            mailErrorLabel.place(relx=0.16, rely=0.02, relwidth=0.7, relheight=0.05)
            mailErrorLabel.after(6000, mailErrorLabel.destroy())
