import numpy as np
import cv2

def schwarzschild_lens_effect(frame, Rs=50, center=None):
    h, w, _ = frame.shape
    if center is None:
        center = (w // 2, h // 2)
    
    Y, X = np.ogrid[:h, :w]
    X = X - center[0]
    Y = Y - center[1]
    r = np.sqrt(X**2 + Y**2)
    theta = np.arctan2(Y, X)
    
    r = np.maximum(r, 1)  # Avoid divide by zero
    r_lensed = r - Rs * np.log(r / Rs)
    r_lensed = np.maximum(r_lensed, 1)  # Avoid negative or zero radius
    
    X_lensed = r_lensed * np.cos(theta) + center[0]
    Y_lensed = r_lensed * np.sin(theta) + center[1]
    
    map_x = np.clip(X_lensed, 0, w - 1).astype(np.float32)
    map_y = np.clip(Y_lensed, 0, h - 1).astype(np.float32)
    
    lensed_frame = cv2.remap(frame, map_x, map_y, interpolation=cv2.INTER_LINEAR)
    return lensed_frame

def kerr_lens_effect(frame, Rs=50, a=0.5, center=None):
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
    
    X_lensed = r_lensed * np.cos(theta) + center[0]
    Y_lensed = r_lensed * np.sin(theta) + center[1]
    
    map_x = np.clip(X_lensed, 0, w - 1).astype(np.float32)
    map_y = np.clip(Y_lensed, 0, h - 1).astype(np.float32)
    
    lensed_frame = cv2.remap(frame, map_x, map_y, interpolation=cv2.INTER_LINEAR)
    return lensed_frame
