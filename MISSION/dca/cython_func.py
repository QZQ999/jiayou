"""
纯Python版本的cython_func - Windows兼容
替代 cython_func.pyx，无需编译

功能：激光命中检测（扇形区域）
"""
import numpy as np

PI = np.pi

def reg_rad(rad):
    """规范化弧度到 [-π, π] 范围"""
    return (rad + PI) % (2 * PI) - PI

def laser_hit_improve3(pos_o, pos_t, fanRadius, fanOpenRad, fanDirRad):
    """
    检测激光是否命中目标（扇形检测）

    参数:
        pos_o: 发射者位置 [x, y]
        pos_t: 目标位置 [x, y]
        fanRadius: 扇形半径
        fanOpenRad: 扇形张角（弧度）
        fanDirRad: 扇形朝向（弧度）

    返回:
        bool: 是否命中
    """
    # 计算距离平方
    delta = pos_t - pos_o
    dis_square = delta[0]**2 + delta[1]**2

    # 检查距离
    if dis_square > fanRadius**2:
        return False

    # 计算扇形边界角度
    ori_rad_pos = fanDirRad + fanOpenRad / 2
    ori_rad_neg = fanDirRad - fanOpenRad / 2

    # 计算目标方向角度
    ori_2tgt = np.arctan2(delta[1], delta[0])

    # 检查角度差
    d1rad = abs(reg_rad(ori_rad_pos - ori_2tgt))
    d2rad = abs(reg_rad(ori_rad_neg - ori_2tgt))

    if d1rad <= fanOpenRad and d2rad <= fanOpenRad:
        return True
    else:
        return False
