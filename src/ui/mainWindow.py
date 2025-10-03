import customtkinter as cTkinter

cTkinter.set_appearance_mode("system")

class MainWindow(cTkinter.CTk):
    def __init__(self, *args, **kwargs):
        from ui import uiUtils

        super().__init__(*args, **kwargs)
        self.geometry("600x400")
        self.title("Cullerian player")

        self.selfTrackButton = cTkinter.CTkButton(self, text="Insert a new track", command=self.openInsertTrack)
        self.selfTrackButton.place(anchor="e", relx=0.29, rely=0.95)

        self.pauseButton = cTkinter.CTkButton(self, text="Pause/Play", fg_color=["#47D14A", "#47D14A"],
            hover_color=["#3DBF40","#3DBF40"], command=self.pauseTrack)
        self.pauseButton.place(anchor="center", relx=0.33, rely=0.55)

        self.stopButton = cTkinter.CTkButton(self, text="Stop", fg_color=["#6E0000","#6E0000"],
            hover_color=["#520000", "#520000"], command=self.stopTrack)
        self.stopButton.place(anchor="center", relx=0.67, rely=0.55)

        uiUtils.setReturn(self, self.exitProgram, "Exit")

        self.insertTrackWindow = None

        self.playTrack()

    def openInsertTrack(self):
        import pygame
        from ui import insertTrackWindow

        if self.insertTrackWindow is None or not self.insertTrackWindow.winfo_exists():
            self.insertTrackWindow = insertTrackWindow.InsertTrackWindow(self)
        else:
            self.insertTrackWindow.focus()

        if pygame.mixer_music.get_busy():
            pygame.mixer_music.pause()

        self.withdraw()

    def setTrackData(self, pName:str, pAuthor:str, pPhrase:str):
        self.trackNameLabel = cTkinter.CTkLabel(self, text=pName, font=("arial", 20, "bold"))
        self.trackNameLabel.place(anchor="center", relx=0.5, rely=0.36)

        self.trackpAuthorLabel = cTkinter.CTkLabel(self, text=pAuthor, font=("arial", 15, "underline"))
        self.trackpAuthorLabel.place(anchor="center", relx=0.5, rely=0.45)

        if (not pPhrase == ""):
            self.trackpPhraseLabel = cTkinter.CTkLabel(self, text=('"'+ pPhrase + '"'))
            self.trackpPhraseLabel.place(anchor="center", relx=0.5, rely=0.5)

    def playTrack(self):
        import pygame
        from ui import uiUtils
        from core import trackPlayer

        if (trackPlayer.noTracksLoaded()):
            uiUtils.throwWarning(self, "Warning! No tracks available to play", 0.5, 0.5, "center")
            return

        pygame.mixer.init()

        dailyTrack, dailyPhrase = trackPlayer.getDailyTrack()
        trackName, trackAuthor, trackPath = trackPlayer.getTrackData(dailyTrack)

        self.setTrackData(trackName, trackAuthor, dailyPhrase)

        pygame.mixer.music.load(str(trackPath))
        pygame.mixer.music.play(loops=0)

    def pauseTrack(self):
        import pygame

        if (pygame.mixer_music.get_busy()):
            pygame.mixer_music.pause()
        else:
            pygame.mixer_music.unpause()
    
    def stopTrack(self):
        import pygame

        if (pygame.mixer_music.get_busy()):
            pygame.mixer_music.stop()

    def exitProgram(self):
        self.destroy() 