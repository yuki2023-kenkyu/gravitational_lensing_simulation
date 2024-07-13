﻿# gravitational_lensing_simulation

このプロジェクトは、リアルタイムでカメラ映像にブラックホールの重力レンズ効果を適用し、シュバルツシルトおよびKerrブラックホールの効果をシミュレートするPythonアプリケーションです。

## 実行環境

このアプリケーションを実行するには、以下の環境が必要です。

- Python 3.6以上
- OpenCV
- NumPy
- Tkinter (Pythonに標準で含まれています)
- Pillow (PIL)

## インストール

必要なライブラリをインストールするために、以下のコマンドを実行してください。

```bash
pip install numpy opencv-python pillow
```

## モジュールの説明

### `black_hole_effect.py`

このモジュールには、ブラックホールの重力レンズ効果をシミュレートする関数が含まれています。

- `schwarzschild_lens_effect(frame, Rs=50, center=None)`: シュバルツシルトブラックホールの重力レンズ効果を適用します。
- `kerr_lens_effect(frame, Rs=50, a=0.5, center=None)`: Kerrブラックホールの重力レンズ効果を適用します。
