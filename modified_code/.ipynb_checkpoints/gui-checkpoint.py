import cv2
import numpy as np
import tkinter as tk
from tkinter import Label, messagebox
from PIL import Image, ImageTk
from lens_simulation import generate_lensed_image_vectorized
from settings_window import SettingsWindow

class MainApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        self.window.geometry("1280x720")
        self.video_source = 0
        
        self.vid = cv2.VideoCapture(self.video_source)

        # カメラデバイスが正常に読み込まれているかテスト
        if not self.vid.isOpened():
            messagebox.showerror("Error", "Cannot open video source")
            self.window.destroy()
            return

        # メインフレームを作成（画像とボタンを分けるため）
        self.main_frame = tk.Frame(window)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # 画像表示用のフレームを作成
        self.image_frame = tk.Frame(self.main_frame)
        self.image_frame.pack(fill=tk.BOTH, expand=True)

        # 2つの画像表示ラベル
        self.label_original = Label(self.image_frame)
        self.label_original.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.label_lensed = Label(self.image_frame)
        self.label_lensed.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # グリッドの列の重みを設定して、ラベルがウィンドウのサイズ変更に対応するようにする
        self.image_frame.grid_columnconfigure(0, weight=1)
        self.image_frame.grid_columnconfigure(1, weight=1)
        self.image_frame.grid_rowconfigure(0, weight=1)

        # ボタン用のフレームを作成
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.X, pady=10)

        # 設定ウィンドウを開くボタン
        self.settings_button = tk.Button(self.button_frame, text="Settings", command=self.open_settings_window)
        self.settings_button.pack(side=tk.LEFT, padx=10)

        # 終了ボタンの追加
        self.quit_button = tk.Button(self.button_frame, text="Quit", command=self.on_closing)
        self.quit_button.pack(side=tk.RIGHT, padx=10)

        # パラメータを保持する変数の初期化
        self.distance_l = tk.DoubleVar(value=500)
        self.distance_s = tk.DoubleVar(value=3000)
        self.mass = tk.DoubleVar(value=10**11)

        # メインウィンドウが開かれると同時に設定ウィンドウを開く
        self.open_settings_window()

        self.update()

    def open_settings_window(self):
        # 設定ウィンドウを開く
        SettingsWindow(self.window, self.distance_l, self.distance_s, self.mass, self.update)

    def update(self, force_update=False):
        ret, frame = self.vid.read()
        
        # フレームを正常に取得できたかテスト
        if not ret:
            messagebox.showerror("Error", "Cannot read frame from video source")
            self.on_closing()
            return
        
        # フレームの最小サイドを基に画像を正方形にクロップ
        image_min_side_inxlength = min(frame.shape[:2])
        image_data = frame[:image_min_side_inxlength, :image_min_side_inxlength]

        # BGRからRGBに変換
        image_data_rgb = cv2.cvtColor(image_data, cv2.COLOR_BGR2RGB)

        # スライダーの値を取得してパラメータを設定
        distance_l = self.distance_l.get()
        distance_s = self.distance_s.get()
        mass = self.mass.get()

        # 重力レンズ効果を適用
        lensed_image = generate_lensed_image_vectorized(image_data_rgb, distance_l, distance_s, mass)

        # 画像のサイズをウィンドウに合わせてリサイズ
        image_original = Image.fromarray(image_data_rgb).resize((self.label_original.winfo_width(), self.label_original.winfo_height()), Image.ANTIALIAS)
        image_lensed = Image.fromarray(lensed_image).resize((self.label_lensed.winfo_width(), self.label_lensed.winfo_height()), Image.ANTIALIAS)

        # 画像の表示（オリジナル）
        photo_original = ImageTk.PhotoImage(image=image_original)
        self.label_original.config(image=photo_original)
        self.label_original.image = photo_original

        # 画像の表示（レンズ効果適用後）
        photo_lensed = ImageTk.PhotoImage(image=image_lensed)
        self.label_lensed.config(image=photo_lensed)
        self.label_lensed.image = photo_lensed

        # 通常の定期更新を行う場合
        if not force_update:
            self.window.after(10, self.update)

    def on_closing(self):
        # カメラデバイスを解放
        if self.vid.isOpened():
            self.vid.release()
        self.window.destroy()

    def __del__(self):
        # アプリケーションが終了する際にカメラデバイスを解放
        if self.vid.isOpened():
            self.vid.release()
