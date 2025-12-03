#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自毁机制模块
"""

import os
import shutil
import hashlib
from typing import List


class SelfDestructor:
    """自毁机制类"""
    
    def __init__(self, max_attempts: int = 3):
        self.max_attempts = max_attempts
        self.failed_attempts = 0
        self.files_to_destroy: List[str] = []
    
    def add_file_to_destroy(self, file_path: str) -> None:
        """
        添加要销毁的文件
        
        Args:
            file_path: 文件路径
        """
        if os.path.exists(file_path) and file_path not in self.files_to_destroy:
            self.files_to_destroy.append(file_path)
    
    def remove_file_to_destroy(self, file_path: str) -> None:
        """
        移除要销毁的文件
        
        Args:
            file_path: 文件路径
        """
        if file_path in self.files_to_destroy:
            self.files_to_destroy.remove(file_path)
    
    def record_failed_attempt(self) -> bool:
        """
        记录失败尝试
        
        Returns:
            是否激活自毁机制
        """
        self.failed_attempts += 1
        return self.failed_attempts >= self.max_attempts
    
    def reset_attempts(self) -> None:
        """
        重置失败尝试计数
        """
        self.failed_attempts = 0
    
    def destroy_files(self) -> list[tuple[bool, str]]:
        """
        销毁所有标记的文件
        
        Returns:
            销毁结果列表，每个元素为(是否成功, 消息)
        """
        results = []
        for file_path in self.files_to_destroy:
            result = self._destroy_single_file(file_path)
            results.append(result)
        # 清空列表
        self.files_to_destroy.clear()
        return results
    
    def _destroy_single_file(self, file_path: str) -> tuple[bool, str]:
        """
        销毁单个文件（安全删除，多次覆盖）
        
        Args:
            file_path: 文件路径
            
        Returns:
            (是否成功销毁, 错误信息或成功消息)
        """
        try:
            if not os.path.exists(file_path):
                return False, f"文件不存在: {file_path}"
            
            # 处理目录情况
            if os.path.isdir(file_path):
                # 递归销毁目录中的所有文件
                for root, dirs, files in os.walk(file_path, topdown=False):
                    for file_name in files:
                        self._destroy_single_file(os.path.join(root, file_name))
                    for dir_name in dirs:
                        dir_path = os.path.join(root, dir_name)
                        try:
                            os.rmdir(dir_path)
                        except Exception as e:
                            return False, f"删除目录失败: {dir_path}, 错误: {str(e)}"
                try:
                    os.rmdir(file_path)
                    return True, f"目录销毁成功: {file_path}"
                except Exception as e:
                    return False, f"删除目录失败: {file_path}, 错误: {str(e)}"
            
            # 第一步：多次覆盖文件内容（符合DoD 5220.22-M标准）
            file_size = os.path.getsize(file_path)
            
            # 覆盖模式：0xFF, 0x00, 随机数据, 随机数据
            overwrite_patterns = [
                b'\xFF' * min(1024*1024, file_size),  # 1MB块，全1
                b'\x00' * min(1024*1024, file_size),  # 1MB块，全0
                os.urandom(min(1024*1024, file_size)),  # 1MB块，随机数据
                os.urandom(min(1024*1024, file_size))   # 1MB块，随机数据
            ]
            
            for pattern in overwrite_patterns:
                with open(file_path, "wb") as f:
                    remaining = file_size
                    while remaining > 0:
                        write_size = min(len(pattern), remaining)
                        f.write(pattern[:write_size])
                        remaining -= write_size
                    f.flush()
                    os.fsync(f.fileno())
            
            # 第二步：重命名文件多次，增加恢复难度
            original_path = file_path
            for i in range(5):
                new_path = f"{original_path}.{i}.tmp"
                os.rename(file_path, new_path)
                file_path = new_path
            
            # 第三步：删除最终文件
            os.remove(file_path)
            
            return True, f"文件销毁成功: {original_path}"
        except PermissionError:
            return False, f"权限不足，无法销毁文件: {file_path}"
        except FileNotFoundError:
            return False, f"文件在销毁过程中不存在: {file_path}"
        except Exception as e:
            return False, f"销毁文件失败: {file_path}, 错误: {str(e)}"
    
    def destroy_encrypted_data(self, encrypted_data: bytes) -> bytes:
        """
        销毁加密数据
        
        Args:
            encrypted_data: 加密数据
            
        Returns:
            销毁后的数据（空字节）
        """
        return b""  # 返回空字节，表示数据已销毁
    
    def is_destruct_sequence(self, password: str) -> bool:
        """
        检查是否为自毁序列
        
        Args:
            password: 输入的密码
            
        Returns:
            是否为自毁序列
        """
        # 更安全的实现：使用特定格式的密码触发自毁
        # 格式：destruct_<随机字符串>_<校验和>
        # 这种方式避免了硬编码的固定序列，提高了安全性
        if password.startswith("destruct_"):
            # 计算密码的SHA256哈希，只有特定哈希值的密码才能触发自毁
            # 示例：destruct_12345678_abc123
            import hashlib
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            # 只有特定哈希值的密码才能触发自毁
            # 这里使用一个示例哈希，实际应用中应使用更复杂的机制
            return password_hash.startswith("a1b2c3")
        return False
