import tkinter as tk
import os
import cv2
import numpy as np
from PIL import Image

class SettingsFrame(tk.Frame):
    def __init__(self, parent, controller):
        from Frames.homeFrame import HomeFrame
        tk.Frame.__init__(self, parent)
        self.primaryColor = '#4479ff'
        self.backgroundColor = '#000000'
        self.surface1Color = '#121212'
        self.surface2Color = '#212121'
        self.successColor = '#03dac6'
        self.errorColor = '#cf6679'
        self.priTextColor = '#000000'
        self.secTextColor = '#ffffff'
        self.entryFont = ("Rockwell", 12)
        self.labelFont = ("Rockwell", 12, "bold")
        self.controller = controller
        self.settingsFrame = tk.LabelFrame(self, text="Settings", bd=5, bg=self.backgroundColor,
                                           fg=self.secTextColor)
        self.settingsFrame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.titleLabel = tk.Label(self.settingsFrame, text='Settings', bg=self.backgroundColor,
                                   fg=self.primaryColor, font=("Rockwell", 18, "bold"))
        self.titleLabel.place(relx=0.25, rely=0.15, relheight=0.1, relwidth=0.5)
        self.faceEntry = tk.Button(self.settingsFrame, text='Change Faceprint',
                                   command=lambda: self.faceLock(), bg=self.surface1Color,
                                   fg=self.secTextColor)
        self.faceEntry.place(relx=0.25, rely=0.30, relwidth=0.5, relheight=0.05)
        self.backupEntry = tk.Button(self.settingsFrame, text='Upload Backup files',
                                     command=lambda: self.uploadBackUp(), bg=self.surface1Color,
                                     fg=self.secTextColor)
        self.backupEntry.place(relx=0.25, rely=0.40, relwidth=0.5, relheight=0.05)
        self.deleteAccount = tk.Button(self.settingsFrame, text='Delete Account',
                                       command=lambda: self.deleteMail(), bg=self.surface1Color,
                                       fg=self.secTextColor)
        self.deleteAccount.place(relx=0.25, rely=0.50, relwidth=0.5, relheight=0.05)

        self.backUp = tk.Button(self.settingsFrame, text='Get BackUp',
                                command=lambda: self.getBackUp(), bg=self.surface1Color,
                                fg=self.secTextColor)
        self.backUp.place(relx=0.25, rely=0.60, relwidth=0.5, relheight=0.05)
        self.otpVerification = tk.Button(self.settingsFrame, text='Switch OTP Verification On',
                                command=lambda: self.setOtpSettings(), bg=self.surface1Color,
                                fg=self.secTextColor)
        self.otpVerification.place(relx=0.25, rely=0.70, relwidth=0.5, relheight=0.05)
        self.backButton = tk.Button(self.settingsFrame, text="Back",
                                    command=lambda: [controller.show_frame(HomeFrame)], bg=self.surface2Color,
                                    fg=self.secTextColor)
        self.backButton.place(relx=0.4, rely=0.8, relwidth=0.2, relheight=0.05)

    def uploadBackUp(self):
        from tkinter import filedialog
        path = tk.filedialog.askopenfilenames(title="Select data.db file and s.key file")
        import shutil
        files = list(path)
        for f in files:
            shutil.copy(f, 'Database/')

    def getBackUp(self):
        from tkinter import filedialog
        path = tk.filedialog.askdirectory()
        import shutil
        files = ['Database/data.db', 'Database/s.key']
        for f in files:
            shutil.copy(f, path)

    def deleteMail(self):
        f = open("Database/config.db", "w")
        f.write("")
        f.close()
        import shutil
        shutil.rmtree("Database/recognizer")
        shutil.rmtree("Database/training-data")
        from Frames.setupFrame import SetupFrame
        self.controller.show_frame(SetupFrame)
        return

    def faceLock(self):
        try:
            self.record_faces()
            self.recognize_face()


        except Exception as e:
            errorLabel = tk.Label(self.settingsFrame, text="Error! Try again!!\n"+e+"", font=self.labelFont,
                                  bg=self.errorColor, fg=self.priTextColor)
            errorLabel.place(relx=0.16, rely=0.02, relwidth=0.7, relheight=0.05)
            errorLabel.after(2000, errorLabel.destroy)

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
            errorLabel = tk.Label(self.settingsFrame, text="Error! Try again!!\n"+e+"", font=self.labelFont,
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
            cv2.destroyAllWindows()
            errorLabel = tk.Label(self.settingsFrame, text="Faceprint changed!!", font=self.labelFont,
                                  bg=self.successColor, fg=self.priTextColor)
            errorLabel.place(relx=0.16, rely=0.02, relwidth=0.7, relheight=0.05)
            errorLabel.after(2000, errorLabel.destroy)
        except Exception as e:
            errorLabel = tk.Label(self.settingsFrame, text="Error! Try again!!\n"+e+"", font=self.labelFont,
                                  bg=self.errorColor, fg=self.priTextColor)
            errorLabel.place(relx=0.16, rely=0.02, relwidth=0.7, relheight=0.05)
            errorLabel.after(2000, errorLabel.destroy)


    def setOtpSettings(self):
        from Frames import OtpSettings
        if OtpSettings.configure:
            self.otpVerification['text'] = "Switch OTP Verification On"
            OtpSettings.configure = False
        else:
            self.otpVerification['text'] = "Switch OTP Verification Off"
            OtpSettings.configure = True