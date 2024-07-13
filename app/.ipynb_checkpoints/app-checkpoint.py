import cv2
from tkinter import Toplevel
from .parameter_window import ParameterWindow
from .image_window import ImageWindow

class App:
    def __init__(self, root, device_index=0):
        self.root = root
        self.cap = cv2.VideoCapture(device_index)
        if not self.cap.isOpened():
            print(f"カメラデバイス {device_index} を開くことができません。")
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

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        self.cap.release()
        self.root.quit()
        self.root.destroy()

    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()
