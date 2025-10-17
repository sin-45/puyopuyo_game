# main.py (修正版)

import tkinter as tk
from src.utill.board import Board
from src.solve.solve import Solve

class PuyoPuyoGUI:
    BOARD_H, BOARD_W = 15, 6
    CELL_SIZE = 32
    COLORS = {0: "#2d2d2d", 1: "red", 2: "blue", 3: "green", 4: "yellow"}
    ROTATIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    CHAIN_DELAY_MS = 500

    def __init__(self, master):
        self.master = master
        self.master.title("ぷよぷよ練習モード")
        self.master.resizable(False, False)

        self.board = Board()
        self.solve = Solve(self.board)

        self.game_over = False
        self.puyo_is_active = False
        self.puyo_colors = self.solve.random_pyo()
        self.next_puyo_colors = self.solve.random_pyo()

        main_frame = tk.Frame(master, bg="#1a1a1a"); main_frame.pack()
        self.canvas = tk.Canvas(main_frame, width=self.BOARD_W * self.CELL_SIZE, height=self.BOARD_H * self.CELL_SIZE, bg="#1a1a1a", highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, padx=(10, 5), pady=10)
        
        info_panel = tk.Frame(main_frame, bg="#1a1a1a"); info_panel.pack(side=tk.LEFT, padx=(5, 10), pady=10, anchor='n')
        tk.Label(info_panel, text="NEXT", fg="white", bg="#1a1a1a").pack()
        self.next_canvas = tk.Canvas(info_panel, width=self.CELL_SIZE * 2, height=self.CELL_SIZE, bg="#1a1a1a", highlightthickness=0)
        self.next_canvas.pack()

        self.master.bind("<KeyPress>", self.handle_key)

        self.start_new_turn()
        self.update_drawing()

    def start_new_turn(self):
        self.puyo_colors = self.next_puyo_colors
        self.next_puyo_colors = self.solve.random_pyo()
        self.axis_pos = [1, 2]
        self.rotation_state = 0
        if self.board.game_end(self.axis_pos[0], self.axis_pos[1]):
            self.game_over = True
        else:
            self.puyo_is_active = True

    def get_puyo_coords(self):
        ax_r, ax_c = self.axis_pos
        rel_r, rel_c = self.ROTATIONS[self.rotation_state]
        return (ax_r, ax_c), (ax_r + rel_r, ax_c + rel_c)

    def is_valid_position(self, axis_pos, rotation_state):
        ax_r, ax_c = axis_pos
        rel_r, rel_c = self.ROTATIONS[rotation_state]
        p2_r, p2_c = ax_r + rel_r, ax_c + rel_c
        return not self.board.game_end(ax_r, ax_c) and not self.board.game_end(p2_r, p2_c)

    def handle_key(self, event):
        if not self.puyo_is_active or self.game_over: return
        key = event.keysym
        
        if key == "Left":
            new_pos = [self.axis_pos[0], self.axis_pos[1] - 1]
            if self.is_valid_position(new_pos, self.rotation_state): self.axis_pos = new_pos
        elif key == "Right":
            new_pos = [self.axis_pos[0], self.axis_pos[1] + 1]
            if self.is_valid_position(new_pos, self.rotation_state): self.axis_pos = new_pos
        elif key == "Down":
            self.move_down_once()
        elif key in ["x", "z"]:
            direction = 1 if key == 'x' else -1
            new_rot = (self.rotation_state + direction) % 4
            if self.is_valid_position(self.axis_pos, new_rot):
                self.rotation_state = new_rot
            else:
                for dc in [-1, 1]:
                    new_pos = [self.axis_pos[0], self.axis_pos[1] + dc]
                    if self.is_valid_position(new_pos, new_rot):
                        self.axis_pos = new_pos; self.rotation_state = new_rot; break
        elif key == "space" or key == "Up":
            self.hard_drop()

    def hard_drop(self):
        self.lock_puyo()

    def move_down_once(self) -> bool:
        new_pos = [self.axis_pos[0] + 1, self.axis_pos[1]]
        if self.is_valid_position(new_pos, self.rotation_state):
            self.axis_pos = new_pos
            return True
        else:
            self.lock_puyo()
            return False

    def lock_puyo(self):
        """★変更点: このメソッドのロジックを全面的に修正"""
        if not self.puyo_is_active: return
        self.puyo_is_active = False
        
        # ぷよの最終的な列と向きを決定
        axis_column = self.axis_pos[1]
        orientation_map = {0: 'u', 1: 'r', 2: 'd', 3: 'l'}
        orientation = orientation_map[self.rotation_state]
        
        # Boardクラスのsettingメソッドを呼び出す
        # これが各ぷよを正しい高さに自動で設置してくれます
        self.board.setting(axis_column, orientation, self.puyo_colors[0], self.puyo_colors[1])
        
        # 連鎖アニメーションを開始
        self.run_chain_sequence()

    def run_chain_sequence(self):
        chain_happened = self.solve.pyo_clear()
        self.draw()
        if chain_happened:
            self.master.after(self.CHAIN_DELAY_MS, self.run_chain_sequence)
        else:
            if not self.game_over:
                self.start_new_turn()

    def draw(self):
        self.canvas.delete("all")
        for r in range(self.BOARD_H):
            for c in range(self.BOARD_W):
                color = self.COLORS.get(self.board.board[r][c], "black")
                x1, y1 = c * self.CELL_SIZE, r * self.CELL_SIZE
                self.canvas.create_oval(x1+2, y1+2, x1+self.CELL_SIZE-2, y1+self.CELL_SIZE-2, fill=color, outline=color)
        if self.puyo_is_active:
            p1, p2 = self.get_puyo_coords()
            coords = [(p1, self.puyo_colors[0]), (p2, self.puyo_colors[1])]
            for (r, c), color_code in coords:
                x1, y1 = c * self.CELL_SIZE, r * self.CELL_SIZE
                self.canvas.create_oval(x1+2, y1+2, x1+self.CELL_SIZE-2, y1+self.CELL_SIZE-2, fill=self.COLORS[color_code], outline="white")
        
        self.next_canvas.delete("all")
        c1, c2 = self.next_puyo_colors
        self.next_canvas.create_oval(2, 2, self.CELL_SIZE-2, self.CELL_SIZE-2, fill=self.COLORS[c1], outline=self.COLORS[c1])
        self.next_canvas.create_oval(self.CELL_SIZE+2, 2, self.CELL_SIZE*2-2, self.CELL_SIZE-2, fill=self.COLORS[c2], outline=self.COLORS[c2])

        if self.game_over:
            self.canvas.create_text(self.BOARD_W * self.CELL_SIZE / 2, self.BOARD_H * self.CELL_SIZE / 2, text="GAME OVER", font=("Helvetica", 32, "bold"), fill="white")

    def update_drawing(self):
        self.draw()
        self.master.after(33, self.update_drawing)

if __name__ == "__main__":
    root = tk.Tk()
    app = PuyoPuyoGUI(root)
    root.mainloop()