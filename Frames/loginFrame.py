import os
import tkinter as tk
import cv2
from Database.MPdatabase import PMPDatabase
from Frames.forgotPassFrame import ForgotPassFrame
from Frames import OtpSettings


class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.pw = False
        self.primaryColor = '#4479ff'
        self.backgroundColor = '#000000'
        self.surface1Color = '#121212'
        self.surface2Color = '#212121'
        self.successColor = '#03dac6'
        self.errorColor = '#cf6679'
        self.priTextColor = '#000000'
        self.secTextColor = '#ffffff'
        self.labelFont = ("Rockwell", 12, "bold")
        self.entryFont = ("Rockwell", 16)
        self.controller = controller
        self.loginFrame = tk.LabelFrame(self, text="Login", bd=5, bg=self.backgroundColor, fg=self.secTextColor)
        self.loginFrame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.titleLabel = tk.Label(self.loginFrame, text='Password Manager', bg=self.backgroundColor,
                                   fg=self.primaryColor, font=("Rockwell", 20, "bold"))
        self.titleLabel.place(relx=0.25, rely=0.2, relheight=0.1, relwidth=0.5)
        self.epassLabel = tk.Label(self.loginFrame, text='Enter password', bg=self.backgroundColor,
                                   fg=self.secTextColor, font=self.labelFont)
        self.epassLabel.place(relx=0.35, rely=0.37, relheight=0.07, relwidth=0.3)
        self.mpassentry = tk.Entry(self.loginFrame, show="*", width=20, font=self.entryFont, bg=self.surface1Color,
                                   fg=self.primaryColor)
        self.mpassentry.place(relx=0.25, rely=0.45, relwidth=0.5, relheight=0.07)
        self.mpassentry.bind("<Return>", self.shortcuts)
        self.mpassentry.delete(0, 'end')
        self.faceLock = tk.Button(self.loginFrame, text="Check Face", bg=self.primaryColor, fg=self.secTextColor,
                                  command=lambda: self.faceLockCheck(), font=self.labelFont)
        self.faceLock.place(relx=0.35, rely=0.8, relwidth=0.3, relheight=0.07)
        self.mpassenter = tk.Button(self.loginFrame, text="Login", bg=self.primaryColor, fg=self.secTextColor,
                                    command=lambda: self.checkPass(), font=self.labelFont)
        self.mpassenter.place(relx=0.35, rely=0.6, relwidth=0.3, relheight=0.07)
        self.forgotPass = tk.Button(self.loginFrame, text="Forgot Password", bg=self.surface2Color,
                                    fg=self.secTextColor, command=lambda: controller.show_frame(ForgotPassFrame))
        self.forgotPass.place(relx=0.4, rely=0.7, relwidth=0.2, relheight=0.05)

    def shortcuts(self, event):
        key = event.char
        if key == '\r':
            self.checkPass()

    def checkPass(self):
        mp = self.mpassentry.get()
        pdb = PMPDatabase()
        if pdb.loginCheck(mp):
            confirmLabel = tk.Label(self.loginFrame, text="Password Correct! Check face now.", font=self.labelFont,
                                    bg=self.successColor,
                                    fg=self.priTextColor)
            confirmLabel.place(relx=0.16, rely=0.02, relwidth=0.7, relheight=0.05)
            confirmLabel.after(2000, confirmLabel.destroy)
            self.mpassentry.delete(0, 'end')
            self.pw = True
            return
        errorLabel = tk.Label(self.loginFrame, text="Wrong Password... try again!", font=self.labelFont,
                              bg=self.errorColor, fg=self.priTextColor)
        errorLabel.place(relx=0.16, rely=0.02, relwidth=0.7, relheight=0.05)
        errorLabel.after(2000, errorLabel.destroy)

    def faceLockCheck(self):
        def check_face():
            try:
                fname = "Database/recognizer/trainingData.yml"
                if not os.path.isfile(fname):
                    errorLabel = tk.Label(self.loginFrame, text="Please register your face first in the settings",
                                          font=self.labelFont, bg=self.errorColor, fg=self.priTextColor)
                    errorLabel.place(relx=0.16, rely=0.02, relwidth=0.7, relheight=0.05)
                    errorLabel.after(6000, errorLabel.destroy)
                face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                cap = cv2.VideoCapture(0)
                recognizer = cv2.face.LBPHFaceRecognizer_create()
                recognizer.read(fname)
                flag = True
                while flag:
                    ret, img = cap.read()
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                    for (x, y, w, h) in faces:
                        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
                        ids, conf = recognizer.predict(gray[y:y + h, x:x + w])
                        if conf < 50:
                            return "User"
                        else:
                            flag = False
                cap.release()
                cv2.destroyAllWindows()
            except Exception as e:
                errorLabel = tk.Label(self.loginFrame, text="Error! Try again!!\n" + e + "", font=self.labelFont,
                                      bg=self.errorColor, fg=self.priTextColor)
                errorLabel.place(relx=0.16, rely=0.02, relwidth=0.7, relheight=0.05)
                errorLabel.after(2000, errorLabel.destroy)

        x = check_face()
        if (x == "User") & self.pw:
            if OtpSettings.configure:
                from Frames.loginVerificationFrame import LoginVerificationFrame
                self.controller.show_frame(LoginVerificationFrame)
            else:
                from Frames.homeFrame import HomeFrame
                self.controller.show_frame(HomeFrame)
