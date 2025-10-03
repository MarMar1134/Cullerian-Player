"""
    Utility functions for all the graphic handle of Cullerian Player.
"""

import customtkinter as cTkinter

def setReturn(self, pCommand, pDisplayText:str):
    self.exitButton = cTkinter.CTkButton(self, text=pDisplayText, fg_color=["#FF0000","#FF0000"], hover_color=["#B50000", "#B50000"], command=pCommand)
    self.exitButton.place(anchor="center", relx=0.85, rely=0.95, bordermode="inside")

def throwWarning(self, pDisplayText:str, pRelx:float=0.4, pRely:float=0.95, pAnchor:str = "e"):
    if hasattr(self, "warningLabel") and self.warningLabel.winfo_exists():
        self.warningLabel.destroy()

    self.warningLabel = cTkinter.CTkLabel(self, text=pDisplayText, text_color=["red", "red"])
    self.warningLabel.place(anchor=pAnchor, relx=pRelx, rely=pRely)