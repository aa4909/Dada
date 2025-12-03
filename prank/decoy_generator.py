#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
诱饵文档生成模块
"""

import os
import random
import string
from typing import List


class DecoyGenerator:
    """诱饵文档生成器类"""
    
    def __init__(self):
        # 诱饵文档内容模板
        self.decoy_templates = [
            "这是一个重要的文档，包含了机密信息。请妥善保管。\n\n密码: password123\n账号: admin\n\n请勿泄露此文档！",
            "项目计划\n\n阶段1: 启动\n阶段2: 开发\n阶段3: 测试\n阶段4: 部署\n\n重要提示: 所有工作必须在截止日期前完成。",
            "财务报告\n\n收入: $1,000,000\n支出: $500,000\n利润: $500,000\n\n本报告仅供内部使用。",
            "个人日记\n\n今天是个重要的日子，我终于完成了我的目标。\n\n秘密: 我藏了一些东西在地下室。",
            "会议记录\n\n参会人员: 张三, 李四, 王五\n会议主题: 项目进度\n会议结论: 项目进展顺利，预计下个月完成。",
            "研究报告\n\n研究主题: 人工智能\n研究结果: 我们取得了重大突破。\n\n关键词: AI, 机器学习, 深度学习",
            "密码列表\n\n邮箱: user@example.com / password1\n银行: 12345678 / 87654321\n社交媒体: username / socialpass",
            "工作计划\n\n周一: 完成任务1\n周二: 完成任务2\n周三: 完成任务3\n周四: 完成任务4\n周五: 完成任务5\n\n请严格按照计划执行。",
            "合同文本\n\n甲方: 公司A\n乙方: 公司B\n\n合同内容: 双方同意合作开发新项目。\n\n签字: _________ 日期: _________",
            "技术文档\n\n系统架构: 三层架构\n技术栈: Python, Java, MySQL\n\n重要配置: 端口号 8080, 数据库密码 dbpass123"
        ]
        
        # 支持的诱饵文档扩展名
        self.supported_extensions = [".txt", ".docx", ".pdf", ".xlsx"]
    
    def generate_decoy_name(self) -> str:
        """
        生成诱饵文档名称
        
        Returns:
            诱饵文档名称字符串
        """
        # 文档名称前缀
        prefixes = ["机密", "重要", "秘密", "项目", "计划", "报告", "记录", "数据", "文档", "文件"]
        # 文档名称后缀
        suffixes = ["文件", "文档", "报告", "记录", "计划", "数据", "资料", "信息", "备份", "副本"]
        
        # 生成随机数字
        random_num = random.randint(1000, 9999)
        
        # 随机选择前缀和后缀
        prefix = random.choice(prefixes)
        suffix = random.choice(suffixes)
        
        # 组合生成文件名
        return f"{prefix}_{suffix}_{random_num}"
    
    def generate_decoy_content(self) -> str:
        """
        生成诱饵文档内容
        
        Returns:
            诱饵文档内容字符串
        """
        return random.choice(self.decoy_templates)
    
    def generate_decoy_file(self, output_dir: str) -> str:
        """
        生成单个诱饵文件
        
        Args:
            output_dir: 输出目录
            
        Returns:
            生成的诱饵文件路径
        """
        # 确保输出目录存在
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 生成文件名和内容
        decoy_name = self.generate_decoy_name()
        decoy_content = self.generate_decoy_content()
        
        # 随机选择文件扩展名（目前只支持txt，其他格式需要额外库支持）
        extension = ".txt"
        
        # 生成文件路径
        file_path = os.path.join(output_dir, f"{decoy_name}{extension}")
        
        # 写入文件内容
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(decoy_content)
        
        return file_path
    
    def generate_multiple_decoys(self, count: int, output_dir: str) -> List[str]:
        """
        生成多个诱饵文件
        
        Args:
            count: 要生成的诱饵文件数量
            output_dir: 输出目录
            
        Returns:
            生成的诱饵文件路径列表
        """
        generated_files = []
        for _ in range(count):
            file_path = self.generate_decoy_file(output_dir)
            generated_files.append(file_path)
        return generated_files
    
    def generate_encrypted_decoy(self, output_dir: str, fake_password: str) -> str:
        """
        生成加密的诱饵文件（使用真实AES-GCM加密）
        
        Args:
            output_dir: 输出目录
            fake_password: 虚假密码
            
        Returns:
            生成的加密诱饵文件路径
        """
        # 生成诱饵内容
        decoy_content = f"{self.generate_decoy_content()}\n\n虚假密码: {fake_password}"
        
        # 生成文件名
        decoy_name = f"加密_{self.generate_decoy_name()}"
        file_path = os.path.join(output_dir, f"{decoy_name}.txt.encrypted")
        
        # 使用真实的AES-GCM加密算法
        from Crypto.Cipher import AES
        from Crypto.Protocol.KDF import PBKDF2
        from Crypto.Hash import SHA256
        from Crypto.Random import get_random_bytes
        
        # 从密码生成密钥
        salt = get_random_bytes(16)
        key = PBKDF2(
            password=fake_password.encode('utf-8'),
            salt=salt,
            dkLen=32,
            count=100000,
            hmac_hash_module=SHA256
        )
        
        # 使用AES-GCM加密
        iv = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_GCM, iv)
        encrypted_data, tag = cipher.encrypt_and_digest(decoy_content.encode('utf-8'))
        
        # 写入加密后的数据（格式：salt + iv + 密文 + 标签）
        with open(file_path, "wb") as f:
            f.write(salt)
            f.write(iv)
            f.write(encrypted_data)
            f.write(tag)
        
        return file_path
    
    def add_fake_metadata(self, file_path: str) -> None:
        """
        为文件添加虚假元数据
        
        Args:
            file_path: 文件路径
        """
        # 简单实现：在文件名中添加虚假元数据
        # 实际应用中可以使用第三方库修改文件元数据
        dir_name = os.path.dirname(file_path)
        base_name = os.path.basename(file_path)
        
        # 添加虚假元数据前缀
        fake_metadata = f"[机密]{base_name}"
        new_file_path = os.path.join(dir_name, fake_metadata)
        
        # 重命名文件
        os.rename(file_path, new_file_path)
