import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
from gravitational_lensing_effect import schwarzschild_lens_effect, kerr_lens_effect

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
        if not ret:
            print("フレームを取得できません。")
            self.master.after(1000, self.update)  # 1秒後に再試行
            return

        if self.app.bh_type == 1:
            lensed_frame = schwarzschild_lens_effect(frame, Rs=self.app.Rs, center=(self.app.lens_x, self.app.lens_y), fill_inside_horizon=self.app.fill_inside_horizon)
        else:
            lensed_frame = kerr_lens_effect(frame, Rs=self.app.Rs, a=self.app.a, center=(self.app.lens_x, self.app.lens_y), fill_inside_horizon=self.app.fill_inside_horizon)

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
