import numpy as np
import cv2

def schwarzschild_lens_effect(frame, Rs=50, center=None, fill_inside_horizon=False):
    h, w, _ = frame.shape
    # 画像の中心を求める
    # centerが指定されていない場合、画像の中心を重心として設定します。wは画像の幅、hは高さです。
    if center is None:
        center = (w // 2, h // 2)
    # グリッドの作成
    # XとYは画像の各ピクセルの座標を表します。ogridを使って、YとXのグリッドを作成します。これにより、画像の全てのピクセルの位置を取得します。その後、これらの座標から重心の位置を引いて、重心を基準とした相対座標に変換します。
    Y, X = np.ogrid[:h, :w]
    X = X - center[0]
    Y = Y - center[1]
    
    # 各ピクセルの距離と角度を計算
    # 各ピクセルの重心からの距離rと角度thetaを計算します。rはピクセルの重心からの直線距離で、thetaは重心から見たときの角度です。
    r = np.sqrt(X**2 + Y**2)
    theta = np.arctan2(Y, X)
    
    # レンズ効果を計算
    # r_lensedは、レンズ効果によって変形された後の距離を表します。Rsはシュバルツシルト半径で、ブラックホールの重力の強さを示します。r_lensedは、もとの距離rに対してシュバルツシルト半径を基にした変形を加えています。np.log(r / Rs)は対数をとることで、距離が近いほど強く、遠いほど弱く変形する効果を与えています。
    r = np.maximum(r, 1)  # Avoid divide by zero
    r_lensed = r - Rs * np.log(r / Rs)
    r_lensed = np.maximum(r_lensed, 1)  # Avoid negative or zero radius
    
    # シュバルツシルト半径内を黒く塗りつぶす
    if fill_inside_horizon:
        inside_horizon = r < Rs
        frame[inside_horizon] = [0, 0, 0]
    
    # 新しい座標を計算
    # 変形後の距離と元の角度を使って、新しい座標X_lensedとY_lensedを計算します。これにより、各ピクセルがどこに移動するかを決定します。
    X_lensed = r_lensed * np.cos(theta) + center[0]
    Y_lensed = r_lensed * np.sin(theta) + center[1]
    
    # 画像を再マップ
    # 新しい座標に基づいて、元の画像を再マップします。np.clipで座標を範囲内に収め、cv2.remap関数を使って、各ピクセルを新しい位置に移動させます。cv2.INTER_LINEARは、ピクセル値を線形補間する方法です。
    map_x = np.clip(X_lensed, 0, w - 1).astype(np.float32)
    map_y = np.clip(Y_lensed, 0, h - 1).astype(np.float32)
    
    lensed_frame = cv2.remap(frame, map_x, map_y, interpolation=cv2.INTER_LINEAR)
    return lensed_frame

def kerr_lens_effect(frame, Rs=50, a=0.5, center=None, fill_inside_horizon=False):
    h, w, _ = frame.shape
    if center is None:
        center = (w // 2, h // 2)
    
    Y, X = np.ogrid[:h, :w]
    X = X - center[0]
    Y = Y - center[1]
    r = np.sqrt(X**2 + Y**2)
    theta = np.arctan2(Y, X)
    
    r = np.maximum(r, 1)  # Avoid divide by zero
    r_lensed = r - Rs * np.log(r / Rs) * (1 - a * np.sin(theta))
    r_lensed = np.maximum(r_lensed, 1)  # Avoid negative or zero radius
    
     # シュバルツシルト半径内を黒く塗りつぶす
    if fill_inside_horizon:
        inside_horizon = r < Rs
        frame[inside_horizon] = [0, 0, 0]
    
    X_lensed = r_lensed * np.cos(theta) + center[0]
    Y_lensed = r_lensed * np.sin(theta) + center[1]
    
    map_x = np.clip(X_lensed, 0, w - 1).astype(np.float32)
    map_y = np.clip(Y_lensed, 0, h - 1).astype(np.float32)
    
    lensed_frame = cv2.remap(frame, map_x, map_y, interpolation=cv2.INTER_LINEAR)
    return lensed_frame
