#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Windows环境测试脚本
用于验证Windows平台是否正确配置并可以运行DCA实验

使用方法:
    python test_windows_setup.py
"""
import sys
import platform

# 颜色输出 (Windows兼容)
try:
    import colorama
    colorama.init()
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'
except:
    GREEN = YELLOW = RED = BLUE = BOLD = END = ''

def print_header(text):
    print(f"\n{BLUE}{'='*70}{END}")
    print(f"{BOLD}{text}{END}")
    print(f"{BLUE}{'='*70}{END}\n")

def print_success(text):
    print(f"{GREEN}✓ {text}{END}")

def print_warning(text):
    print(f"{YELLOW}⚠ {text}{END}")

def print_error(text):
    print(f"{RED}✗ {text}{END}")

def test_python_version():
    """测试Python版本"""
    print_header("1. 检查 Python 版本")
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    print(f"Python版本: {version_str}")

    if version.major >= 3 and version.minor >= 7:
        print_success(f"Python版本符合要求 (>= 3.7)")
        return True
    else:
        print_error(f"Python版本过低，需要 >= 3.7")
        print_warning(f"请升级Python: https://www.python.org/downloads/")
        return False

def test_platform():
    """测试操作系统"""
    print_header("2. 检查操作系统")
    os_name = platform.system()
    os_version = platform.version()
    print(f"操作系统: {os_name} {os_version}")

    if os_name == "Windows":
        print_success("Windows平台 - 将使用Windows兼容模式")
        return True
    else:
        print_warning(f"非Windows平台 ({os_name}) - 将使用标准模式")
        return True

def test_dependencies():
    """测试依赖包"""
    print_header("3. 检查依赖包")

    packages = {
        'numpy': '数值计算',
        'torch': 'PyTorch深度学习',
        'gym': 'OpenAI Gym环境',
        'scipy': '科学计算',
    }

    all_ok = True
    for package, desc in packages.items():
        try:
            mod = __import__(package)
            version = getattr(mod, '__version__', 'unknown')
            print_success(f"{package:10s} {version:10s} - {desc}")
        except ImportError:
            print_error(f"{package:10s} 未安装 - {desc}")
            all_ok = False

    if not all_ok:
        print(f"\n{YELLOW}安装缺失的包:{END}")
        print(f"  pip install numpy torch gym scipy")

    return all_ok

def test_windows_modules():
    """测试Windows专用模块"""
    print_header("4. 检查 Windows 兼容模块")

    modules = {
        'UTIL.win_pool': 'Windows进程池',
        'MISSION.dca.cython_func': 'DCA激光检测',
        'MISSION.dca_multiteam.cython_func': '多队激光检测',
        'ALGORITHM.conc_4hist.cython_func': '历史观察',
    }

    all_ok = True
    for module, desc in modules.items():
        try:
            __import__(module)
            print_success(f"{module:40s} - {desc}")
        except ImportError as e:
            print_error(f"{module:40s} - 导入失败")
            print(f"        错误: {e}")
            all_ok = False

    return all_ok

def test_scipy_compatibility():
    """测试Scipy兼容性"""
    print_header("5. 检查 Scipy 兼容性")

    try:
        from scipy.cluster.vq import kmeans2
        import numpy as np

        # 测试kmeans2是否正常工作 (不使用seed参数)
        data = np.random.rand(20, 2)
        centroid, labels = kmeans2(data, 3, iter=10, minit='++')

        print_success("kmeans2 函数正常工作 (无seed参数)")
        return True
    except Exception as e:
        print_error(f"kmeans2 测试失败: {e}")
        return False

def test_config_files():
    """测试配置文件"""
    print_header("6. 检查配置文件")

    import os
    configs = [
        'DOCS/examples/dca/quick_start/dca_debug_cpu.jsonc',
        'DOCS/examples/dca/quick_start/dca_train_gpu.jsonc',
        'DOCS/examples/dca/quick_start/dca_multiteam_2v2_cpu.jsonc',
    ]

    all_ok = True
    for config in configs:
        if os.path.exists(config):
            print_success(f"{config}")
        else:
            print_error(f"{config} - 文件不存在")
            all_ok = False

    return all_ok

def test_launcher_files():
    """测试启动器文件"""
    print_header("7. 检查启动器文件")

    import os
    files = {
        'run_dca.py': '交互式启动器',
        'run_dca.bat': 'Windows批处理启动器',
        'main_windows.py': 'Windows专用主程序',
    }

    all_ok = True
    for file, desc in files.items():
        if os.path.exists(file):
            print_success(f"{file:20s} - {desc}")
        else:
            print_error(f"{file:20s} - 文件不存在")
            all_ok = False

    return all_ok

def print_summary(results):
    """打印总结"""
    print_header("测试总结")

    total = len(results)
    passed = sum(results.values())

    print(f"总测试项: {total}")
    print(f"通过: {passed}")
    print(f"失败: {total - passed}")

    if all(results.values()):
        print(f"\n{GREEN}{BOLD}{'='*70}{END}")
        print(f"{GREEN}{BOLD}  🎉 恭喜! Windows环境配置完美!{END}")
        print(f"{GREEN}{BOLD}  您可以开始运行DCA实验了!{END}")
        print(f"{GREEN}{BOLD}{'='*70}{END}\n")

        print(f"{BLUE}下一步:{END}")
        print(f"  1. 双击 run_dca.bat")
        print(f"  2. 或运行: python run_dca.py")
        print(f"  3. 选择 [1] DCA调试配置")
        print(f"  4. 开始训练!\n")
        return True
    else:
        print(f"\n{YELLOW}{BOLD}{'='*70}{END}")
        print(f"{YELLOW}{BOLD}  ⚠ 部分测试未通过{END}")
        print(f"{YELLOW}{BOLD}{'='*70}{END}\n")

        print(f"{BLUE}修复建议:{END}")
        if not results['依赖包']:
            print(f"  • 安装缺失的Python包: pip install numpy torch gym scipy")
        if not results['Windows模块']:
            print(f"  • 确保在正确的目录: cd /path/to/jiayou")
        if not results['配置文件']:
            print(f"  • 重新下载完整项目")

        print(f"\n{BLUE}获取帮助:{END}")
        print(f"  • 查看 WINDOWS_故障排除.md")
        print(f"  • 查看 WINDOWS_用户必读.md\n")
        return False

def main():
    """主函数"""
    print(f"\n{BOLD}DCA Windows 环境测试工具{END}")
    print(f"检查Windows平台是否正确配置并可以运行DCA实验\n")

    results = {}

    # 运行所有测试
    results['Python版本'] = test_python_version()
    results['操作系统'] = test_platform()
    results['依赖包'] = test_dependencies()
    results['Windows模块'] = test_windows_modules()
    results['Scipy兼容性'] = test_scipy_compatibility()
    results['配置文件'] = test_config_files()
    results['启动器'] = test_launcher_files()

    # 打印总结
    success = print_summary(results)

    # 返回状态码
    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(main())
