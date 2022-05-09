import tkinter as tk

from Database.MPdatabase import PMPDatabase
from Database.PDatabase import siteData
from Backend.encryption import EncryptDeCrypt
from Frames.addPassFrame import AddPassFrame
from Frames.forgotPassFrame import ForgotPassFrame
from Frames.homeFrame import HomeFrame
from Frames.loginFrame import LoginFrame
from Frames.loginVerificationFrame import LoginVerificationFrame
from Frames.resetPassFrame import ResetPassFrame
from Frames.searchPassFrame import SearchPassFrame
from Frames.settingChangeFrame import SettingChangeFrame
from Frames.settingsFrame import SettingsFrame
from Frames.setupFrame import SetupFrame

database = PMPDatabase()
database.createTable()
Pdb = siteData()
Pdb.createDataTable()
en = EncryptDeCrypt()
en.generate_key()


class PasswordManagerApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.geometry(self, '650x600+450+120')
        tk.Tk.resizable(self, width=False, height=False)
        pwmLogo = tk.PhotoImage(file="img/logo.png")
        pwmLogo = (pwmLogo.zoom(25)).subsample(32)
        tk.Tk.iconphoto(self, True, pwmLogo)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        for F in (
                LoginFrame, ForgotPassFrame, SetupFrame, SettingsFrame, SettingChangeFrame, ResetPassFrame, HomeFrame,
                SearchPassFrame, AddPassFrame, LoginVerificationFrame):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        if database.isEmpty():
            self.show_frame(SetupFrame)
        elif not database.isEmpty():
            self.show_frame(LoginFrame)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
