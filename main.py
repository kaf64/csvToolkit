import tkinter as tk
from main_window import MainWindow


def main() -> None:
    root = tk.Tk()
    main_window = MainWindow(root)
    main_window.mainloop()


if __name__ == '__main__':
    main()
