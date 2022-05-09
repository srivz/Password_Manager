import tkinter as tk
from Database.MPdatabase import PMPDatabase
from Backend.OTPGenerator import Otp
from Backend.sendMail import SendMail
from Frames.settingsFrame import SettingsFrame


class SettingChangeFrame(tk.Frame):
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
        otpObj = Otp()
        self.generatedOTP = otpObj.generateOTP()
        self.settingChangeFrame = tk.LabelFrame(self, text="Settings", bd=5, bg=self.backgroundColor,
                                                fg=self.secTextColor)
        self.settingChangeFrame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.confirmLabel = tk.Label(self.settingChangeFrame, text="Email Sent", bg=self.successColor,
                                     fg=self.priTextColor, font=self.labelFont)
        self.titleLabel = tk.Label(self.settingChangeFrame, text='Authentication for Settings', bg=self.backgroundColor,
                                   fg=self.primaryColor, font=("Rockwell", 18, "bold"))
        self.titleLabel.place(relx=0.25, rely=0.15, relheight=0.1, relwidth=0.5)
        self.emailLabel = tk.Label(self.settingChangeFrame, text='Enter registered email id',
                                   bg=self.backgroundColor, fg=self.secTextColor, font=self.labelFont)
        self.emailLabel.place(relx=0.25, rely=0.32, relheight=0.07, relwidth=0.5)
        self.emailentry = tk.Entry(self.settingChangeFrame, width=20, font=self.entryFont, bg=self.surface1Color,
                                   fg=self.secTextColor)
        self.emailentry.place(relx=0.25, rely=0.38, relwidth=0.5, relheight=0.05)
        self.emailentry.insert(0, "Enter your Email")
        self.emailentry.focus()
        self.emailentry.delete(0, 'end')
        self.sendOtpButton = tk.Button(self.settingChangeFrame, text="Send OTP", command=self.sendOtp,
                                       font=self.labelFont,
                                       bg=self.primaryColor, fg=self.secTextColor)
        self.sendOtpButton.place(relx=0.35, rely=0.45, relwidth=0.3, relheight=0.07)
        self.otpLabel = tk.Label(self.settingChangeFrame, text='Enter Otp', bg=self.backgroundColor,
                                 fg=self.secTextColor,
                                 font=self.labelFont)
        self.otpLabel.place(relx=0.25, rely=0.56, relheight=0.07, relwidth=0.5)
        self.otpentry = tk.Entry(self.settingChangeFrame, width=20, font=self.entryFont, bg=self.surface1Color,
                                 fg=self.secTextColor)
        self.otpentry.place(relx=0.25, rely=0.62, relwidth=0.5, relheight=0.05)
        self.otpentry.bind("<Return>", self.shortcuts)
        self.otpentry.delete(0, 'end')
        self.otpEnterButton = tk.Button(self.settingChangeFrame, text="Enter",
                                        command=lambda: [self.checkOTP(), self.emailentry.delete(0, 'end'),
                                                         self.otpentry.delete(0, 'end')], font=self.labelFont,
                                        bg=self.primaryColor, fg=self.secTextColor)
        self.otpEnterButton.place(relx=0.35, rely=0.7, relwidth=0.3, relheight=0.07)
        self.backButton = tk.Button(self.settingChangeFrame, text="Back",
                                    command=lambda: [self.emailentry.delete(0, 'end'), self.otpentry.delete(0, 'end'),
                                                     controller.show_frame(HomeFrame)], bg=self.surface2Color,
                                    fg=self.secTextColor)
        self.backButton.place(relx=0.4, rely=0.8, relwidth=0.2, relheight=0.05)

    def checkOTP(self):
        enteredOTP = self.otpentry.get()
        if enteredOTP == self.generatedOTP:
            self.controller.show_frame(SettingsFrame)
        else:
            errorLabel = tk.Label(self.settingChangeFrame, text="OTP incorrect", bg=self.errorColor,
                                  fg=self.priTextColor, font=self.labelFont)
            errorLabel.place(relx=0.16, rely=0.02, relwidth=0.7, relheight=0.05)
            errorLabel.after(2000, errorLabel.destroy)

    def sendOtp(self):
        mail = self.emailentry.get()
        pdb = PMPDatabase()
        if not (pdb.mailCheck(mail)):
            errorLabel = tk.Label(self.settingChangeFrame, text="Wrong Email entered", bg=self.errorColor,
                                  fg=self.priTextColor, font=self.labelFont)
            errorLabel.place(relx=0.16, rely=0.02, relwidth=0.7, relheight=0.05)
            errorLabel.after(3000, errorLabel.destroy)
            return

        mail = SendMail()
        subject = 'PasswordManager: Accessing the Settings'
        message = "Hello Dear Customer,\n\tWe received a request to access settings. Your OTP for accessing settings " \
                  "in Password Manager is:\t" + str(self.generatedOTP) + "\n\nIf you did not access your password " \
                                                                         "manager settings you can safely delete and " \
                                                                         "ignore this mail.\n\nThankyou. "
        mail.send((self.emailentry.get()), subject, message)

        self.confirmLabel.place(relx=0.16, rely=0.02, relwidth=0.7, relheight=0.05)
        self.confirmLabel.after(3000, self.confirmLabel.destroy())

    def shortcuts(self, event):
        key = event.char
        if key == '\r':
            self.sendOtp()
