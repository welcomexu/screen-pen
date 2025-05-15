#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import time
import subprocess
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QTimer, Qt
from screen_pen.app import ScreenPenApp

def check_screen_recording_permission():
    """检查屏幕录制权限"""
    try:
        # 尝试截图，如果没有权限会抛出异常
        from screen_pen.screen_capture import capture_screen
        test_image = capture_screen()
        if test_image is not None:
            return True
    except Exception as e:
        print(f"权限检查错误: {e}")
        return False
    return False

def run_permission_setup():
    """运行权限设置向导"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    setup_script = os.path.join(script_dir, "setup_permissions.py")
    
    if os.path.exists(setup_script):
        python_path = sys.executable
        subprocess.run([python_path, setup_script])
    else:
        print("找不到权限设置脚本")

if __name__ == "__main__":
    # 使用新版本的高 DPI 支持方式
    # PyQt6 中已废弃 AA_EnableHighDpiScaling，改用 QApplication.setHighDpiScaleFactorRoundingPolicy
    if hasattr(Qt, 'HighDpiScaleFactorRoundingPolicy'):  # 检查属性是否存在
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    
    # AA_UseHighDpiPixmaps 仍然存在，但为了安全也加入检查
    if hasattr(Qt.ApplicationAttribute, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
    
    app = QApplication(sys.argv)
    
    # 检查屏幕录制权限
    if not check_screen_recording_permission():
        result = QMessageBox.question(
            None,
            "需要设置权限",
            "屏幕教鞭需要屏幕录制权限才能正常工作。\n是否现在设置权限？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if result == QMessageBox.StandardButton.Yes:
            run_permission_setup()
            sys.exit(0)  # 退出当前进程，权限设置完成后会重新启动应用
    
    # 创建屏幕教鞭应用
    screen_pen = ScreenPenApp()
    screen_pen.show()
    
    # 使用定时器确保窗口显示在最前端和正确设置不透明度
    def ensure_visible():
        screen_pen.raise_()
        screen_pen.activateWindow()
        # 确保初始状态为非绘图模式
        if not screen_pen.drawing_mode_active:
            screen_pen.setWindowOpacity(0.01)
        QApplication.processEvents()
    
    # 设置定时器，延迟100毫秒后确保窗口可见
    QTimer.singleShot(100, ensure_visible)
    
    # 再次确认设置正确
    QTimer.singleShot(500, lambda: screen_pen.ensure_mouse_transparency())
    QTimer.singleShot(1000, lambda: screen_pen.ensure_mouse_transparency())
    QTimer.singleShot(2000, lambda: screen_pen.ensure_mouse_transparency())
    
    sys.exit(app.exec())
