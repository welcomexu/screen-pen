import os
import sys
from PyQt6.QtWidgets import (QMainWindow, QApplication, QWidget, QPushButton, 
                            QVBoxLayout, QHBoxLayout, QColorDialog, QSlider, 
                            QLabel, QComboBox, QMenu, QFileDialog, QMessageBox,
                            QToolButton, QFrame, QSizePolicy, QStatusBar)
from PyQt6.QtCore import Qt, QPoint, QRect, QSize, QEvent
from PyQt6.QtGui import (QPainter, QPen, QColor, QPixmap, QIcon, QAction, 
                        QKeySequence, QShortcut, QCursor, QImage, QBrush)
from .drawing_tools import FreeDraw, Line, Rectangle, Ellipse, Eraser
from .screen_capture import capture_screen

class ControlPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("工具")
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setup_ui()
        
    def setup_ui(self):
        # 主布局使用垂直布局
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(5, 8, 5, 8)  # 减小边距使面板更窄
        self.layout.setSpacing(10)  # 适当减小控件间距
        
        # === 绘图模式开关 ===
        self.draw_mode_btn = QPushButton("开启绘图")
        self.draw_mode_btn.setCheckable(True)  # 让按钮可以切换状态
        self.draw_mode_btn.setStyleSheet("""
            QPushButton {
                background-color: #5cb85c;
                color: white;
                font-weight: bold;
                padding: 6px;
            }
            QPushButton:checked {
                background-color: #d9534f;
                color: white;
            }
        """)
        # 将按钮添加到布局最上方
        self.layout.insertWidget(0, self.draw_mode_btn)
        
        # 在按钮下方添加分隔线
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        self.layout.insertWidget(1, separator)
        
        # === 工具选择区 ===
        self.tool_label = QLabel("工具:")
        self.tool_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.tool_label)
        
        self.tool_combo = QComboBox()
        self.tool_combo.addItems(["画笔", "直线", "矩形", "椭圆", "橡皮"])
        self.tool_combo.setFixedHeight(25)  # 增加高度改善可点击性
        self.tool_combo.setFocusPolicy(Qt.FocusPolicy.StrongFocus)  # 确保能够接收焦点
        self.layout.addWidget(self.tool_combo)
        
        # 添加分隔线
        self.add_separator()
        
        # === 颜色选择区 ===
        self.color_label = QLabel("颜色:")
        self.color_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.color_label)
        
        # 将"选择颜色"改为"颜色"
        self.color_btn = QPushButton("颜色")
        self.layout.addWidget(self.color_btn)
        
        self.color_indicator = QWidget()
        self.color_indicator.setFixedHeight(20)
        self.color_indicator.setStyleSheet("background-color: #FF0000; border: 1px solid #999;")
        self.layout.addWidget(self.color_indicator)
        
        # 添加分隔线
        self.add_separator()
        
        # === 线宽选择区 ===
        self.width_label = QLabel("线宽:")
        self.width_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.width_label)
        
        self.width_slider = QSlider(Qt.Orientation.Horizontal)
        self.width_slider.setRange(1, 20)
        self.width_slider.setValue(6)  # 修改默认值为6
        self.layout.addWidget(self.width_slider)
        
        self.width_value = QLabel("6")  # 修改默认显示值为6
        self.width_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.width_value)
        
        # 添加分隔线
        self.add_separator()
        
        # === 操作按钮区 ===
        # 将"清除全部"改为"清屏"，移除截屏按钮
        self.clear_btn = QPushButton("清屏")
        self.quit_btn = QPushButton("退出")
        
        self.layout.addWidget(self.clear_btn)
        self.layout.addWidget(self.quit_btn)
        
        # 设置按钮样式
        for btn in [self.clear_btn, self.quit_btn]:
            btn.setMinimumHeight(32)  # 稍微调整按钮高度
        
        # 设置信号连接
        self.width_slider.valueChanged.connect(self.update_width_label)
        
        # 设置整体风格和大小
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(240, 240, 240, 230);
            }
            QPushButton {
                padding: 4px;
                border-radius: 4px;
                background-color: rgba(220, 220, 220, 230);
            }
            QPushButton:hover {
                background-color: rgba(200, 200, 200, 230);
            }
            QLabel {
                font-size: 11px;
                font-weight: bold;
            }
            QComboBox {
                padding: 2px;
                border-radius: 4px;
                min-height: 20px;
            }
            QComboBox::drop-down {
                width: 20px;
            }
            QFrame[frameShape="4"] {
                background-color: rgba(180, 180, 180, 150);
                max-height: 1px;
            }
        """)
        
        # 减小固定宽度，使面板更窄
        self.setFixedWidth(80)  # 从100减为80
        
    def add_separator(self):
        """添加水平分隔线"""
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        self.layout.addWidget(separator)
        
    def update_width_label(self, value):
        self.width_value.setText(str(value))
        
    def toggle_draw_mode(self, is_active):
        """切换绘图模式时更新按钮文字"""
        if is_active:
            self.draw_mode_btn.setText("停用绘图")
        else:
            self.draw_mode_btn.setText("开启绘图")
        
    def showEvent(self, event):
        """窗口显示时，设置位置到屏幕右侧"""
        super().showEvent(event)
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        
        # 计算窗口位置，使其位于屏幕右侧中部
        x = screen_geometry.width() - self.width() - 20  # 距离右边缘20像素
        y = (screen_geometry.height() - self.height()) // 2
        
        self.move(x, y)
        

class ScreenPenApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("屏幕教鞭")
        self.setup_drawing_tools()
        self.drawing_mode_active = False  # 默认不启用绘图模式，允许操作其他应用
        self.setup_ui()
        self.setup_shortcuts()
        
    def setup_drawing_tools(self):
        # 初始化绘画参数
        self.current_tool = "画笔"
        self.pen_color = QColor(255, 0, 0)  # 红色
        self.pen_width = 6  # 修改默认线宽为6
        self.drawing = False
        self.last_point = QPoint()
        self.current_shape = None
        
        # 初始化绘图工具
        self.tools = {
            "画笔": FreeDraw(),
            "直线": Line(),
            "矩形": Rectangle(),
            "椭圆": Ellipse(),
            "橡皮": Eraser(),
        }
        
        # 创建画布
        self.canvas = QPixmap()
        
    def setup_ui(self):
        # 获取屏幕尺寸
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        self.screen_width = screen_geometry.width()
        self.screen_height = screen_geometry.height()
        
        # 设置窗口
        self.setGeometry(0, 0, self.screen_width, self.screen_height)
        
        # 修改窗口属性 - 使用合适的窗口类型来支持鼠标事件穿透
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        
        # 设置窗口透明属性
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
        
        # 在初始化时不要设置鼠标事件穿透属性，而是直接将窗口隐藏
        # 这样更彻底地让鼠标事件传递到其他应用程序
        self.setWindowOpacity(0.01)  # 几乎透明但不完全隐藏，以保持窗口活跃
        self.drawing_mode_active = False
        
        # 初始化画布
        self.canvas = QPixmap(self.screen_width, self.screen_height)
        self.canvas.fill(Qt.GlobalColor.transparent)
        
        # 创建控制面板并停靠在右侧
        self.control_panel = ControlPanel()
        self.control_panel.show()
        
        # 添加状态栏，显示当前模式
        self.status_bar = QStatusBar()
        self.status_bar.showMessage("鼠标穿透模式：可操作其他应用")
        self.setStatusBar(self.status_bar)
        self.status_bar.hide()  # 默认隐藏，仅调试时使用
        
        # 连接信号
        self.control_panel.tool_combo.currentTextChanged.connect(self.change_tool)
        self.control_panel.color_btn.clicked.connect(self.change_color)
        self.control_panel.width_slider.valueChanged.connect(self.change_width)
        self.control_panel.clear_btn.clicked.connect(self.clear_canvas)
        self.control_panel.quit_btn.clicked.connect(self.close_app)
        self.control_panel.draw_mode_btn.clicked.connect(self.toggle_drawing_mode)
        
    def toggle_drawing_mode(self, checked):
        """切换绘图模式 - 使用窗口不透明度而不是鼠标事件穿透属性"""
        self.drawing_mode_active = checked
        
        # 更新按钮文字
        self.control_panel.toggle_draw_mode(checked)
        
        if checked:
            # 绘图模式：窗口正常显示，可以绘图
            self.setWindowOpacity(1.0)
            print("已切换到绘图模式")
            self.status_bar.showMessage("绘图模式：可以在屏幕上绘图")
        else:
            # 非绘图模式：窗口几乎不可见，鼠标事件会穿透到其他应用
            self.setWindowOpacity(0.01)  # 非常低的透明度，实质上是隐藏窗口
            print("已切换到鼠标穿透模式")
            self.status_bar.showMessage("鼠标穿透模式：可操作其他应用")
            self.drawing = False  # 确保绘图状态被重置
        
        # 强制刷新
        self.repaint()
        QApplication.processEvents()
    
    def ensure_mouse_transparency(self):
        """确保在非绘图模式下窗口几乎不可见"""
        if not self.drawing_mode_active:
            self.setWindowOpacity(0.01)
            self.repaint()
            QApplication.processEvents()
            print("已重新确认鼠标穿透模式")
    
    def setup_shortcuts(self):
        # ESC键退出
        self.quit_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Escape), self)
        self.quit_shortcut.activated.connect(self.close_app)
        
        # C键清除
        self.clear_shortcut = QShortcut(QKeySequence(Qt.Key.Key_C), self)
        self.clear_shortcut.activated.connect(self.clear_canvas)
        
        # 保留截图快捷键，即使我们移除了按钮
        self.capture_shortcut = QShortcut(QKeySequence(Qt.Key.Key_S), self)
        self.capture_shortcut.activated.connect(self.capture_screen)
        
        # 数字键选择工具
        self.pen_shortcut = QShortcut(QKeySequence(Qt.Key.Key_1), self)
        self.pen_shortcut.activated.connect(lambda: self.quick_change_tool("画笔"))
        
        self.line_shortcut = QShortcut(QKeySequence(Qt.Key.Key_2), self)
        self.line_shortcut.activated.connect(lambda: self.quick_change_tool("直线"))
        
        self.rect_shortcut = QShortcut(QKeySequence(Qt.Key.Key_3), self)
        self.rect_shortcut.activated.connect(lambda: self.quick_change_tool("矩形"))
        
        self.ellipse_shortcut = QShortcut(QKeySequence(Qt.Key.Key_4), self)
        self.ellipse_shortcut.activated.connect(lambda: self.quick_change_tool("椭圆"))
        
        self.eraser_shortcut = QShortcut(QKeySequence(Qt.Key.Key_5), self)
        self.eraser_shortcut.activated.connect(lambda: self.quick_change_tool("橡皮"))
        
        # 添加空格键作为切换绘图模式的快捷键
        self.toggle_drawing_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Space), self)
        self.toggle_drawing_shortcut.activated.connect(self.toggle_draw_shortcut)
        
    def toggle_draw_shortcut(self):
        """通过快捷键切换绘图模式"""
        new_state = not self.drawing_mode_active
        self.control_panel.draw_mode_btn.setChecked(new_state)
        self.toggle_drawing_mode(new_state)
    
    def quick_change_tool(self, tool_name):
        self.current_tool = tool_name
        self.control_panel.tool_combo.setCurrentText(tool_name)
        
    def change_tool(self, tool_name):
        self.current_tool = tool_name
        
    def change_color(self):
        color = QColorDialog.getColor(self.pen_color)
        if color.isValid():
            self.pen_color = color
            self.control_panel.color_indicator.setStyleSheet(f"background-color: {color.name()};")
            
    def change_width(self, width):
        self.pen_width = width
        
    def clear_canvas(self):
        self.canvas.fill(Qt.GlobalColor.transparent)
        self.update()
        
    def capture_screen(self):
        # 暂时隐藏绘图窗口和控制面板
        self.hide()
        self.control_panel.hide()
        
        # 等待一下确保窗口完全隐藏
        QApplication.processEvents()
        
        # 截取屏幕
        screen_image = capture_screen()
        
        # 显示窗口
        self.show()
        self.control_panel.show()
        
        # 保存截图
        if screen_image:
            file_path, _ = QFileDialog.getSaveFileName(self, "保存截图", 
                                                    os.path.expanduser("~/Desktop/screenshot.png"),
                                                    "PNG 图片 (*.png)")
            if file_path:
                screen_image.save(file_path)
                QMessageBox.information(self, "保存成功", f"截图已保存至: {file_path}")
        
    def close_app(self):
        self.control_panel.close()
        self.close()
        QApplication.quit()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        
        # 确保整个区域都能接收鼠标事件，即使是透明的部分
        # 添加半透明背景以便于用户知道窗口已激活
        painter.fillRect(self.rect(), QColor(0, 0, 0, 1))  # 几乎全透明，但不是完全透明
        
        # 绘制当前画布
        painter.drawPixmap(0, 0, self.canvas)
        
        # 如果正在绘制，绘制临时形状
        if self.drawing and self.current_shape:
            if self.current_tool == "橡皮":
                painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
                painter.setPen(QPen(Qt.GlobalColor.transparent, self.pen_width, Qt.PenStyle.SolidLine))
            else:
                painter.setPen(QPen(self.pen_color, self.pen_width, Qt.PenStyle.SolidLine))
                
            self.current_shape.draw(painter)
        
    def mousePressEvent(self, event):
        if not self.drawing_mode_active:
            # 如果不是绘图模式，不处理鼠标事件
            event.ignore()
            return
            
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = True
            self.last_point = event.pos()
            
            # 根据当前工具初始化形状
            self.current_shape = self.tools[self.current_tool]
            self.current_shape.start(event.pos())
            
    def mouseMoveEvent(self, event):
        if not self.drawing_mode_active:
            # 如果不是绘图模式，不处理鼠标事件
            event.ignore()
            return
            
        if event.buttons() & Qt.MouseButton.LeftButton and self.drawing:
            tool = self.tools[self.current_tool]
            
            if self.current_tool == "画笔" or self.current_tool == "橡皮":
                painter = QPainter(self.canvas)
                
                if self.current_tool == "橡皮":
                    painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
                    painter.setPen(QPen(Qt.GlobalColor.transparent, self.pen_width, Qt.PenStyle.SolidLine))
                else:
                    painter.setPen(QPen(self.pen_color, self.pen_width, Qt.PenStyle.SolidLine))
                    
                tool.update(self.last_point, event.pos())
                tool.draw(painter)
                painter.end()
                
                self.last_point = event.pos()
            else:
                # 对于其他形状，更新当前点并重绘
                tool.update(self.last_point, event.pos())
                
            self.update()
            
    def mouseReleaseEvent(self, event):
        if not self.drawing_mode_active:
            # 如果不是绘图模式，不处理鼠标事件
            event.ignore()
            return
            
        if event.button() == Qt.MouseButton.LeftButton and self.drawing:
            if self.current_tool not in ["画笔", "橡皮"]:
                painter = QPainter(self.canvas)
                
                if self.current_tool == "橡皮":
                    painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
                    painter.setPen(QPen(Qt.GlobalColor.transparent, self.pen_width, Qt.PenStyle.SolidLine))
                else:
                    painter.setPen(QPen(self.pen_color, self.pen_width, Qt.PenStyle.SolidLine))
                    
                self.current_shape.update(self.last_point, event.pos())
                self.current_shape.draw(painter)
                painter.end()
                
            self.drawing = False
            self.current_shape = None
            self.update()
    
    def eventFilter(self, obj, event):
        if obj == self.control_panel and event.type() in [QEvent.Type.MouseButtonPress, 
                                                         QEvent.Type.MouseButtonRelease,
                                                         QEvent.Type.MouseMove]:
            # 在控制面板区域，让事件正常处理
            return False
        return super().eventFilter(obj, event)
    
    def showEvent(self, event):
        """窗口显示时确保正确的透明度设置"""
        super().showEvent(event)
        # 根据当前模式设置透明度
        if not self.drawing_mode_active:
            self.setWindowOpacity(0.01)
        else:
            self.setWindowOpacity(1.0)
        QApplication.processEvents()
