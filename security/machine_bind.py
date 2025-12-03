#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
机器绑定模块
"""

import platform
import hashlib
import subprocess
import sys


class MachineBinder:
    """机器绑定类"""
    
    def __init__(self):
        self.machine_id = self.get_machine_id()
    
    def get_machine_id(self) -> str:
        """
        获取机器唯一标识（结合多种硬件信息，更难伪造）
        
        Returns:
            机器唯一标识字符串
        """
        try:
            # 收集多种硬件和系统信息
            hardware_info = []
            
            # 平台基础信息
            hardware_info.append(platform.system())
            hardware_info.append(platform.architecture()[0])
            hardware_info.append(platform.machine())
            hardware_info.append(platform.version())
            
            # CPU信息
            try:
                if platform.system() == "Windows":
                    result = subprocess.check_output(["wmic", "cpu", "get", "name,processorid,numberofcores"], 
                                                   universal_newlines=True, stderr=subprocess.STDOUT)
                    hardware_info.append(result.strip())
                elif platform.system() == "Linux":
                    with open("/proc/cpuinfo", "r") as f:
                        cpuinfo = f.read()
                    hardware_info.append(cpuinfo)
                elif platform.system() == "Darwin":
                    result = subprocess.check_output(["sysctl", "-n", "machdep.cpu.brand_string", "machdep.cpu.core_count"], 
                                                   universal_newlines=True, stderr=subprocess.STDOUT)
                    hardware_info.append(result.strip())
            except Exception:
                hardware_info.append("cpu_info_unavailable")
            
            # 内存信息
            try:
                import psutil
                memory = psutil.virtual_memory()
                hardware_info.append(f"total_memory:{memory.total}")
                hardware_info.append(f"available_memory:{memory.available}")
            except Exception:
                hardware_info.append("memory_info_unavailable")
            
            # 磁盘信息
            try:
                if platform.system() == "Windows":
                    result = subprocess.check_output(["wmic", "diskdrive", "get", "model,size,serialnumber"], 
                                                   universal_newlines=True, stderr=subprocess.STDOUT)
                    hardware_info.append(result.strip())
                elif platform.system() == "Linux":
                    with open("/proc/partitions", "r") as f:
                        partitions = f.read()
                    hardware_info.append(partitions)
                elif platform.system() == "Darwin":
                    result = subprocess.check_output(["diskutil", "info", "/"], 
                                                   universal_newlines=True, stderr=subprocess.STDOUT)
                    hardware_info.append(result.strip())
            except Exception:
                hardware_info.append("disk_info_unavailable")
            
            # 网络信息
            try:
                if platform.system() == "Windows":
                    result = subprocess.check_output(["wmic", "nic", "get", "macaddress"], 
                                                   universal_newlines=True, stderr=subprocess.STDOUT)
                    hardware_info.append(result.strip())
                else:
                    # 读取网络接口信息
                    import psutil
                    net_if_addrs = psutil.net_if_addrs()
                    net_info = []
                    for interface, addrs in net_if_addrs.items():
                        for addr in addrs:
                            if addr.family == psutil.AF_LINK:  # MAC地址
                                net_info.append(f"{interface}:{addr.address}")
                    hardware_info.append(",".join(net_info))
            except Exception:
                hardware_info.append("network_info_unavailable")
            
            # 系统安装时间
            try:
                if platform.system() == "Windows":
                    result = subprocess.check_output(["wmic", "os", "get", "installdate"], 
                                                   universal_newlines=True, stderr=subprocess.STDOUT)
                    hardware_info.append(result.strip())
                elif platform.system() == "Linux":
                    with open("/proc/stat", "r") as f:
                        boot_time = f.readline()
                    hardware_info.append(boot_time.strip())
                elif platform.system() == "Darwin":
                    result = subprocess.check_output(["sysctl", "-n", "kern.boottime"], 
                                                   universal_newlines=True, stderr=subprocess.STDOUT)
                    hardware_info.append(result.strip())
            except Exception:
                hardware_info.append("install_time_unavailable")
            
            # 组合所有信息，生成唯一ID
            combined_info = "|" .join(hardware_info)
            machine_id = hashlib.sha256(combined_info.encode()).hexdigest()
            
            return machine_id
        except Exception:
            # 异常情况下使用更复杂的通用方法
            import uuid
            # 使用UUID和平台信息的组合
            fallback_id = f"{platform.system()}-{platform.architecture()[0]}-{platform.machine()}-{uuid.getnode()}"
            return hashlib.sha256(fallback_id.encode()).hexdigest()
    
    def is_authorized_machine(self, encrypted_machine_id: str) -> bool:
        """
        检查当前机器是否为授权机器
        
        Args:
            encrypted_machine_id: 加密的机器ID
            
        Returns:
            是否为授权机器
        """
        return self.machine_id == encrypted_machine_id
    
    def bind_to_machine(self, data: bytes) -> bytes:
        """
        将数据绑定到当前机器（加密绑定）
        
        Args:
            data: 要绑定的数据
            
        Returns:
            绑定后的数据
        """
        # 生成绑定密钥（基于机器ID和随机盐值）
        salt = os.urandom(16)
        
        # 使用PBKDF2生成密钥
        from Crypto.Protocol.KDF import PBKDF2
        from Crypto.Hash import SHA256
        key = PBKDF2(
            password=self.machine_id.encode(),
            salt=salt,
            dkLen=32,
            count=100000,
            hmac_hash_module=SHA256
        )
        
        # 使用AES-GCM加密数据
        from Crypto.Cipher import AES
        from Crypto.Random import get_random_bytes
        iv = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_GCM, iv)
        encrypted_data, tag = cipher.encrypt_and_digest(data)
        
        # 返回格式：盐值(16字节) + IV(16字节) + 密文 + 认证标签(16字节)
        return salt + iv + encrypted_data + tag
    
    def unbind_from_machine(self, bound_data: bytes) -> bytes:
        """
        从数据中提取原始数据（验证并解密机器绑定）
        
        Args:
            bound_data: 绑定了机器ID的数据
            
        Returns:
            原始数据（如果机器ID匹配且解密成功）
        """
        # 检查数据长度
        if len(bound_data) < 48:  # 盐值(16) + IV(16) + 至少1字节密文 + 标签(16)
            raise ValueError("绑定数据长度不足，无法提取必要信息")
        
        # 提取盐值、IV、密文和认证标签
        salt = bound_data[:16]
        iv = bound_data[16:32]
        tag = bound_data[-16:]
        encrypted_data = bound_data[32:-16]
        
        # 生成绑定密钥（基于机器ID和盐值）
        from Crypto.Protocol.KDF import PBKDF2
        from Crypto.Hash import SHA256
        key = PBKDF2(
            password=self.machine_id.encode(),
            salt=salt,
            dkLen=32,
            count=100000,
            hmac_hash_module=SHA256
        )
        
        # 使用AES-GCM解密数据
        from Crypto.Cipher import AES
        cipher = AES.new(key, AES.MODE_GCM, iv)
        
        try:
            # 解密数据并验证认证标签
            original_data = cipher.decrypt_and_verify(encrypted_data, tag)
            return original_data
        except ValueError:
            raise ValueError("机器ID不匹配或数据已被篡改，无法解绑")
