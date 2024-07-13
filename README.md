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

### `main.py`

このファイルには、Tkinterを使用してGUIを構築し、カメラ映像に重力レンズ効果をリアルタイムで適用するためのコードが含まれています。

- `ParameterWindow`: ユーザーがブラックホールのパラメーターを調整するためのウィンドウを提供します。
- `ImageWindow`: 重力レンズ効果を適用した映像を表示するウィンドウを提供します。
- `App`: アプリケーションのメインクラスで、パラメーターウィンドウと画像表示ウィンドウを管理します。

## 実行方法

1. `black_hole_effect.py`と`main.py`を同じディレクトリに配置してください。
2. 以下のコードをコマンドプロンプト内で実行してください。
```bash
python main.py
```

## 使用方法

1. アプリケーションを実行すると、2つのウィンドウが表示されます。
   - `パラメーター設定ウィンドウ`: ここでブラックホールのパラメーターを調整できます。
   - `画像表示ウィンドウ`: 調整したパラメーターに基づいて重力レンズ効果が適用された映像が表示されます。
2. `パラメーター設定ウィンドウ`でスライダーを使用して以下のパラメーターを調整できます。
   - シュバルツシルト半径
   - レンズ天体のX位置
   - レンズ天体のY位置
   - Kerrパラメータ a
   - ウィンドウサイズ
3. `更新`ボタンを押すと、設定したパラメーターに基づいて画像が更新されます。

## 注意事項
- カメラが接続されていない場合、アプリケーションはエラーを出力して終了します。カメラが正しく接続されていることを確認してください。
- ウィンドウサイズの変更により、パフォーマンスに影響を与える可能性があります。適切なサイズを選択してください。
