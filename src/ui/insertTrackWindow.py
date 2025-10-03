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

        self.insertTrackButton = cTkinter.CTkButton(self, text="Insert track", fg_color=["#075C00", "#075C00"], hover_color=["#074500", "#074500"], command=self.insertTrack) 
        
        self.checkSelectedData()
        uiUtils.setReturn(self, self.returnToMain, "Return")

    def setMonth(self):
        def setComboDay(monthChoise):
            daysTo28 = ["No special day", "1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18",
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
            self.comboDay.set(selectedDays[0]) 
            setPhraseEntry("") 
            self.checkSelectedData()

        def setPhraseEntry(choise):
            current_text = self.phraseTextBox.get()
            self.phraseTextBox.configure(state="normal")
            self.phraseTextBox.delete(0, cTkinter.END)
            self.phraseTextBox.configure(state="disabled")
            
            if self.comboDay.get() == "No special day":
                self.phraseTextBox.configure(state="normal")
                self.phraseTextBox.insert(0, "No phrases allowed for non-special days")
                self.phraseTextBox.configure(state="disabled")
            else:
                if current_text == "No phrases allowed for non-special days":
                    current_text = ""  # Clear the default message
                self.phraseTextBox.insert(0, current_text)
                self.phraseTextBox.configure(state="normal")

        defaultChoise = ["No special day", "1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18",
        "19","20","21","22","23","24","25","26","27","28", "29", "30"]

        self.dayLabel = cTkinter.CTkLabel(self, text="Select day")
        self.dayLabel.place(anchor="ne", relx=0.22, rely=0.49)

        self.comboDay = cTkinter.CTkComboBox(self, values=defaultChoise, state="readonly", command=setPhraseEntry)
        self.comboDay.place(anchor="ne", relx=0.3, rely=0.565)


        self.monthLabel = cTkinter.CTkLabel(self, text="Select month")
        self.monthLabel.place(anchor="ne", relx=0.23, rely=0.29)

        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                  "November", "December"]

        self.monthsComboBox = cTkinter.CTkComboBox(self, values=months, state="readonly", command=setComboDay)
        self.monthsComboBox.place(anchor="ne", relx=0.3, rely=0.365)

        self.monthsComboBox.set("January")
        self.comboDay.set("No special day")

    def setPhrase(self):
        self.phraseLabel = cTkinter.CTkLabel(self, text="Write a phrase")
        self.phraseLabel.place(anchor="sw", relx=0.755, rely=0.354)

        self.phraseTextBox = cTkinter.CTkEntry(self, width=140, height=28, placeholder_text="No phrases allowed for non-special days")
        self.phraseTextBox.place(anchor="sw", relx=0.7, rely=0.44)
        
        self.phraseTextBox.configure(state="disabled")
        self.phraseTextBox.insert(0, "No phrases allowed for non-special days")
    
    def setTrackSelector(self):
        def selectTrack():
            from data import fileManager
            
            baseTrackPath = fileManager.getBaseTrackPath()
            self.trackEntry.configure(text=baseTrackPath.stem)
            self.baseTrackPath = baseTrackPath
            self.checkSelectedData()

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

        if (trackDay == "No special day"):
            trackDay = None
            trackPhrase = ""

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

            trackMetadata.encodeTrackData()

            if (not trackDay is None):
                fileManager.addPhrase(monthId, trackDay, trackPhrase)

            self.successLabel = cTkinter.CTkLabel(self, text="Track added succesfully!", text_color=["green", "green"])
            self.successLabel.place(anchor="e", relx=0.3, rely=0.95)
        except Exception as e:
            uiUtils.throwWarning(self, e, 0.4)

    def checkSelectedData(self):
        from data import jsonParser
        from ui import uiUtils

        trackData = jsonParser.Encoder(
            pMonth=self.monthsComboBox.get().lower()[:3],
            pName="",
            pAuthor="",
            pTrackId=self.baseTrackPath.stem if self.baseTrackPath is not None else "",
            pPhraseDay=self.comboDay.get()
        )

        if (self.baseTrackPath is not None):
            if (trackData.trackExists()):
                uiUtils.throwWarning(self, "Warning! The selected track already exists.\n Don't you want to modify it instead?", 0.5, 0.5, "center")
                self.insertTrackButton.pack_forget()
                return
            elif(self.monthsComboBox.get() and self.comboDay.get()):
                uiUtils.clearWarnings(self)

                self.insertTrackButton.pack()
                self.insertTrackButton.place(anchor="center", relx=0.5, rely=0.6)
        else:
            self.insertTrackButton.pack_forget()

    def returnToMain(self):
        self.destroy()
        self.master.deiconify()