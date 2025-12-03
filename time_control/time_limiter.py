#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
时间限制访问控制模块
"""

import time
from datetime import datetime, timedelta
from typing import Union


class TimeLimiter:
    """时间限制器类"""
    
    def __init__(self):
        self.current_time = time.time()
    
    def is_expired(self, expiry_time: Union[float, str, datetime]) -> bool:
        """
        检查是否过期
        
        Args:
            expiry_time: 过期时间，可以是时间戳、字符串或datetime对象
            
        Returns:
            是否过期
        """
        # 转换过期时间为时间戳
        expiry_timestamp = self._convert_to_timestamp(expiry_time)
        
        # 检查当前时间是否超过过期时间
        return time.time() > expiry_timestamp
    
    def _convert_to_timestamp(self, time_value: Union[float, str, datetime]) -> float:
        """
        将各种时间格式转换为时间戳
        
        Args:
            time_value: 时间值
            
        Returns:
            时间戳
        """
        if isinstance(time_value, float) or isinstance(time_value, int):
            # 已经是时间戳
            return float(time_value)
        elif isinstance(time_value, datetime):
            # datetime对象转换为时间戳
            return time.mktime(time_value.timetuple())
        elif isinstance(time_value, str):
            # 字符串转换为时间戳
            try:
                # 尝试多种时间格式
                formats = [
                    "%Y-%m-%d %H:%M:%S",
                    "%Y-%m-%d",
                    "%Y/%m/%d %H:%M:%S",
                    "%Y/%m/%d",
                    "%d-%m-%Y %H:%M:%S",
                    "%d-%m-%Y"
                ]
                
                for fmt in formats:
                    try:
                        dt = datetime.strptime(time_value, fmt)
                        return time.mktime(dt.timetuple())
                    except ValueError:
                        continue
                
                # 如果所有格式都失败，抛出异常
                raise ValueError(f"无法解析时间字符串: {time_value}")
            except Exception as e:
                raise ValueError(f"时间字符串转换失败: {str(e)}")
        else:
            raise TypeError(f"不支持的时间类型: {type(time_value)}")
    
    def add_time_limit(self, data: bytes, expiry_time: Union[float, str, datetime]) -> bytes:
        """
        为数据添加时间限制
        
        Args:
            data: 原始数据
            expiry_time: 过期时间
            
        Returns:
            添加时间限制后的数据
        """
        # 转换过期时间为时间戳
        expiry_timestamp = self._convert_to_timestamp(expiry_time)
        
        # 格式：过期时间戳 + 分隔符 + 原始数据
        time_limit_header = f"EXPIRY:{expiry_timestamp}:END".encode()
        return time_limit_header + data
    
    def remove_time_limit(self, data: bytes) -> tuple[bytes, float]:
        """
        移除数据的时间限制
        
        Args:
            data: 带有时间限制的数据
            
        Returns:
            (原始数据, 过期时间戳)
        """
        # 查找时间限制头
        header_start = b"EXPIRY:"
        header_end = b":END"
        
        if not data.startswith(header_start):
            raise ValueError("数据不包含时间限制头")
        
        # 提取过期时间戳
        header_end_pos = data.find(header_end)
        if header_end_pos == -1:
            raise ValueError("无效的时间限制头")
        
        # 解析过期时间戳
        expiry_str = data[len(header_start):header_end_pos].decode()
        expiry_timestamp = float(expiry_str)
        
        # 提取原始数据
        original_data = data[header_end_pos + len(header_end):]
        
        return original_data, expiry_timestamp
    
    def get_remaining_time(self, expiry_time: Union[float, str, datetime]) -> tuple[bool, float]:
        """
        获取剩余时间
        
        Args:
            expiry_time: 过期时间
            
        Returns:
            (是否过期, 剩余时间（秒）)
        """
        # 转换过期时间为时间戳
        expiry_timestamp = self._convert_to_timestamp(expiry_time)
        
        # 计算剩余时间
        current_timestamp = time.time()
        remaining = expiry_timestamp - current_timestamp
        
        if remaining <= 0:
            return True, 0
        else:
            return False, remaining
    
    def format_remaining_time(self, remaining_seconds: float) -> str:
        """
        格式化剩余时间为可读字符串
        
        Args:
            remaining_seconds: 剩余时间（秒）
            
        Returns:
            格式化后的剩余时间字符串
        """
        if remaining_seconds <= 0:
            return "已过期"
        
        # 转换为timedelta对象
        remaining = timedelta(seconds=remaining_seconds)
        
        # 格式化输出
        days = remaining.days
        hours, remainder = divmod(remaining.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        if days > 0:
            return f"{days}天 {hours}小时 {minutes}分钟 {seconds}秒"
        elif hours > 0:
            return f"{hours}小时 {minutes}分钟 {seconds}秒"
        elif minutes > 0:
            return f"{minutes}分钟 {seconds}秒"
        else:
            return f"{seconds}秒"
    
    def generate_expiry_time(self, days: int = 0, hours: int = 0, minutes: int = 0) -> float:
        """
        生成过期时间
        
        Args:
            days: 天数
            hours: 小时数
            minutes: 分钟数
            
        Returns:
            过期时间戳
        """
        # 计算总秒数
        total_seconds = days * 86400 + hours * 3600 + minutes * 60
        
        # 生成过期时间
        return time.time() + total_seconds
    
    def validate_time_limit(self, data: bytes) -> tuple[bool, str]:
        """
        验证时间限制
        
        Args:
            data: 带有时间限制的数据
            
        Returns:
            (是否有效, 错误信息或剩余时间)
        """
        try:
            # 移除时间限制，获取原始数据和过期时间
            original_data, expiry_timestamp = self.remove_time_limit(data)
            
            # 检查是否过期
            is_expired = self.is_expired(expiry_timestamp)
            if is_expired:
                return False, "文件已过期"
            
            # 获取剩余时间
            _, remaining = self.get_remaining_time(expiry_timestamp)
            remaining_str = self.format_remaining_time(remaining)
            
            return True, f"文件有效期剩余: {remaining_str}"
        except Exception as e:
            return False, f"时间限制验证失败: {str(e)}"
