#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXE打包模块
"""

import os
import subprocess
import tempfile
from typing import Dict, List, Optional


class EXEPackager:
    """EXE打包器类"""
    
    def __init__(self):
        self.pyinstaller_path = self._find_pyinstaller()
    
    def _find_pyinstaller(self) -> str:
        """
        查找PyInstaller可执行文件路径
        
        Returns:
            PyInstaller可执行文件路径
        """
        # 尝试直接调用pyinstaller
        try:
            subprocess.check_output(["pyinstaller", "--version"], stderr=subprocess.STDOUT)
            return "pyinstaller"
        except subprocess.CalledProcessError:
            # 尝试使用python -m PyInstaller
            try:
                subprocess.check_output(["python", "-m", "PyInstaller", "--version"], stderr=subprocess.STDOUT)
                return "python -m PyInstaller"
            except subprocess.CalledProcessError:
                # 尝试使用python3 -m PyInstaller
                try:
                    subprocess.check_output(["python3", "-m", "PyInstaller", "--version"], stderr=subprocess.STDOUT)
                    return "python3 -m PyInstaller"
                except subprocess.CalledProcessError:
                    raise RuntimeError("未找到PyInstaller，请先安装: pip install pyinstaller")
    
    def package(self, script_path: str, output_dir: str, options: Dict = None) -> bool:
        """
        打包Python脚本为EXE文件
        
        Args:
            script_path: Python脚本路径
            output_dir: 输出目录
            options: 打包选项
            
        Returns:
            打包是否成功
        """
        if not os.path.exists(script_path):
            raise FileNotFoundError(f"脚本文件不存在: {script_path}")
        
        # 默认选项
        default_options = {
            "onefile": False,
            "windowed": False,
            "icon": None,
            "name": None,
            "include_modules": [],
            "exclude_modules": [],
            "add_data": [],
            "hidden_imports": []
        }
        
        if options:
            default_options.update(options)
        
        options = default_options
        
        # 构建PyInstaller命令
        cmd = self._build_pyinstaller_cmd(script_path, output_dir, options)
        
        # 执行打包命令
        try:
            subprocess.run(cmd, check=True, shell=True, cwd=output_dir)
            return True
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"打包失败: {str(e)}")
    
    def _build_pyinstaller_cmd(self, script_path: str, output_dir: str, options: Dict) -> str:
        """
        构建PyInstaller命令
        
        Args:
            script_path: Python脚本路径
            output_dir: 输出目录
            options: 打包选项
            
        Returns:
            PyInstaller命令字符串
        """
        # 基础命令
        cmd = f"{self.pyinstaller_path} {script_path} --distpath {output_dir} --workpath {os.path.join(output_dir, 'build')} --specpath {os.path.join(output_dir, 'spec')}"
        
        # 单文件模式
        if options["onefile"]:
            cmd += " --onefile"
        
        # 窗口模式
        if options["windowed"]:
            cmd += " --windowed"
        
        # 应用名称
        if options["name"]:
            cmd += f" --name {options['name']}"
        
        # 图标
        if options["icon"]:
            cmd += f" --icon {options['icon']}"
        
        # 包含模块
        for module in options["include_modules"]:
            cmd += f" --hidden-import {module}"
        
        # 排除模块
        for module in options["exclude_modules"]:
            cmd += f" --exclude-module {module}"
        
        # 附加数据
        for data in options["add_data"]:
            cmd += f" --add-data {data}"
        
        # 隐藏导入
        for hidden_import in options["hidden_imports"]:
            cmd += f" --hidden-import {hidden_import}"
        
        return cmd
    
    def create_spec_file(self, script_path: str, output_dir: str, options: Dict = None) -> str:
        """
        创建PyInstaller spec文件
        
        Args:
            script_path: Python脚本路径
            output_dir: 输出目录
            options: 打包选项
            
        Returns:
            spec文件路径
        """
        if not os.path.exists(script_path):
            raise FileNotFoundError(f"脚本文件不存在: {script_path}")
        
        # 默认选项
        default_options = {
            "name": os.path.splitext(os.path.basename(script_path))[0],
            "onefile": False,
            "windowed": False,
            "icon": None
        }
        
        if options:
            default_options.update(options)
        
        options = default_options
        
        # 构建spec文件内容
        spec_content = self._generate_spec_content(script_path, options)
        
        # 保存spec文件
        spec_filename = f"{options['name']}.spec"
        spec_path = os.path.join(output_dir, spec_filename)
        
        with open(spec_path, "w", encoding="utf-8") as f:
            f.write(spec_content)
        
        return spec_path
    
    def _generate_spec_content(self, script_path: str, options: Dict) -> str:
        """
        生成spec文件内容
        
        Args:
            script_path: Python脚本路径
            options: 打包选项
            
        Returns:
            spec文件内容字符串
        """
        # 基础spec内容
        spec_content = f"""# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['{script_path}'],
             pathex=[],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={{}},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

"""
        
        # 根据选项添加不同的EXE配置
        if options["onefile"]:
            spec_content += f"""
ex = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='{options['name']}',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console={'False' if options['windowed'] else 'True'},
          disable_windowed_traceback=False,
          argv_emulation=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None,
          icon='{options['icon']}' if options['icon'] else 'None')
"""
        else:
            spec_content += f"""
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='{options['name']}')
"""
        
        return spec_content
    
    def get_supported_options(self) -> List[str]:
        """
        获取支持的打包选项
        
        Returns:
            支持的选项列表
        """
        return [
            "onefile",
            "windowed",
            "icon",
            "name",
            "include_modules",
            "exclude_modules",
            "add_data",
            "hidden_imports"
        ]
    
    def validate_script(self, script_path: str) -> bool:
        """
        验证Python脚本是否可以正常运行
        
        Args:
            script_path: Python脚本路径
            
        Returns:
            脚本是否有效
        """
        if not os.path.exists(script_path):
            return False
        
        # 尝试使用Python解释器运行脚本，检查语法错误
        try:
            subprocess.run(["python", "-m", "py_compile", script_path], check=True)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def get_version(self) -> str:
        """
        获取PyInstaller版本
        
        Returns:
            PyInstaller版本字符串
        """
        try:
            output = subprocess.check_output(f"{self.pyinstaller_path} --version", shell=True, text=True)
            return output.strip()
        except subprocess.CalledProcessError:
            return "未知版本"
