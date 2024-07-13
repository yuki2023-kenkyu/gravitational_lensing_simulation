import cv2
import numpy as np
import tkinter as tk
from tkinter import Toplevel, Scale, Radiobutton, IntVar, Button
from PIL import Image, ImageTk
from gravitational_lensing_effect import schwarzschild_lens_effect, kerr_lens_effect

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

        self.update_button = tk.Button(master, text="更新", command=self.update_parameters)
        self.update_button.pack()

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

class ImageWindow:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.master.title("画像表示")
        self.canvas = tk.Canvas(master, width=app.window_size * 2, height=app.window_size)
        self.canvas.pack()
        self.image_on_canvas = None
        self.image_refs = []  # 参照を保持するリスト
        self.update()

    def update(self):
        ret, frame = self.app.cap.read()
        if ret:
            if self.app.bh_type == 1:
                lensed_frame = schwarzschild_lens_effect(frame, Rs=self.app.Rs, center=(self.app.lens_x, self.app.lens_y))
            else:
                lensed_frame = kerr_lens_effect(frame, Rs=self.app.Rs, a=self.app.a, center=(self.app.lens_x, self.app.lens_y))

            combined_frame = np.hstack((frame, lensed_frame))

            # 画像のサイズをウィンドウサイズに合わせてリサイズ
            combined_frame = cv2.resize(combined_frame, (self.app.window_size * 2, self.app.window_size))
            combined_frame = cv2.cvtColor(combined_frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(combined_frame)
            imgtk = ImageTk.PhotoImage(image=image)
            self.image_refs.append(imgtk)  # 参照をリストに追加

            if self.image_on_canvas is None:
                self.image_on_canvas = self.canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)
            else:
                self.canvas.itemconfig(self.image_on_canvas, image=imgtk)

        self.master.after(10, self.update)

class App:
    def __init__(self, root):
        self.root = root
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("カメラが見つかりません")
            exit()

        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.Rs = 50
        self.lens_x = self.width // 2
        self.lens_y = self.height // 2
        self.a = 0.5
        self.window_size = 800  # 初期ウィンドウサイズ
        self.bh_type = 1

        param_window = Toplevel(self.root)
        self.param_win = ParameterWindow(param_window, self)

        image_window = Toplevel(self.root)
        self.image_win = ImageWindow(image_window, self)

    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()

root = tk.Tk()
app = App(root)
root.mainloop()
