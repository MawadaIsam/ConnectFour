from src.ui.gui import GUI
from src.ui.ui import UI
import tkinter as tk


def main():
    print("==== CONNECT FOUR ====")
    print('1. Console')
    print('2. GUI')
    choice = input("Enter your choice: ").strip()

    if choice == '1':
        UI().run()
    elif choice == '2':
        root= tk.Tk()
        GUI(root)
        root.mainloop()
    else:
        print("Invalid choice")


if __name__ == '__main__':
    main()

