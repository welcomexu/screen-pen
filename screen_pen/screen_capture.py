import io
import time
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QBuffer, QByteArray
from PyQt6.QtGui import QImage, QPixmap
from Quartz import (CGWindowListCopyWindowInfo, kCGWindowListOptionOnScreenOnly, kCGNullWindowID,
                   CGDisplayCreateImage, CGMainDisplayID, CGImageGetWidth, CGImageGetHeight,
                   CGImageGetBytesPerRow, CGImageGetDataProvider, CGDataProviderCopyData)

def capture_screen():
    """捕获整个屏幕并返回QImage"""
    # 使用Quartz直接截取屏幕
    try:
        display_id = CGMainDisplayID()
        image_ref = CGDisplayCreateImage(display_id)
        
        # 转换为QImage - 使用正确的Quartz函数
        width = CGImageGetWidth(image_ref)
        height = CGImageGetHeight(image_ref)
        bytes_per_row = CGImageGetBytesPerRow(image_ref)
        
        # 获取像素数据
        data_provider = CGImageGetDataProvider(image_ref)
        pixel_data = CGDataProviderCopyData(data_provider)
        
        # 将CGImage数据转换为QImage
        q_image = QImage(pixel_data, width, height, bytes_per_row, QImage.Format.Format_ARGB32)
        
        # 适应Qt的BGRA与macOS的ARGB格式转换
        return q_image.rgbSwapped()
    except Exception as e:
        print(f"截图失败: {e}")
        return None
