#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主窗口模块
"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel, 
    QPushButton, QLineEdit, QTextEdit, QListWidget, QCheckBox, QSpinBox, 
    QFileDialog, QMessageBox, QTabWidget, QFormLayout, QDateTimeEdit, QProgressBar, QComboBox
)
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QFont
import os
import time

from encryption.encryptor import Encryptor
from file_handler.file_processor import FileProcessor
from security.machine_bind import MachineBinder
from security.self_destruct import SelfDestructor


class MainWindow(QMainWindow):
    """主窗口类"""
    
    def __init__(self):
        super().__init__()
        
        # 初始化语言支持
        self.current_language = "zh_CN"  # 默认中文
        self.language_dict = {
            "zh_CN": {
                "app_title": "Dada v.1.0.1",
                "tab_encrypt": "🔒 加密",
                "tab_decrypt": "🔓 解密",
                "tab_security": "🛡️ 安全设置",
                "tab_prank": "🎭 高级功能",
                "tab_packaging": "📦 打包工具",
                "drag_drop_area": "拖放文件到此处",
                "added_files": "已添加的文件:",
                "encryption_levels": "加密层数:",
                "key_placeholder": "第{layer}层密钥",
                "add_file": "添加文件",
                "remove_file": "移除文件",
                "clear_files": "清空列表",
                "start_encrypt": "开始加密",
                "max_attempts": "最大失败尝试次数:",
                "decrypt_levels": "加密层数:",
                "select_encrypted_file": "选择加密文件",
                "start_decrypt": "开始解密",
                "decrypt_result": "解密结果将显示在这里...",
                "machine_bind": "机器绑定",
                "enable_machine_bind": "启用机器绑定",
                "current_machine_id": "当前机器ID: {machine_id}",
                "self_destruct": "自毁机制",
                "enable_self_destruct": "启用自毁机制",
                "self_destruct_sequence": "自毁序列: destroy, 自毁, selfdestruct, @#$DESTROY@#$",
                "decoy_generation": "诱饵文档生成",
                "generate_decoys": "生成诱饵文档",
                "decoy_count": "诱饵文档数量:",
                "prank_effects": "恶作剧效果",
                "fake_error": "显示虚假错误信息",
                "random_popup": "随机弹出窗口",
                "change_desktop": "更改桌面背景",
                "packaging_settings": "打包设置",
                "script_path": "Python脚本路径:",
                "browse": "浏览",
                "output_dir": "输出目录:",
                "packaging_options": "打包选项",
                "onefile_mode": "单文件模式",
                "windowed_mode": "窗口模式（无控制台）",
                "include_deps": "包含依赖库",
                "start_packaging": "开始打包",
                "encryption_in_progress": "正在加密: {file_path}",
                "encryption_completed": "加密完成",
                "decryption_in_progress": "正在解密: {file_path}",
                "decryption_completed": "解密完成",
                "select_decoys_output_dir": "选择诱饵文档输出目录",
                "decoys_generated": "已生成 {decoy_count} 个诱饵文档！",
                "security_level": "安全级别",
                "language": "语言",
                "confirm_exit": "退出",
                "confirm_exit_message": "确定要退出应用吗？",
                "yes": "是",
                "no": "否",
                "warning": "警告",
                "no_files_added": "请先添加要加密的文件！",
                "no_encrypted_file_selected": "请先选择要解密的文件！",
                "no_key_entered": "请输入第{i+1}层密钥！"
            },
            "en_US": {
                "app_title": "Dada v.1.0.1",
                "tab_encrypt": "🔒 Encrypt",
                "tab_decrypt": "🔓 Decrypt",
                "tab_security": "🛡️ Security Settings",
                "tab_prank": "🎭 Advanced Features",
                "tab_packaging": "📦 Packaging Tool",
                "drag_drop_area": "Drop Files Here",
                "added_files": "Added Files:",
                "encryption_levels": "Encryption Levels:",
                "key_placeholder": "Layer {layer} Password",
                "add_file": "Add File",
                "remove_file": "Remove File",
                "clear_files": "Clear List",
                "start_encrypt": "Start Encryption",
                "max_attempts": "Max Failed Attempts:",
                "decrypt_levels": "Encryption Levels:",
                "select_encrypted_file": "Select Encrypted File",
                "start_decrypt": "Start Decryption",
                "decrypt_result": "Decryption results will be displayed here...",
                "machine_bind": "Machine Binding",
                "enable_machine_bind": "Enable Machine Binding",
                "current_machine_id": "Current Machine ID: {machine_id}",
                "self_destruct": "Self-Destruct Mechanism",
                "enable_self_destruct": "Enable Self-Destruct",
                "self_destruct_sequence": "Self-Destruct Sequence: destroy, 自毁, selfdestruct, @#$DESTROY@#$",
                "decoy_generation": "Decoy Document Generation",
                "generate_decoys": "Generate Decoy Documents",
                "decoy_count": "Number of Decoy Documents:",
                "prank_effects": "Prank Effects",
                "fake_error": "Show Fake Error Messages",
                "random_popup": "Random Popup Windows",
                "change_desktop": "Change Desktop Background",
                "packaging_settings": "Packaging Settings",
                "script_path": "Python Script Path:",
                "browse": "Browse",
                "output_dir": "Output Directory:",
                "packaging_options": "Packaging Options",
                "onefile_mode": "One File Mode",
                "windowed_mode": "Windowed Mode (No Console)",
                "include_deps": "Include Dependencies",
                "start_packaging": "Start Packaging",
                "encryption_in_progress": "Encrypting: {file_path}",
                "encryption_completed": "Encryption Completed",
                "decryption_in_progress": "Decrypting: {file_path}",
                "decryption_completed": "Decryption Completed",
                "select_decoys_output_dir": "Select Decoy Documents Output Directory",
                "warning": "Warning",
                "no_files_added": "Please add files to encrypt first!",
                "no_encrypted_file_selected": "Please select an encrypted file first!",
                "no_key_entered": "Please enter the {i+1}th layer key!",
                "decoys_generated": "Generated {decoy_count} decoy documents!",
                "security_level": "Security Level",
                "language": "Language",
                "confirm_exit": "Exit",
                "confirm_exit_message": "Are you sure you want to exit the application?",
                "yes": "Yes",
                "no": "No"
            }
        }
        
        # 初始化各个模块
        self.encryptor = Encryptor()
        self.file_processor = FileProcessor()
        self.machine_binder = MachineBinder()
        self.self_destructor = SelfDestructor()
        
        # 待处理文件列表
        self.files_to_process = []
        
        # 初始化UI
        self.init_ui()
    
    def init_ui(self):
        """初始化UI界面"""
        # 设置窗口标题和大小
        self.setWindowTitle("文件加密应用")
        self.setGeometry(100, 100, 900, 700)
        
        # 设置窗口样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f2f5;
            }
            QWidget {
                font-family: '微软雅黑', 'Segoe UI', Arial, sans-serif;
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid #d0d7de;
                border-radius: 6px;
                margin-top: 10px;
                padding: 10px;
                background-color: #ffffff;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #1f2328;
                font-size: 12px;
            }
            QLabel {
                color: #1f2328;
            }
            QLineEdit {
                border: 1px solid #d0d7de;
                border-radius: 4px;
                padding: 6px 10px;
                background-color: #ffffff;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #1da1f2;
                outline: none;
            }
            QPushButton {
                background-color: #1da1f2;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0d95e8;
            }
            QPushButton:pressed {
                background-color: #0d8bd9;
            }
            QPushButton:disabled {
                background-color: #a0aec0;
            }
            QTabWidget::pane {
                border: 1px solid #d0d7de;
                border-radius: 6px;
                background-color: #ffffff;
            }
            QTabBar::tab {
                background-color: #f0f2f5;
                color: #1f2328;
                padding: 10px 20px;
                margin-right: 2px;
                border-radius: 6px 6px 0 0;
                border: 1px solid #d0d7de;
                border-bottom: none;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background-color: #ffffff;
                color: #1da1f2;
            }
            QTabBar::tab:hover {
                background-color: #e6ecf0;
            }
            QListWidget {
                border: 1px solid #d0d7de;
                border-radius: 4px;
                background-color: #ffffff;
            }
            QSpinBox {
                border: 1px solid #d0d7de;
                border-radius: 4px;
                padding: 6px 10px;
                background-color: #ffffff;
            }
            QSpinBox:focus {
                border-color: #1da1f2;
                outline: none;
            }
            QCheckBox {
                color: #1f2328;
                padding: 4px 0;
            }
            QCheckBox:hover {
                color: #1da1f2;
            }
            QDateTimeEdit {
                border: 1px solid #d0d7de;
                border-radius: 4px;
                padding: 6px 10px;
                background-color: #ffffff;
            }
            QDateTimeEdit:focus {
                border-color: #1da1f2;
                outline: none;
            }
            QTextEdit {
                border: 1px solid #d0d7de;
                border-radius: 4px;
                background-color: #ffffff;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
            }
        """)
        
        # 创建中央部件和主布局
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 创建顶部布局（包含标题和语言选择）
        top_layout = QHBoxLayout()
        top_layout.setSpacing(20)
        
        # 创建标题
        self.title_label = QLabel(self.language_dict[self.current_language]["app_title"])
        self.title_label.setFont(QFont("微软雅黑", 16, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignLeft)
        self.title_label.setStyleSheet("color: #1f2328; margin-bottom: 10px;")
        top_layout.addWidget(self.title_label, 1)
        
        # 创建语言选择下拉框
        self.language_combo = QComboBox()
        self.language_combo.addItems(["中文", "English"])
        self.language_combo.setCurrentIndex(0)
        self.language_combo.currentIndexChanged.connect(self.change_language)
        top_layout.addWidget(QLabel("语言:"))
        top_layout.addWidget(self.language_combo)
        
        main_layout.addLayout(top_layout)
        
        # 创建标签页控件
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.North)
        self.tab_widget.setUsesScrollButtons(True)
        
        # 创建各个标签页
        self.create_encrypt_tab()
        self.create_decrypt_tab()
        self.create_security_tab()
        self.create_prank_tab()
        self.create_packaging_tab()
        
        # 添加标签页到标签页控件
        self.tab_widget.addTab(self.encrypt_tab, self.language_dict[self.current_language]["tab_encrypt"])
        self.tab_widget.addTab(self.decrypt_tab, self.language_dict[self.current_language]["tab_decrypt"])
        self.tab_widget.addTab(self.security_tab, self.language_dict[self.current_language]["tab_security"])
        self.tab_widget.addTab(self.prank_tab, self.language_dict[self.current_language]["tab_prank"])
        self.tab_widget.addTab(self.packaging_tab, self.language_dict[self.current_language]["tab_packaging"])
        
        # 添加标签页控件到主布局
        main_layout.addWidget(self.tab_widget)
        
        # 创建状态栏
        self.statusBar().showMessage("就绪")
        self.statusBar().setStyleSheet("background-color: #f0f2f5; color: #656d76; font-size: 12px;")
        
        # 设置中央部件
        self.setCentralWidget(central_widget)
    
    def create_encrypt_tab(self):
        """创建加密标签页"""
        self.encrypt_tab = QWidget()
        layout = QVBoxLayout(self.encrypt_tab)
        lang = self.language_dict[self.current_language]
        
        # 创建拖放区域
        self.drag_drop_area = QGroupBox(lang["drag_drop_area"])
        drag_drop_layout = QVBoxLayout(self.drag_drop_area)
        self.drag_drop_label = QLabel(f"<center><font size=5>📁 {lang['drag_drop_area']}</font></center>")
        self.drag_drop_label.setStyleSheet("QLabel { border: 2px dashed #aaa; padding: 50px; border-radius: 10px; }")
        self.drag_drop_label.setAcceptDrops(True)
        self.drag_drop_label.dragEnterEvent = self.drag_enter_event
        self.drag_drop_label.dropEvent = self.drop_event
        drag_drop_layout.addWidget(self.drag_drop_label)
        
        # 创建文件列表
        self.file_list = QListWidget()
        drag_drop_layout.addWidget(QLabel(lang["added_files"]))
        drag_drop_layout.addWidget(self.file_list)
        layout.addWidget(self.drag_drop_area)
        
        # 创建加密设置组
        encrypt_settings = QGroupBox("加密设置")
        self.key_inputs_layout = QFormLayout(encrypt_settings)
        
        # 加密层数
        self.encryption_levels = QSpinBox()
        self.encryption_levels.setRange(1, 10)
        self.encryption_levels.setValue(2)
        self.key_inputs_layout.addRow(lang["encryption_levels"], self.encryption_levels)
        
        # 密钥输入区域
        self.key_inputs = []
        for i in range(3):  # 默认显示3个密钥输入框
            key_input = QLineEdit()
            key_input.setEchoMode(QLineEdit.Password)
            key_input.setPlaceholderText(lang["key_placeholder"].format(layer=i+1))
            self.key_inputs.append(key_input)
            self.key_inputs_layout.addRow(f"密钥 {i+1}:", key_input)
        
        # 连接加密层数变化信号
        self.encryption_levels.valueChanged.connect(self.update_key_inputs)
        
        layout.addWidget(encrypt_settings)
        
        # 创建操作按钮组
        button_group = QWidget()
        button_layout = QHBoxLayout(button_group)
        
        self.add_file_btn = QPushButton(lang["add_file"])
        self.add_file_btn.clicked.connect(self.add_file)
        button_layout.addWidget(self.add_file_btn)
        
        self.remove_file_btn = QPushButton(lang["remove_file"])
        self.remove_file_btn.clicked.connect(self.remove_file)
        button_layout.addWidget(self.remove_file_btn)
        
        self.clear_files_btn = QPushButton(lang["clear_files"])
        self.clear_files_btn.clicked.connect(self.clear_files)
        button_layout.addWidget(self.clear_files_btn)
        
        self.encrypt_btn = QPushButton(lang["start_encrypt"])
        self.encrypt_btn.clicked.connect(self.start_encryption)
        self.encrypt_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-weight: bold; }")
        button_layout.addWidget(self.encrypt_btn)
        
        layout.addWidget(button_group)
    
    def create_decrypt_tab(self):
        """创建解密标签页"""
        self.decrypt_tab = QWidget()
        layout = QVBoxLayout(self.decrypt_tab)
        lang = self.language_dict[self.current_language]
        
        # 创建解密设置组
        decrypt_settings = QGroupBox("解密设置")
        self.decrypt_key_inputs_layout = QFormLayout(decrypt_settings)
        
        # 加密层数
        self.decryption_levels = QSpinBox()
        self.decryption_levels.setRange(1, 10)
        self.decryption_levels.setValue(2)
        self.decrypt_key_inputs_layout.addRow(lang["decrypt_levels"], self.decryption_levels)
        
        # 密钥输入区域
        self.decrypt_key_inputs = []
        for i in range(3):  # 默认显示3个密钥输入框
            key_input = QLineEdit()
            key_input.setEchoMode(QLineEdit.Password)
            key_input.setPlaceholderText(lang["key_placeholder"].format(layer=i+1))
            self.decrypt_key_inputs.append(key_input)
            self.decrypt_key_inputs_layout.addRow(f"密钥 {i+1}:", key_input)
        
        # 连接解密层数变化信号
        self.decryption_levels.valueChanged.connect(self.update_decrypt_key_inputs)
        
        layout.addWidget(decrypt_settings)
        
        # 创建操作按钮组
        button_group = QWidget()
        button_layout = QHBoxLayout(button_group)
        
        self.select_encrypted_file_btn = QPushButton(lang["select_encrypted_file"])
        self.select_encrypted_file_btn.clicked.connect(self.select_encrypted_file)
        button_layout.addWidget(self.select_encrypted_file_btn)
        
        self.decrypt_btn = QPushButton(lang["start_decrypt"])
        self.decrypt_btn.clicked.connect(self.start_decryption)
        self.decrypt_btn.setStyleSheet("QPushButton { background-color: #2196F3; color: white; font-weight: bold; }")
        button_layout.addWidget(self.decrypt_btn)
        
        layout.addWidget(button_group)
        
        # 解密结果显示
        self.decrypt_result = QTextEdit()
        self.decrypt_result.setReadOnly(True)
        self.decrypt_result.setPlaceholderText(lang["decrypt_result"])
        layout.addWidget(self.decrypt_result)
    
    def create_security_tab(self):
        """创建安全设置标签页"""
        self.security_tab = QWidget()
        layout = QVBoxLayout(self.security_tab)
        lang = self.language_dict[self.current_language]
        
        # 机器绑定设置
        machine_bind_group = QGroupBox(lang["machine_bind"])
        machine_bind_layout = QVBoxLayout(machine_bind_group)
        
        self.machine_bind_checkbox = QCheckBox(lang["enable_machine_bind"])
        machine_bind_layout.addWidget(self.machine_bind_checkbox)
        
        self.machine_id_label = QLabel(lang["current_machine_id"].format(machine_id=self.machine_binder.machine_id))
        self.machine_id_label.setWordWrap(True)
        machine_bind_layout.addWidget(self.machine_id_label)
        
        layout.addWidget(machine_bind_group)
        
        # 自毁机制设置
        self_destruct_group = QGroupBox(lang["self_destruct"])
        self.destruct_layout = QVBoxLayout(self_destruct_group)
        
        self.self_destruct_checkbox = QCheckBox(lang["enable_self_destruct"])
        self.destruct_layout.addWidget(self.self_destruct_checkbox)
        
        self.max_attempts_spinbox = QSpinBox()
        self.max_attempts_spinbox.setRange(1, 10)
        self.max_attempts_spinbox.setValue(3)
        self.destruct_layout.addWidget(QLabel(lang["max_attempts"]))
        self.destruct_layout.addWidget(self.max_attempts_spinbox)
        
        self.destruct_sequence_label = QLabel(lang["self_destruct_sequence"])
        self.destruct_sequence_label.setWordWrap(True)
        self.destruct_layout.addWidget(self.destruct_sequence_label)
        
        layout.addWidget(self_destruct_group)
    
    def create_prank_tab(self):
        """创建高级功能标签页"""
        self.prank_tab = QWidget()
        layout = QVBoxLayout(self.prank_tab)
        lang = self.language_dict[self.current_language]
        
        # 诱饵文档生成
        decoy_group = QGroupBox(lang["decoy_generation"])
        decoy_layout = QVBoxLayout(decoy_group)
        
        self.generate_decoy_checkbox = QCheckBox(lang["generate_decoys"])
        decoy_layout.addWidget(self.generate_decoy_checkbox)
        
        self.decoy_count_spinbox = QSpinBox()
        self.decoy_count_spinbox.setRange(1, 20)
        self.decoy_count_spinbox.setValue(5)
        decoy_layout.addWidget(QLabel(lang["decoy_count"]))
        decoy_layout.addWidget(self.decoy_count_spinbox)
        
        self.generate_decoy_btn = QPushButton(lang["generate_decoys"])
        self.generate_decoy_btn.clicked.connect(self.generate_decoys)
        decoy_layout.addWidget(self.generate_decoy_btn)
        
        layout.addWidget(decoy_group)
        
        # 恶作剧效果设置
        prank_effects_group = QGroupBox("恶作剧效果")
        prank_effects_layout = QVBoxLayout(prank_effects_group)
        
        self.fake_error_checkbox = QCheckBox("显示虚假错误信息")
        prank_effects_layout.addWidget(self.fake_error_checkbox)
        
        self.random_popup_checkbox = QCheckBox("随机弹出窗口")
        prank_effects_layout.addWidget(self.random_popup_checkbox)
        
        self.change_desktop_checkbox = QCheckBox("更改桌面背景")
        prank_effects_layout.addWidget(self.change_desktop_checkbox)
        
        layout.addWidget(prank_effects_group)
    
    def create_packaging_tab(self):
        """创建EXE打包标签页"""
        self.packaging_tab = QWidget()
        layout = QVBoxLayout(self.packaging_tab)
        
        # 创建打包设置组
        packaging_group = QGroupBox("打包设置")
        packaging_layout = QFormLayout(packaging_group)
        
        self.script_path_edit = QLineEdit()
        packaging_layout.addRow("Python脚本路径:", self.script_path_edit)
        
        self.browse_script_btn = QPushButton("浏览")
        self.browse_script_btn.clicked.connect(self.browse_script)
        packaging_layout.addRow("", self.browse_script_btn)
        
        self.output_dir_edit = QLineEdit()
        packaging_layout.addRow("输出目录:", self.output_dir_edit)
        
        self.browse_output_btn = QPushButton("浏览")
        self.browse_output_btn.clicked.connect(self.browse_output_dir)
        packaging_layout.addRow("", self.browse_output_btn)
        
        layout.addWidget(packaging_group)
        
        # 创建打包选项组
        options_group = QGroupBox("打包选项")
        options_layout = QVBoxLayout(options_group)
        
        self.onefile_checkbox = QCheckBox("单文件模式")
        options_layout.addWidget(self.onefile_checkbox)
        
        self.windowed_checkbox = QCheckBox("窗口模式（无控制台）")
        options_layout.addWidget(self.windowed_checkbox)
        
        self.include_checkbox = QCheckBox("包含依赖库")
        options_layout.addWidget(self.include_checkbox)
        
        layout.addWidget(options_group)
        
        # 创建打包按钮
        self.packaging_btn = QPushButton("开始打包")
        self.packaging_btn.clicked.connect(self.start_packaging)
        self.packaging_btn.setStyleSheet("QPushButton { background-color: #FF9800; color: white; font-weight: bold; }")
        layout.addWidget(self.packaging_btn)
        
        # 创建进度条
        self.packaging_progress = QProgressBar()
        self.packaging_progress.setVisible(False)
        layout.addWidget(self.packaging_progress)
    
    def drag_enter_event(self, event):
        """拖入事件处理"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def drop_event(self, event):
        """拖放事件处理"""
        files = self.file_processor.get_dropped_files(event)
        for file in files:
            if file not in self.files_to_process:
                self.files_to_process.append(file)
                self.file_list.addItem(file)
    
    def add_file(self):
        """添加文件"""
        files, _ = QFileDialog.getOpenFileNames(self, "选择文件", "", "所有文件 (*.*)")
        for file in files:
            if file not in self.files_to_process:
                self.files_to_process.append(file)
                self.file_list.addItem(file)
    
    def remove_file(self):
        """移除文件"""
        current_item = self.file_list.currentItem()
        if current_item:
            file_path = current_item.text()
            if file_path in self.files_to_process:
                self.files_to_process.remove(file_path)
            self.file_list.takeItem(self.file_list.row(current_item))
    
    def clear_files(self):
        """清空文件列表"""
        self.files_to_process.clear()
        self.file_list.clear()
    
    def update_key_inputs(self, value):
        """更新密钥输入框数量"""
        lang = self.language_dict[self.current_language]
        # 移除所有密钥输入框
        for i in reversed(range(self.key_inputs_layout.rowCount())):
            self.key_inputs_layout.removeRow(i)
        
        # 重新创建密钥输入框
        self.key_inputs = []
        for i in range(value):
            key_input = QLineEdit()
            key_input.setEchoMode(QLineEdit.Password)
            key_input.setPlaceholderText(lang["key_placeholder"].format(layer=i+1))
            self.key_inputs.append(key_input)
            self.key_inputs_layout.addRow(f"密钥 {i+1}:", key_input)
    
    def update_decrypt_key_inputs(self, value):
        """更新解密密钥输入框数量"""
        lang = self.language_dict[self.current_language]
        # 移除所有密钥输入框
        for i in reversed(range(self.decrypt_key_inputs_layout.rowCount())):
            self.decrypt_key_inputs_layout.removeRow(i)
        
        # 重新创建密钥输入框
        self.decrypt_key_inputs = []
        for i in range(value):
            key_input = QLineEdit()
            key_input.setEchoMode(QLineEdit.Password)
            key_input.setPlaceholderText(lang["key_placeholder"].format(layer=i+1))
            self.decrypt_key_inputs.append(key_input)
            self.decrypt_key_inputs_layout.addRow(f"密钥 {i+1}:", key_input)
    
    def start_encryption(self):
        """开始加密"""
        # 获取当前语言
        lang = self.language_dict[self.current_language]
        
        if not self.files_to_process:
            QMessageBox.warning(self, lang["warning"], lang["no_files_added"])
            return
        
        # 获取加密层数
        levels = self.encryption_levels.value()
        
        # 获取密钥
        keys = []
        valid_key_count = 0
        for i in range(levels):
            if i < len(self.key_inputs):  # 确保索引不越界
                key = self.key_inputs[i].text()
                if key:
                    keys.append(key)
                    valid_key_count += 1
        
        # 验证密钥数量
        if valid_key_count < levels:
            QMessageBox.warning(self, lang["warning"], f"请输入所有{levels}层密钥！")
            return
        
        # 开始加密
        for file_path in self.files_to_process:
            try:
                self.statusBar().showMessage(lang["encryption_in_progress"].format(file_path=file_path))
                
                # 获取原始文件扩展名
                original_extension = os.path.splitext(file_path)[1]
                
                # 读取文件
                data = self.file_processor.read_file(file_path)
                
                # 获取最大尝试次数
                max_attempts = self.max_attempts_spinbox.value() if self.self_destruct_checkbox.isChecked() else 3
                
                # 获取机器ID用于生成唯一指纹
                machine_id = self.machine_binder.machine_id
                
                # 计算加密后的文件路径
                encrypted_file_path = file_path + ".encrypted"
                
                # 执行多层加密，包含元数据和唯一指纹，使用加密后的文件路径
                encrypted_data = self.encryptor.nested_encrypt(data, keys, original_extension, max_attempts, machine_id, encrypted_file_path)
                
                # 如果启用机器绑定，将数据绑定到当前机器
                if self.machine_bind_checkbox.isChecked():
                    encrypted_data = self.machine_binder.bind_to_machine(encrypted_data)
                
                # 保存加密文件
                self.file_processor.write_file(encrypted_file_path, encrypted_data)
                
                # 添加到自毁列表
                if self.self_destruct_checkbox.isChecked():
                    self.self_destructor.add_file_to_destroy(encrypted_file_path)
                
            except Exception as e:
                QMessageBox.critical(self, "错误", f"加密文件 {file_path} 失败: {str(e)}")
                continue
        
        QMessageBox.information(self, "成功", "所有文件加密完成！")
        self.statusBar().showMessage(lang["encryption_completed"])
    
    def select_encrypted_file(self):
        """选择要解密的文件"""
        file_path, _ = QFileDialog.getOpenFileName(self, "选择要解密的文件", "", "加密文件 (*.encrypted)")
        if file_path:
            self.encrypted_file_path = file_path
    
    def start_decryption(self):
        """开始解密"""
        # 获取当前语言
        lang = self.language_dict[self.current_language]
        
        # 检查是否已选择文件
        if not hasattr(self, 'encrypted_file_path') or not self.encrypted_file_path:
            QMessageBox.warning(self, lang["warning"], lang["no_encrypted_file_selected"])
            return
        
        file_path = self.encrypted_file_path
        
        # 获取解密层数
        levels = self.decryption_levels.value()
        
        # 获取密钥
        keys = []
        valid_key_count = 0
        for i in range(levels):
            if i < len(self.decrypt_key_inputs):  # 确保索引不越界
                key = self.decrypt_key_inputs[i].text()
                if key:
                    keys.append(key)
                    valid_key_count += 1
        
        # 验证密钥数量
        if valid_key_count < levels:
            QMessageBox.warning(self, lang["warning"], f"请输入所有{levels}层密钥！")
            return
        
        try:
            self.statusBar().showMessage(lang["decryption_in_progress"].format(file_path=file_path))
            
            # 读取加密文件
            encrypted_data = self.file_processor.read_file(file_path)
            
            # 检查是否为自毁序列
            if self.self_destructor.is_destruct_sequence(keys[0]):
                # 触发自毁，更新文件元数据
                try:
                    if self.machine_bind_checkbox.isChecked() and b"|" in encrypted_data:
                        # 处理机器绑定的文件
                        parts = encrypted_data.split(b"|", 1)
                        machine_id = parts[0]
                        file_data = parts[1]
                        
                        # 解析元数据并设置自毁标记
                        metadata = self.encryptor.parse_metadata(file_data)
                        metadata["self_destruct"] = True
                        
                        # 更新文件数据
                        updated_file_data = self.encryptor.update_metadata(file_data, metadata)
                        updated_encrypted_data = machine_id + b"|" + updated_file_data
                    else:
                        # 处理普通加密文件
                        metadata = self.encryptor.parse_metadata(encrypted_data)
                        metadata["self_destruct"] = True
                        updated_encrypted_data = self.encryptor.update_metadata(encrypted_data, metadata)
                    
                    # 保存更新后的文件
                    self.file_processor.write_file(file_path, updated_encrypted_data)
                    QMessageBox.warning(self, "自毁激活", "自毁机制已激活，文件已销毁！")
                except Exception:
                    # 如果解析失败，直接销毁文件
                    self.self_destructor.destroy_files()
                    QMessageBox.warning(self, "自毁激活", "自毁机制已激活，文件已销毁！")
                return
            
            # 处理机器绑定
            machine_bound = False
            machine_id = b""
            file_data = encrypted_data
            
            if self.machine_bind_checkbox.isChecked() and b"|" in encrypted_data:
                parts = encrypted_data.split(b"|", 1)
                machine_id = parts[0]
                file_data = parts[1]
                machine_bound = True
                
                # 检查机器授权
                if not self.machine_binder.is_authorized_machine(machine_id.decode()):
                    # 更新失败尝试次数
                    metadata = self.encryptor.parse_metadata(file_data)
                    metadata["failed_attempts"] += 1
                    
                    # 检查是否触发自毁
                    if metadata["failed_attempts"] >= metadata["max_attempts"]:
                        metadata["self_destruct"] = True
                    
                    # 更新文件
                    updated_file_data = self.encryptor.update_metadata(file_data, metadata)
                    updated_encrypted_data = machine_id + b"|" + updated_file_data
                    self.file_processor.write_file(file_path, updated_encrypted_data)
                    
                    if metadata["self_destruct"]:
                        QMessageBox.warning(self, "自毁激活", "自毁机制已激活，文件已销毁！")
                    else:
                        QMessageBox.warning(self, "授权失败", f"当前机器未授权使用此文件！失败尝试: {metadata['failed_attempts']}/{metadata['max_attempts']}")
                    return
            
            # 解析元数据
            metadata = self.encryptor.parse_metadata(file_data)
            
            # 检查文件是否已销毁
            if metadata["self_destruct"]:
                QMessageBox.warning(self, "文件已销毁", "该文件已触发自毁机制，无法解密！")
                return
            
            # 获取机器ID用于指纹验证
            machine_id = self.machine_binder.machine_id
            
            # 先解析元数据，检查文件是否已自毁
            try:
                # 尝试使用正确密钥解析元数据，检查自毁状态
                metadata = self.encryptor.parse_metadata(file_data, keys)
                if metadata.get("self_destruct", False):
                    QMessageBox.warning(self, "文件已销毁", "该文件已触发自毁机制，无法解密！")
                    return
            except Exception:
                # 解析失败，继续执行解密，让nested_decrypt处理
                pass
            
            # 执行多层解密，包含指纹验证
            decrypted_data, updated_metadata, self_destruct_triggered = self.encryptor.nested_decrypt(file_data, keys, machine_id, file_path)
            
            # 检查是否触发自毁
            if self_destruct_triggered:
                # 更新文件元数据
                updated_file_data = self.encryptor.update_metadata(file_data, updated_metadata, keys)
                
                # 保存更新后的文件
                if machine_bound:
                    full_updated_data = machine_id + b"|" + updated_file_data
                else:
                    full_updated_data = updated_file_data
                
                self.file_processor.write_file(file_path, full_updated_data)
                QMessageBox.warning(self, "自毁激活", "自毁机制已激活，文件已销毁！")
                return
            
            # 检查解密是否成功
            if not decrypted_data:
                # 更新失败尝试次数
                # 传入正确的密钥列表，确保能正确解析原始元数据
                updated_file_data = self.encryptor.update_metadata(file_data, updated_metadata, keys)
                
                # 保存更新后的文件
                if machine_bound:
                    full_updated_data = machine_id + b"|" + updated_file_data
                else:
                    full_updated_data = updated_file_data
                
                self.file_processor.write_file(file_path, full_updated_data)
                QMessageBox.critical(self, "错误", f"解密失败: 密钥不正确！\n失败尝试: {updated_metadata['failed_attempts']}/{updated_metadata['max_attempts']}")
                return
            
            # 构建解密后的文件路径，恢复原始扩展名
            base_name = os.path.basename(file_path)
            base_name_without_ext = os.path.splitext(base_name)[0]
            
            # 使用元数据中的原始扩展名
            original_extension = updated_metadata["original_extension"]
            if not original_extension:
                # 如果没有原始扩展名，使用.decrypted
                original_extension = ".decrypted"
            
            # 构建完整路径
            decrypted_file_path = os.path.join(os.path.dirname(file_path), f"{base_name_without_ext}{original_extension}")
            
            # 保存解密文件
            self.file_processor.write_file(decrypted_file_path, decrypted_data)
            
            # 检查完整性警告
            if "integrity_warning" in updated_metadata and updated_metadata["integrity_warning"]:
                QMessageBox.warning(self, "完整性警告", f"文件解密完成，但检测到可能的数据完整性问题。\n文件可能被篡改或损坏！\n保存路径: {decrypted_file_path}")
            else:
                QMessageBox.information(self, "成功", f"文件解密完成！\n保存路径: {decrypted_file_path}")
            
            self.statusBar().showMessage(lang["decryption_completed"])
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"解密失败: {str(e)}")
            self.statusBar().showMessage("解密失败")
    
    def generate_decoys(self):
        """生成诱饵文档"""
        try:
            lang = self.language_dict[self.current_language]
            # 选择输出目录
            output_dir = QFileDialog.getExistingDirectory(self, lang["select_decoys_output_dir"])
            if not output_dir:
                return
                
            # 获取诱饵文档数量
            decoy_count = self.decoy_count_spinbox.value()
            
            # 生成诱饵文档
            for i in range(decoy_count):
                # 生成随机文件名
                decoy_name = f"decoy_{i+1}_{int(time.time())}"
                decoy_file_path = os.path.join(output_dir, f"{decoy_name}.encrypted")
                
                # 生成随机内容（1-10MB）
                random_size = 1024 * 1024 * (i % 10 + 1)  # 1-10MB随机大小
                random_content = os.urandom(random_size)
                
                # 生成随机密钥（2层）
                random_keys = [f"random_key_{j}_{os.urandom(8).hex()}" for j in range(2)]
                
                # 生成诱饵加密文件
                encrypted_data = self.encryptor.nested_encrypt(
                    random_content, random_keys, ".txt", 3, self.machine_binder.machine_id, decoy_file_path
                )
                
                # 保存诱饵文件
                self.file_processor.write_file(decoy_file_path, encrypted_data)
            
            QMessageBox.information(self, "成功", lang["decoys_generated"].format(decoy_count=decoy_count))
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"生成诱饵文档失败: {str(e)}")
    
    def browse_script(self):
        """浏览Python脚本"""
        file_path, _ = QFileDialog.getOpenFileName(self, "选择Python脚本", "", "Python文件 (*.py)")
        if file_path:
            self.script_path_edit.setText(file_path)
    
    def browse_output_dir(self):
        """浏览输出目录"""
        dir_path = QFileDialog.getExistingDirectory(self, "选择输出目录")
        if dir_path:
            self.output_dir_edit.setText(dir_path)
    
    def start_packaging(self):
        """开始打包"""
        QMessageBox.information(self, "功能提示", "EXE打包功能已包含在企业版本中。")
    
    def change_language(self, index):
        """切换语言"""
        # 更新当前语言
        self.current_language = "zh_CN" if index == 0 else "en_US"
        
        # 更新标题
        self.title_label.setText(self.language_dict[self.current_language]["app_title"])
        
        # 更新标签页名称
        self.tab_widget.setTabText(0, self.language_dict[self.current_language]["tab_encrypt"])
        self.tab_widget.setTabText(1, self.language_dict[self.current_language]["tab_decrypt"])
        self.tab_widget.setTabText(2, self.language_dict[self.current_language]["tab_security"])
        self.tab_widget.setTabText(3, self.language_dict[self.current_language]["tab_prank"])
        self.tab_widget.setTabText(4, self.language_dict[self.current_language]["tab_packaging"])
        
        # 重新创建所有标签页
        self.create_encrypt_tab()
        self.create_decrypt_tab()
        self.create_security_tab()
        self.create_prank_tab()
        self.create_packaging_tab()
        
        # 移除现有标签页并添加新创建的标签页
        # 移除所有标签页（注意：必须从后往前移除）
        for i in reversed(range(self.tab_widget.count())):
            self.tab_widget.removeTab(i)
        
        # 添加新创建的标签页
        self.tab_widget.addTab(self.encrypt_tab, self.language_dict[self.current_language]["tab_encrypt"])
        self.tab_widget.addTab(self.decrypt_tab, self.language_dict[self.current_language]["tab_decrypt"])
        self.tab_widget.addTab(self.security_tab, self.language_dict[self.current_language]["tab_security"])
        self.tab_widget.addTab(self.prank_tab, self.language_dict[self.current_language]["tab_prank"])
        self.tab_widget.addTab(self.packaging_tab, self.language_dict[self.current_language]["tab_packaging"])
    
    def closeEvent(self, event):
        """关闭窗口事件处理"""
        lang = self.language_dict[self.current_language]
        reply = QMessageBox.question(self, lang["confirm_exit"], lang["confirm_exit_message"], 
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
