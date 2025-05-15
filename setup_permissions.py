#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import subprocess
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, 
                            QPushButton, QMessageBox, QDialog)
from PyQt6.QtCore import Qt, QProcess, QUrl
from PyQt6.QtGui import QPixmap, QDesktopServices

class PermissionSetupDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("屏幕教鞭权限设置")
        self.setMinimumWidth(500)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # 说明标签
        info_label = QLabel(
            "使用屏幕教鞭需要macOS的屏幕录制权限，请按照以下步骤设置："
        )
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        # 步骤说明
        steps = [
            "1. 点击下方\"打开系统偏好设置\"按钮",
            "2. 在隐私与安全性中选择\"屏幕录制\"",
            "3. 点击左下角锁图标并用Touch ID或密码解锁",
            "4. 勾选\"Terminal\"或\"Python\"(取决于您启动应用的方式)",
            "5. 退出系统偏好设置并重新启动屏幕教鞭应用"
        ]
        
        for step in steps:
            step_label = QLabel(step)
            layout.addWidget(step_label)
        
        # 打开系统偏好设置的按钮
        open_prefs_btn = QPushButton("打开系统偏好设置")
        open_prefs_btn.clicked.connect(self.open_system_preferences)
        layout.addWidget(open_prefs_btn)
        
        # Python路径
        python_path = sys.executable
        path_label = QLabel(f"您的Python路径: {python_path}")
        path_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(path_label)
        
        # 启动方式
        terminal_path = "/Applications/Utilities/Terminal.app"
        terminal_label = QLabel(f"如果您通过Terminal启动，也需要为Terminal添加权限")
        layout.addWidget(terminal_label)
        
        # 确定按钮
        ok_btn = QPushButton("我已完成设置，重新启动应用")
        ok_btn.clicked.connect(self.restart_app)
        layout.addWidget(ok_btn)
        
        # 设置布局
        self.setLayout(layout)
    
    def open_system_preferences(self):
        # macOS Ventura及以后使用这个路径
        try:
            # 先尝试打开新版系统设置
            QDesktopServices.openUrl(QUrl("x-apple.systempreferences:com.apple.preference.security?Privacy_ScreenCapture"))
        except:
            # 如果失败，尝试打开旧版系统偏好设置
            try:
                subprocess.run(["open", "/System/Applications/System Settings.app"])
            except:
                subprocess.run(["open", "/System/Applications/System Preferences.app"])
                
        QMessageBox.information(
            self, 
            "导航提示",
            "请在系统设置中找到\"隐私与安全性\" -> \"屏幕录制\"部分，并为Python和Terminal授予权限。"
        )
    
    def restart_app(self):
        python_path = sys.executable
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.py")
        
        self.accept()
        
        # 退出当前进程
        QApplication.quit()
        
        # 启动新进程
        subprocess.Popen([python_path, script_path])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = PermissionSetupDialog()
    dialog.exec()
