class Board:
    def __init__(self):
        self.board = [[0 for j in range(6)] for _ in range(15)]
        

    def setting(self, x: int, c: str, p1: int, p2: int):
        """ぷよぷよを設置します

            Args:
                x (int): 列番号
                c (str): 向き (l, r, u, d)
                p1, p2 (int, int): ぷよぷよの色
        """
        self.board_up = [15] * 6
        for i in range(6):
            for j in range(15):
                if self.board[j][i] != 0:
                    self.board_up[i] = j
                    break

        center = self.board_up[x]
        print(center)
        print(self.board_up)
        # for i in self.board: print(i)
        if c == "u":
            self.board[center-1][x] = p1
            self.board[center-2][x] = p2
            self.board_up[x] -= 2

        elif c == "d":
            self.board[center-2][x] = p1
            self.board[center-1][x] = p2
            self.board_up[x] -= 2

        elif c == "l":
            left = self.board_up[x-1]
            self.board[center-1][x] = p1
            self.board[left-1][x-1] = p2
            self.board_up[x-1] -= 1
            self.board_up[x] -= 1

        else:
            right = self.board_up[x-1]
            self.board[center-1][x] = p1
            self.board[right-1][x+1] = p2
            self.board_up[x] -= 1
            self.board_up[x+1] = 1


    def __getitem__(self, index: int) -> list:
        # インデックスを使ってデータ要素を返す
        return self.board[index]
    
if __name__ == "__main__":
    g = Board()
    # g.setting(2, "l", 1, 3)
    # g.setting(1, "l", 3, 0)
    # g.setting(3, "u", 3, 0)
    # g.setting(1, "l", 2, 2)
    # g.setting(4, "d", 0, 0)
    for i in g: print(i)
    print()
    print(g.board_up)
        
        

