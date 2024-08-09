import numpy as np
import astropy.constants as c
import astropy.units as u

# 定数の定義
radtoarcsec = 206265
arcsectorad = 1/radtoarcsec

def calculate_einstein_radius(M, D_L, D_S):
    D_LS = np.abs(D_S - D_L)  # ブラックホールからソースまでの距離
    G = c.G
    C = c.c.to(u.m/u.s)
    R_E = np.sqrt((4 * G * M * D_LS) / ((C**2) * D_L * D_S)).decompose().value * radtoarcsec  # アインシュタイン半径 [arcsec]
    return R_E

def invlensed_pixel_vectorized(image_data, pixel_coords, image_pixel_Center, pixel_Size, R_E, D_S):
    """ベクトル化された重力レンズ効果"""
    dx = (pixel_coords[:, 0] - image_pixel_Center[0]) * pixel_Size / D_S.to_value(u.pc)
    dy = (pixel_coords[:, 1] - image_pixel_Center[1]) * pixel_Size / D_S.to_value(u.pc)
    r = np.sqrt(dx**2 + dy**2)
    
    theta = np.arctan(r) * radtoarcsec  # 角度 [arcsec]
    
    # ゼロ除算を避けるために、非常に小さい theta に対する処理を追加
    small_angle_threshold = 1e-10  # 閾値を設定
    theta_safe = np.where(theta < small_angle_threshold, small_angle_threshold, theta)
    
    beta = theta_safe - (R_E**2 / theta_safe)  # 修正された角度 [arcsec]
    
    factor = beta / theta_safe
    x_new = image_pixel_Center[0] + (pixel_coords[:, 0] - image_pixel_Center[0]) * factor
    y_new = image_pixel_Center[1] + (pixel_coords[:, 1] - image_pixel_Center[1]) * factor
    
    # 無効な座標を扱うために、NaN をゼロに置き換える
    x_new = np.nan_to_num(x_new, nan=image_pixel_Center[0])
    y_new = np.nan_to_num(y_new, nan=image_pixel_Center[1])
    
    return np.stack((x_new, y_new), axis=-1).astype(int)

def generate_lensed_image_vectorized(image_data, distance_l, distance_s, mass):
    D_L = distance_l * u.pc
    D_S = distance_s * u.pc
    M = mass * u.Msun
    R_E = calculate_einstein_radius(M, D_L, D_S)
    
    image_Mat_Len = image_data.shape[0]
    image_pixel_Center = np.array([image_Mat_Len / 2, image_Mat_Len / 2])
    image_Ang_Size = 2.0 * R_E
    image_Length = 2 * np.tan(image_Ang_Size * arcsectorad) * D_S.to_value(u.pc)  # 実際のサイズ [pc]
    pixel_Size = image_Length / image_Mat_Len

    pixel_coords = np.indices((image_Mat_Len, image_Mat_Len)).reshape(2, -1).T
    lensed_coords = invlensed_pixel_vectorized(image_data, pixel_coords, image_pixel_Center, pixel_Size, R_E, D_S)
    
    valid_mask = (
        (lensed_coords[:, 0] >= 0) & (lensed_coords[:, 0] < image_Mat_Len) &
        (lensed_coords[:, 1] >= 0) & (lensed_coords[:, 1] < image_Mat_Len)
    )
    
    lensed_image = np.zeros_like(image_data)
    lensed_image[pixel_coords[valid_mask, 0], pixel_coords[valid_mask, 1]] = \
        image_data[lensed_coords[valid_mask, 0], lensed_coords[valid_mask, 1]]
    
    return lensed_image
