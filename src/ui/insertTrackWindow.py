import customtkinter as cTkinter

class InsertTrackWindow(cTkinter.CTkToplevel):
    def __init__(self, *args, fg_color = None, **kwargs):
        from ui import uiUtils

        super().__init__(*args, fg_color=fg_color, **kwargs)
        self.geometry("500x400")
        self.title("Cullerian player")

        self.baseTrackPath = None

        self.labelTitle = cTkinter.CTkLabel(self, text="Track inserter", font=("arial", 30, "bold"))
        self.labelTitle.pack(padx=20, pady=20)

        self.setMonth()
        self.setPhrase()
        self.setTrackSelector()

        uiUtils.setReturn(self, self.returnToMain, "Return")

        self.insertTrackButton = cTkinter.CTkButton(self, text="Insert track", fg_color=["#075C00", "#075C00"], hover_color=["#074500", "#074500"], command=self.insertTrack)
        self.insertTrackButton.place(anchor="center", relx=0.5, rely=0.55)     

    def setMonth(self):
        def setComboDay(monthChoise):
            daysTo28 = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18",
            "19","20","21","22","23","24","25","26","27","28"]
        
            daysTo30 = daysTo28.copy()
            daysTo30.extend(["29", "30"])

            daysTo31 = daysTo30.copy()
            daysTo31.append("31")

            match monthChoise:
                case "February":
                    selectedDays = daysTo28
                case "January" | "March" | "May" | "July" | "August" | "October" | "December":
                    selectedDays = daysTo31
                case _:
                    selectedDays = daysTo30

            self.comboDay.configure(values=selectedDays)

        defaultChoise = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18",
        "19","20","21","22","23","24","25","26","27","28", "29", "30"]

        self.dayLabel = cTkinter.CTkLabel(self, text="Select day")
        self.dayLabel.place(anchor="ne", relx=0.22, rely=0.49)

        self.comboDay = cTkinter.CTkComboBox(self, values=defaultChoise, state="readonly")
        self.comboDay.place(anchor="ne", relx=0.3, rely=0.565)


        self.monthLabel = cTkinter.CTkLabel(self, text="Select month")
        self.monthLabel.place(anchor="ne", relx=0.23, rely=0.29)

        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                  "November", "December"]

        self.monthsComboBox = cTkinter.CTkComboBox(self, values=months, state="readonly", command=setComboDay)
        self.monthsComboBox.place(anchor="ne", relx=0.3, rely=0.365)

        self.monthsComboBox.set("January")
        self.comboDay.set("1")

    def setPhrase(self):
        self.phraseLabel = cTkinter.CTkLabel(self, text="Write a phrase")
        self.phraseLabel.place(anchor="sw", relx=0.755, rely=0.354)

        self.phraseTextBox = cTkinter.CTkEntry(self, width=140, height=28)
        self.phraseTextBox.place(anchor="sw", relx=0.7, rely=0.44)
    
    def setTrackSelector(self):
        from ui import uiUtils

        def selectTrack():
            from data import fileManager
            
            baseTrackPath = fileManager.getBaseTrackPath()
            self.trackEntry.configure(text=baseTrackPath.stem)
            self.baseTrackPath = baseTrackPath

            message = "Track selected:" + str(self.baseTrackPath)
            print(message)
            uiUtils.throwWarning(self, message, 0.33)

        self.trackLabel = cTkinter.CTkLabel(self, text="Select track")
        self.trackLabel.place(anchor="sw", relx=0.76, rely=0.574)

        self.trackEntry = cTkinter.CTkButton(self, text="example_track", fg_color=["#D4D4D4","#D4D4D4"],
            hover_color=["#C2C2C2","#C2C2C2"], text_color=["black","black"], command=selectTrack)
        self.trackEntry.place(anchor="sw", relx=0.7, rely=0.64)

    def insertTrack(self):
        import eyed3
        from ui import uiUtils
        from data import jsonParser, fileManager

        monthId = self.monthsComboBox.get().lower()[:3]
        trackDay = self.comboDay.get()
        trackPhrase = self.phraseTextBox.get()

        if (not trackDay.isnumeric()):
            uiUtils.throwWarning(self, "Warning! Days can only be numeric", 0.4)
            return
        
        if (int(trackDay) > 31):
            uiUtils.throwWarning(self, "Warning! tracks can have only 31 days", 0.43)
            return

        if (self.baseTrackPath is None or self.baseTrackPath == "example_track"):
            uiUtils.throwWarning(self, "Warning! No track selected", 0.33)
            return
        
        trackPath = fileManager.addTrack(monthId, self.baseTrackPath)
        
        track = eyed3.load(trackPath)

        try:
            trackMetadata = jsonParser.Encoder(
                pMonth=monthId,
                pName=track.tag.title,
                pAuthor=track.tag.artist,
                pTrackId=trackPath.stem,
                pPhraseDay=trackDay
            )

            trackMetadata.encodeTrack()

            if (not trackDay is None):
                fileManager.addPhrase(monthId, trackDay, trackPhrase)

            self.successLabel = cTkinter.CTkLabel(self, text="Track added succesfully!", text_color=["green", "green"])
            self.successLabel.place(anchor="e", relx=0.3, rely=0.95)
        except Exception as e:
            uiUtils.throwWarning(self, e, 0.4)

    def returnToMain(self):
        self.destroy()
        self.master.deiconify()