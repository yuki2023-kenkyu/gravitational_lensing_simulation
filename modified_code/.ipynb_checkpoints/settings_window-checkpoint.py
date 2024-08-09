import tkinter as tk

class SettingsWindow:
    def __init__(self, parent, distance_l_var, distance_s_var, mass_var, update_callback):
        self.window = tk.Toplevel(parent)
        self.window.title("Settings")

        # スライダー用の変数を保持
        self.distance_l_var = distance_l_var
        self.distance_s_var = distance_s_var
        self.mass_var = mass_var
        self.update_callback = update_callback

        # 初期値を保存
        self.initial_distance_l = distance_l_var.get()
        self.initial_distance_s = distance_s_var.get()
        self.initial_mass = mass_var.get()

        # スライダーの作成
        self.distance_l_slider = tk.Scale(self.window, from_=100, to=1000, orient=tk.HORIZONTAL, label="Black Hole Distance (pc)", variable=self.distance_l_var)
        self.distance_l_slider.pack(side="top", padx=5, pady=5)

        self.distance_s_slider = tk.Scale(self.window, from_=1000, to=10000, orient=tk.HORIZONTAL, label="Source Distance (pc)", variable=self.distance_s_var)
        self.distance_s_slider.pack(side="top", padx=5, pady=5)

        self.mass_slider = tk.Scale(self.window, from_=10**9, to=10**12, orient=tk.HORIZONTAL, label="Black Hole Mass (Msun)", resolution=10**9, variable=self.mass_var)
        self.mass_slider.pack(side="top", padx=5, pady=5)

        # 更新ボタンとリセットボタンの追加
        self.update_button = tk.Button(self.window, text="Update", command=self.update_parameters)
        self.update_button.pack(side="left", padx=10, pady=10)

        self.reset_button = tk.Button(self.window, text="Reset", command=self.reset_parameters)
        self.reset_button.pack(side="right", padx=10, pady=10)

        # 閉じるボタン
        self.close_button = tk.Button(self.window, text="Close", command=self.window.destroy)
        self.close_button.pack(side="bottom", pady=10)

    def update_parameters(self):
        # パラメータを更新して再計算をトリガー
        self.update_callback(force_update=True)

    def reset_parameters(self):
        # スライダーを初期値に戻す
        self.distance_l_var.set(self.initial_distance_l)
        self.distance_s_var.set(self.initial_distance_s)
        self.mass_var.set(self.initial_mass)
        self.update_callback(force_update=True)
