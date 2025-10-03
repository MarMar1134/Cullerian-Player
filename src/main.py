import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import customtkinter as cTkinter
from ui import MainWindow

def main():
    cTkinter.set_appearance_mode("system")
    
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()