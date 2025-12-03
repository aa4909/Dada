#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件处理模块
"""

import os
import shutil
from typing import List


class FileProcessor:
    """文件处理器类"""
    
    def __init__(self):
        self.supported_extensions = [".txt", ".docx", ".pdf", ".jpg", ".png", ".xlsx", ".pptx", ".zip", ".rar"]
    
    def read_file(self, file_path: str) -> bytes:
        """
        读取文件内容
        
        Args:
            file_path: 文件路径
            
        Returns:
            文件内容字节
        """
        try:
            with open(file_path, "rb") as f:
                return f.read()
        except Exception as e:
            raise IOError(f"读取文件失败: {str(e)}")
    
    def write_file(self, file_path: str, data: bytes) -> None:
        """
        写入文件内容
        
        Args:
            file_path: 文件路径
            data: 要写入的数据
        """
        try:
            with open(file_path, "wb") as f:
                f.write(data)
        except Exception as e:
            raise IOError(f"写入文件失败: {str(e)}")
    
    def get_file_info(self, file_path: str) -> dict:
        """
        获取文件信息
        
        Args:
            file_path: 文件路径
            
        Returns:
            文件信息字典
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        return {
            "name": os.path.basename(file_path),
            "path": file_path,
            "size": os.path.getsize(file_path),
            "extension": os.path.splitext(file_path)[1].lower(),
            "created_time": os.path.getctime(file_path),
            "modified_time": os.path.getmtime(file_path)
        }
    
    def is_supported_file(self, file_path: str) -> bool:
        """
        检查文件是否受支持
        
        Args:
            file_path: 文件路径
            
        Returns:
            是否受支持
        """
        ext = os.path.splitext(file_path)[1].lower()
        return ext in self.supported_extensions
    
    def get_dropped_files(self, event) -> List[str]:
        """
        处理拖放事件，获取文件路径列表
        
        Args:
            event: 拖放事件对象
            
        Returns:
            文件路径列表
        """
        files = []
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if os.path.isfile(file_path):
                files.append(file_path)
        return files
    
    def create_backup(self, file_path: str) -> str:
        """
        创建文件备份
        
        Args:
            file_path: 文件路径
            
        Returns:
            备份文件路径
        """
        backup_path = f"{file_path}.bak"
        try:
            shutil.copy2(file_path, backup_path)
            return backup_path
        except Exception as e:
            raise IOError(f"创建备份失败: {str(e)}")
    
    def delete_file(self, file_path: str) -> None:
        """
        删除文件
        
        Args:
            file_path: 文件路径
        """
        try:
            os.remove(file_path)
        except Exception as e:
            raise IOError(f"删除文件失败: {str(e)}")
    
    def get_file_hash(self, file_path: str, algorithm: str = "sha256") -> str:
        """
        获取文件哈希值
        
        Args:
            file_path: 文件路径
            algorithm: 哈希算法
            
        Returns:
            哈希值字符串
        """
        import hashlib
        
        hash_obj = hashlib.new(algorithm)
        
        try:
            with open(file_path, "rb") as f:
                # 分块读取大文件
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_obj.update(chunk)
            return hash_obj.hexdigest()
        except Exception as e:
            raise IOError(f"计算文件哈希失败: {str(e)}")
