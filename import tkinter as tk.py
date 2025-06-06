import tkinter as tk
import random
import copy

BOARD_SIZE = 3  # Change to 4 for 4x4 board

class TicTacToe:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic Tac Toe")
        self.stats = {"X": 0, "O": 0, "Draw": 0}
        self.mode = tk.StringVar(value="2P")
        self.create_widgets()
        self.reset_board()

    def create_widgets(self):
        top = tk.Frame(self.master)
        top.pack()
        tk.Radiobutton(top, text="2 Player", variable=self.mode, value="2P", command=self.reset_board).pack(side=tk.LEFT)
        tk.Radiobutton(top, text="Vs Computer", variable=self.mode, value="AI", command=self.reset_board).pack(side=tk.LEFT)
        tk.Button(top, text="Undo", command=self.undo_move).pack(side=tk.LEFT)
        tk.Button(top, text="Reset", command=self.reset_board).pack(side=tk.LEFT)
        self.status = tk.Label(self.master, text="", font=("Arial", 14))
        self.status.pack()
        self.stats_label = tk.Label(self.master, text="", font=("Arial", 10))
        self.stats_label.pack()
        self.buttons = []
        board = tk.Frame(self.master)
        board.pack()
        for i in range(BOARD_SIZE):
            row = []
            for j in range(BOARD_SIZE):
                btn = tk.Button(board, text="", width=4, height=2, font=("Arial", 24),
                                command=lambda r=i, c=j: self.make_move(r, c))
                btn.grid(row=i, column=j)
                row.append(btn)
            self.buttons.append(row)

    def reset_board(self):
        self.board = [["" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.history = []
        self.current_player = "X"
        for row in self.buttons:
            for btn in row:
                btn.config(text="", state=tk.NORMAL)
        self.status.config(text=f"{self.current_player}'s turn")
        self.update_stats()
        if self.mode.get() == "AI" and self.current_player == "O":
            self.master.after(500, self.ai_move)

    def update_stats(self):
        self.stats_label.config(
            text=f"X Wins: {self.stats['X']} | O Wins: {self.stats['O']} | Draws: {self.stats['Draw']}"
        )

    def make_move(self, row, col):
        if self.board[row][col] == "" and not self.check_winner(self.board):
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player)
            self.history.append((row, col))
            winner = self.check_winner(self.board)
            if winner:
                self.end_game(winner)
            elif all(self.board[r][c] != "" for r in range(BOARD_SIZE) for c in range(BOARD_SIZE)):
                self.end_game("Draw")
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                self.status.config(text=f"{self.current_player}'s turn")
                if self.mode.get() == "AI" and self.current_player == "O":
                    self.master.after(500, self.ai_move)

    def undo_move(self):
        if self.history:
            row, col = self.history.pop()
            self.board[row][col] = ""
            self.buttons[row][col].config(text="")
            self.current_player = "O" if self.current_player == "X" else "X"
            self.status.config(text=f"{self.current_player}'s turn")

    def end_game(self, winner):
        if winner == "Draw":
            self.status.config(text="Draw!")
            self.stats["Draw"] += 1
        else:
            self.status.config(text=f"{winner} wins!")
            self.stats[winner] += 1
        self.update_stats()
        for row in self.buttons:
            for btn in row:
                btn.config(state=tk.DISABLED)

    def ai_move(self):
        if self.mode.get() == "AI" and not self.check_winner(self.board):
            # Uncomment for unbeatable AI:
            # _, move = self.minimax(self.board, "O")
            # Simpler random AI:
            moves = [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE) if self.board[r][c] == ""]
            move = random.choice(moves) if moves else None
            if move:
                self.make_move(*move)

    def check_winner(self, board):
        lines = []
        # Rows and columns
        for i in range(BOARD_SIZE):
            lines.append([board[i][j] for j in range(BOARD_SIZE)])
            lines.append([board[j][i] for j in range(BOARD_SIZE)])
        # Diagonals
        lines.append([board[i][i] for i in range(BOARD_SIZE)])
        lines.append([board[i][BOARD_SIZE - 1 - i] for i in range(BOARD_SIZE)])
        for line in lines:
            if line.count(line[0]) == BOARD_SIZE and line[0] != "":
                return line[0]
        return None

    def minimax(self, board, player):
        winner = self.check_winner(board)
        if winner == "O":
            return 1, None
        elif winner == "X":
            return -1, None
        elif all(board[r][c] != "" for r in range(BOARD_SIZE) for c in range(BOARD_SIZE)):
            return 0, None

        moves = [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE) if board[r][c] == ""]
        if player == "O":
            best_score = -float("inf")
            best_move = None
            for r, c in moves:
                new_board = copy.deepcopy(board)
                new_board[r][c] = "O"
                score, _ = self.minimax(new_board, "X")
                if score > best_score:
                    best_score = score
                    best_move = (r, c)
            return best_score, best_move
        else:
            best_score = float("inf")
            best_move = None
            for r, c in moves:
                new_board = copy.deepcopy(board)
                new_board[r][c] = "X"
                score, _ = self.minimax(new_board, "O")
                if score < best_score:
                    best_score = score
                    best_move = (r, c)
            return best_score, best_move

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()