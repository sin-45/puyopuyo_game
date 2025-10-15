from copy import deepcopy

from src.utill.board import Board

class Solve:
    def __init__(self, board: Board):
        self.cmd = True
        self.board = board

    def solve(self):
        for _ in range(10):
            print("=======================================")
            # for i in self.board: print(i)
            command = list(input().split())
            if len(command) == 0: break
            command = [
                int(command[0]),
                command[1],
                int(command[2]),
                int(command[3])
                ]
            if self.cmd:
                if command[1] == "l" and command[0] == 0:
                    command[0] += 1

                elif command[1] == "r" and command[0] >= 6:
                    command[0] = 5

            board.setting(*command)
            for i in self.board: print(i)
            # print(*command)
            self.pyo_clear()

    def pyo_clear(self):
        while True:
            self.board_map = [[False] * 6 for _ in range(15)]
            clear_puyo_list = []
            for i in range(15):
                for j in range(6):
                    if self.board[i][j] == 0:
                        self.board_map[i][j] = True
                    else:
                        choice = self.board[i][j]
                        clear_puyo_list += self.pyo_clear_search(i, j, choice)

            print(clear_puyo_list)
            if len(clear_puyo_list) == 0:
                break     
            
            # print("->", clear_puyo_list)
            for k in self.board: print(k)

            # ぷよを消す
            for i, j in clear_puyo_list:
                self.board[i][j] = 0

            # print()
            # for k in self.board: print(k)
            # ぷよを消した分下にブラス
            for i in range(6):
                heigh = 14
                for j in range(14, -1, -1):
                    if self.board[j][i] != 0:
                        # print(j, i, heigh, i)
                        if heigh != j:
                            self.board[heigh][i] = self.board[j][i]
                            self.board[j][i] = 0
                        heigh -= 1

            print("~~~~~~~~~~~~~~~~~~~~")
            for i in self.board: print(i)
            print("~~~~~~~~~~~~~~~~~~~~~~~")

    def pyo_clear_search(self, i: int, j:int, choice:int) -> list:
        temp = [[i, j]]
        dxdy = [[0, -1], [0, 1], [-1, 0], [1, 0]]
        cnt = 1
        result = []
        while temp:
            x, y = temp.pop()
            result.append([x, y])
            if self.board_map[x][y]:
                continue
            self.board_map[x][y] = True
            for p, q in dxdy:
                nx, ny = x+p, y+q
                if 0 <= nx < 15 and 0 <= ny < 6:
                    if not self.board_map[nx][ny] and self.board[nx][ny] == choice:
                        temp.append([nx, ny])
                        cnt += 1

        # print(cnt)
        if cnt >= 4:
            print("=>", result)
            print("color", choice)
            return result
        else:
            return []

if __name__ == "__main__":
    board = Board()
    # print(board)
    solve = Solve(board)
    solve.solve()
