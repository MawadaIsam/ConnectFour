import tkinter as tk
from tkinter import messagebox
from src.services.game import Game

class GUI:
    def __init__(self,root):
        self.root = root
        self.root.title("Connect Four")
        self.cell_size=70

        #control frame
        control_frame = tk.Frame(root)
        control_frame.pack(pady=10)

        #AI difficulty selector
        tk.Label(
            control_frame,
            text="AI Difficulty",
            font=("Arial", 12, "bold"),
        ). pack(side=tk.LEFT, padx = 5)

        self.ai_var = tk.StringVar(value="basic") #storing ai choice

        tk.Radiobutton(
            control_frame,
            text="Basic AI",
            variable=self.ai_var,
            value="basic",
            font=("Arial", 10),
        ).pack(side=tk.LEFT, padx=5)

        tk.Radiobutton(
            control_frame,
            text="Advanced AI (Minimax)",
            variable=self.ai_var,
            value= "minimax",
            font=("Arial", 10),
        ).pack(side=tk.LEFT, padx=5)

        #new game button
        tk.Button(
            control_frame,
            text="New Game",
            command= self._new_game,
            font=("Arial", 10, "bold"),
            bg="#27AE60",
            fg="white",
            padx=10,
            pady=5
        ).pack(side=tk.LEFT, padx=10)


        #creating canvas
        self.canvas =tk.Canvas(
            root,
            width=self.cell_size*7,
            height=self.cell_size*6,
            bg = "blue"
        )
        self.canvas.pack(padx=10, pady=10)
        self.canvas.bind('<Button-1>', self._on_click)

        #status label
        self.status =tk.Label(
            root,
            text="Your Turn (Red)",
            font=("Arial", 20, "bold")
        )
        self.status.pack(pady=5)



        self._new_game()


    def _draw_board(self):
        self.canvas.delete('all')

        for row in range(6):
            for col in range(7):
                x= col * self.cell_size + self.cell_size//2
                y= row * self.cell_size + self.cell_size//2

                cell= self.game.board.grid[row][col]
                color= 'white' if cell ==0 else('red'if cell ==1 else'yellow')

                self.canvas.create_oval(
                    x-25,y-25,x+25,y+25,
                    fill=color,outline='black',width=2
                )


    def _on_click(self, event):
        # handle the mouse click
        if self.game.game_over or self.game.current_player == 2:
            return

        col= event.x // self.cell_size
        result= self.game.make_move(col)

        if not result['success']:
            messagebox.showwarning('Invalid Move', result['message'])
            return

        self._draw_board()

        if self.game.game_over:
            self._show_result()
        else:
            self.root.after(500, self._computer_move)#add a short delay before computer plays


    def _computer_move(self):
        if self.game.game_over:
            return

        self.status.config(text="Computer's thinking...")
        self.root.update()

        col=self.game.get_computer_move()
        self.game.make_move(col)
        self._draw_board()

        if self.game.game_over:
            self._show_result()
        else:
            self.status.config(text=" Your Turn (Red)")


    def _show_result(self):

        if self.game.winner==1:
            msg ='You Win'
        elif self.game.winner==2:
            msg ='You Lose, Computer Wins'
        else:
            msg ='DRAW'

        messagebox.showinfo("Game Over", msg)
        self.status.config(text="Game Over-"+ msg)

    def _new_game(self):
        use_minimax=(self.ai_var.get()=="minimax")

        self.game = Game(use_minimax=use_minimax,minimax_depth=5)
        self.status.config(text="Your Turn (Red)")
        self._draw_board()


if __name__ == '__main__':
    root = tk.Tk()
    GUI(root)
    root.mainloop()





