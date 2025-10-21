from src.utill.board import Board
import tkinter as tk
import json
from src.gui.ai_main_gui import PuyoPuyoGUI

if __name__ == '__main__':
    # js = json.loads(open('json/test.json','r').read())
    # print(js)
    # field = Field(js)
    # print(field)
    root = tk.Tk()
    app = PuyoPuyoGUI(root)
    root.mainloop()