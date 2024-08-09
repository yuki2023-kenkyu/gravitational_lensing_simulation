import tkinter as tk
from tkinter import Scale, Radiobutton, IntVar, Checkbutton, BooleanVar, Button

class ParameterWindow:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.master.title("パラメーター設定")

        self.scale_rs = self.create_scale_with_reset("シュバルツシルト半径", 10, 100, 50, self.reset_rs)
        self.scale_x = self.create_scale_with_reset("レンズ天体のX位置", -app.width//2, app.width//2, 0, self.reset_x)
        self.scale_y = self.create_scale_with_reset("レンズ天体のY位置", -app.height//2, app.height//2, 0, self.reset_y)
        self.scale_a = self.create_scale_with_reset("Kerrパラメータ a", 0, 1, 0.5, self.reset_a)
        self.scale_window_size = self.create_scale_with_reset("ウィンドウサイズ", 400, 1600, 800, self.reset_window_size, resolution=100)

        self.bh_type = IntVar()
        self.bh_type.set(1)  # デフォルトはシュバルツシルトブラックホール

        Radiobutton(master, text="シュバルツシルトブラックホール", variable=self.bh_type, value=1).pack(anchor=tk.W)
        Radiobutton(master, text="Kerrブラックホール", variable=self.bh_type, value=2).pack(anchor=tk.W)

        self.fill_inside_horizon = BooleanVar()
        self.fill_inside_horizon.set(False)  # デフォルトは塗りつぶしなし
        Checkbutton(master, text="シュバルツシルト半径内を塗りつぶす", variable=self.fill_inside_horizon).pack(anchor=tk.W)

        self.update_button = tk.Button(master, text="更新", command=self.update_parameters)
        self.update_button.pack()

        # 終了ボタンを作成して配置
        self.exit_button = tk.Button(master, text="終了", command=app.on_closing)
        self.exit_button.pack()

    def create_scale_with_reset(self, label, from_, to_, initial, reset_command, resolution=1):
        frame = tk.Frame(self.master)
        frame.pack(fill=tk.X)

        scale = Scale(frame, from_=from_, to_=to_, orient=tk.HORIZONTAL, label=label, resolution=resolution)
        scale.set(initial)
        scale.pack(side=tk.LEFT, expand=True, fill=tk.X)

        button = Button(frame, text="リセット", command=reset_command)
        button.pack(side=tk.RIGHT)

        return scale

    def reset_rs(self):
        self.scale_rs.set(50)

    def reset_x(self):
        self.scale_x.set(0)

    def reset_y(self):
        self.scale_y.set(0)

    def reset_a(self):
        self.scale_a.set(0.5)

    def reset_window_size(self):
        self.scale_window_size.set(800)

    def update_parameters(self):
        self.app.Rs = self.scale_rs.get()
        self.app.lens_x = self.app.width // 2 + self.scale_x.get()
        self.app.lens_y = self.app.height // 2 + self.scale_y.get()
        self.app.a = self.scale_a.get()
        self.app.window_size = self.scale_window_size.get()
        self.app.bh_type = self.bh_type.get()
        self.app.fill_inside_horizon = self.fill_inside_horizon.get()
