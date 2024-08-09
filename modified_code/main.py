from gui import MainApp
import tkinter as tk

# Tkinterのウィンドウ作成と実行
if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root, "Gravitational Lens Simulation")
    root.mainloop()
