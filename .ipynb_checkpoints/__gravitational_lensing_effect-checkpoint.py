import numpy as np
import cv2
from geodesic import schwarzschild_geodesic, kerr_geodesic

def schwarzschild_lens_effect(frame, Rs=50, center=None, fill_inside_horizon=False):
    h, w, _ = frame.shape
    if center is None:
        center = (w // 2, h // 2)

    Y, X = np.ogrid[:h, :w]
    X = X - center[0]
    Y = Y - center[1]
    r = np.sqrt(X**2 + Y**2)
    theta = np.arctan2(Y, X)
    
    # 初期条件と時間の範囲を設定
    initial_conditions = [r, theta, 0, 0, 0, 0]
    t_span = [0, 10]
    
    # シュバルツシルト測地線を計算
    sol = schwarzschild_geodesic(Rs, initial_conditions, t_span)
    r_lensed = sol(t_span)[0]
    theta_lensed = sol(t_span)[1]
    
    if fill_inside_horizon:
        inside_horizon = r < Rs
        frame[inside_horizon] = [0, 0, 0]
    
    X_lensed = r_lensed * np.cos(theta_lensed) + center[0]
    Y_lensed = r_lensed * np.sin(theta_lensed) + center[1]
    
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
    
    # 初期条件と時間の範囲を設定
    initial_conditions = [r, theta, 0, 0, 0, 0]
    t_span = [0, 10]
    
    # Kerr測地線を計算
    sol = kerr_geodesic(Rs, a, initial_conditions, t_span)
    r_lensed = sol(t_span)[0]
    theta_lensed = sol(t_span)[1]
    
    if fill_inside_horizon:
        inside_horizon = r < Rs
        frame[inside_horizon] = [0, 0, 0]
    
    X_lensed = r_lensed * np.cos(theta_lensed) + center[0]
    Y_lensed = r_lensed * np.sin(theta_lensed) + center[1]
    
    map_x = np.clip(X_lensed, 0, w - 1).astype(np.float32)
    map_y = np.clip(Y_lensed, 0, h - 1).astype(np.float32)
    
    lensed_frame = cv2.remap(frame, map_x, map_y, interpolation=cv2.INTER_LINEAR)
    return lensed_frame
