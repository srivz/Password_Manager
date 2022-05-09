import tkinter as tk
from tkinter import scrolledtext
from Database.PDatabase import siteData
from Frames.addPassFrame import AddPassFrame
from Frames.searchPassFrame import SearchPassFrame
from Frames.settingChangeFrame import SettingChangeFrame


class HomeFrame(tk.Frame):
    def __init__(self, parent, controller):
        from Frames.loginFrame import LoginFrame
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

        self.homeFrame = tk.LabelFrame(self, text="Home", bg=self.backgroundColor, fg=self.secTextColor, bd=5)
        self.homeFrame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.homeBoxFrame = tk.Frame(self.homeFrame, bd=5, bg=self.backgroundColor)
        self.homeBoxFrame.place(relx=0.05, rely=0.025, relwidth=0.8, relheight=0.8)
        self.viewData = scrolledtext.ScrolledText(self.homeBoxFrame, font=self.labelFont, bg=self.surface1Color)
        self.viewData.place(relheight=1, relwidth=1)
        self.refreshBtn = tk.Button(self.homeFrame, text="Refresh", command=self.insertScrolledText,
                                    bg=self.successColor)
        self.refreshBtn.place(relx=0.9, rely=0.045, relwidth=0.08, relheight=0.08)
        self.logoutBtn = tk.Button(self.homeFrame, text="Logout",
                                   command=lambda: [controller.show_frame(LoginFrame)],
                                   bg=self.errorColor)

        self.logoutBtn.place(relx=0.9, rely=0.15, relwidth=0.08, relheight=0.08)
        self.settingsBtn = tk.Button(self.homeFrame, text="Settings", fg=self.secTextColor,
                                     command=lambda: [controller.show_frame(SettingChangeFrame)],
                                     bg=self.surface2Color)

        self.settingsBtn.place(relx=0.9, rely=0.255, relwidth=0.08, relheight=0.08)
        self.newPassBtn = tk.Button(self.homeFrame, text="Add New Password", bg=self.primaryColor, fg=self.secTextColor,
                                    command=lambda: [controller.show_frame(AddPassFrame)], font=self.labelFont)
        self.newPassBtn.place(relx=0.15, rely=0.855, relwidth=0.3, relheight=0.08)
        self.searchPassBtn = tk.Button(self.homeFrame, text="Retrieve Password", bg=self.primaryColor,
                                       fg=self.secTextColor, command=lambda: [controller.show_frame(SearchPassFrame)],
                                       font=self.labelFont)
        self.searchPassBtn.place(relx=0.55, rely=0.855, relwidth=0.3, relheight=0.08)

        self.insertScrolledText()

    def insertScrolledText(self):
        self.viewData.config(state='normal')
        self.viewData.delete(1.0, 'end')
        VObj = siteData()
        allPass = VObj.viewData()
        heading = "SiteName\t|\tUsername\n"
        heading += "-" * 95 + "\n"
        self.viewData.insert('insert', heading, 'head')
        for d in allPass:
            if (d[0]=='') and (d[1]==''):
                continue
            info = "" + d[0] + "\t|\t" + d[1] + "\n"
            info += "-" * 95 + "\n"
            self.viewData.insert('insert', info, 'data')
        self.viewData.tag_config('head', background=self.primaryColor, foreground=self.secTextColor)
        self.viewData.tag_config('data', foreground=self.secTextColor)
        self.viewData.config(state='disabled')
