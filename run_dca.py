#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
DCA Experiment Launcher - Windows Compatible
一键启动 DCA 和 DCA_MULTITEAM 实验的交互式启动器

使用方法:
    python run_dca.py
    或者直接双击 run_dca.bat (Windows)
"""
import os
import sys
import subprocess
from pathlib import Path

# 颜色输出支持 (Windows兼容)
try:
    import colorama
    colorama.init()
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'
except:
    GREEN = BLUE = YELLOW = RED = CYAN = BOLD = END = ''

class DCALauncher:
    def __init__(self):
        self.root_dir = Path(__file__).parent
        self.configs = {
            # === 快速开始 (推荐新手) ===
            '1': {
                'name': '⚡ DCA 调试配置 - CPU (推荐新手)',
                'file': 'DOCS/examples/dca/quick_start/dca_debug_cpu.jsonc',
                'desc': '10 vs 12智能体, CPU运行, 快速测试',
                'category': 'quick'
            },
            '2': {
                'name': '🔥 DCA 正式训练 - GPU',
                'file': 'DOCS/examples/dca/quick_start/dca_train_gpu.jsonc',
                'desc': '50 vs 55智能体, GPU加速, 完整训练',
                'category': 'quick'
            },
            '3': {
                'name': '⚔️ DCA_MULTITEAM 双队对战 - CPU',
                'file': 'DOCS/examples/dca/quick_start/dca_multiteam_2v2_cpu.jsonc',
                'desc': '2队 x 20智能体, 竞争学习',
                'category': 'quick'
            },

            # === 标准配置 ===
            '4': {
                'name': 'DCA - 单队标准训练 (50 vs 55)',
                'file': 'DOCS/examples/dca/example_dca.jsonc',
                'desc': '标准单队对抗场景',
                'category': 'standard'
            },
            '5': {
                'name': 'DCA_MULTITEAM - 双队标准 (50 vs 50)',
                'file': 'DOCS/examples/dca/conc_mt_dca_2team.jsonc',
                'desc': '两支50人队伍相互竞争',
                'category': 'standard'
            },
            '6': {
                'name': 'DCA_MULTITEAM - 三队大乱斗 (25x3)',
                'file': 'DOCS/examples/dca/conc_mt_dca.jsonc',
                'desc': '三支25人RL队伍混战',
                'category': 'standard'
            },

            # === 高级配置 ===
            '7': {
                'name': 'DCA - 大规模战斗 (100 vs 105)',
                'file': 'DOCS/examples/dca/adca_100vs+.jsonc',
                'desc': '大规模对抗场景 (高性能要求)',
                'category': 'advanced'
            },
        }

    def print_banner(self):
        banner = f"""
{CYAN}{'='*70}
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║          {BOLD}DCA 实验启动器 - HMAP Multi-Agent Platform{END}{CYAN}           ║
║                                                                   ║
║   🎮 Collective Assault 集体对抗环境                              ║
║   🤖 支持单队训练 & 多队竞争                                       ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
{'='*70}{END}
"""
        print(banner)

    def check_environment(self):
        """检查环境是否就绪"""
        print(f"\n{YELLOW}[检查] 正在检查运行环境...{END}")

        checks = []

        # 检查配置文件
        for key, config in self.configs.items():
            config_path = self.root_dir / config['file']
            exists = config_path.exists()
            checks.append((f"配置文件: {config['file']}", exists))
            if not exists:
                print(f"{RED}✗ 缺失: {config['file']}{END}")

        # 检查关键目录
        critical_dirs = [
            'MISSION/dca',
            'MISSION/dca_multiteam',
            'ALGORITHM/conc_4hist',
            'ALGORITHM/conc_mt',
        ]

        for dir_name in critical_dirs:
            dir_path = self.root_dir / dir_name
            exists = dir_path.exists()
            checks.append((f"目录: {dir_name}", exists))
            if not exists:
                print(f"{RED}✗ 缺失: {dir_name}{END}")

        # 检查 main.py
        main_exists = (self.root_dir / 'main.py').exists()
        checks.append(("main.py", main_exists))

        all_ok = all(check[1] for check in checks)

        if all_ok:
            print(f"{GREEN}✓ 所有检查通过!{END}")
        else:
            print(f"{RED}✗ 环境检查失败，请确保所有必要文件存在{END}")
            return False

        return True

    def show_menu(self):
        """显示实验选择菜单"""
        print(f"\n{BOLD}请选择要运行的实验:{END}\n")

        # 按类别组织配置
        categories = {
            'quick': f'{GREEN}=== 🚀 快速开始 (推荐) ==={END}',
            'standard': f'{BLUE}=== 📚 标准配置 ==={END}',
            'advanced': f'{YELLOW}=== 🔬 高级配置 ==={END}'
        }

        for cat_key, cat_name in categories.items():
            # 打印类别标题
            cat_configs = {k: v for k, v in self.configs.items() if v.get('category') == cat_key}
            if cat_configs:
                print(f"\n{cat_name}")
                for key in sorted(cat_configs.keys()):
                    config = self.configs[key]
                    print(f"{CYAN}[{key}]{END} {BOLD}{config['name']}{END}")
                    print(f"    {config['desc']}\n")

        print(f"\n{CYAN}[c]{END} 自定义配置文件路径")
        print(f"{CYAN}[q]{END} 退出\n")

    def get_device_choice(self):
        """选择运行设备"""
        print(f"\n{BOLD}选择运行设备:{END}")
        print(f"{CYAN}[1]{END} CPU (推荐用于调试)")
        print(f"{CYAN}[2]{END} GPU (CUDA)")

        while True:
            choice = input(f"\n{GREEN}➜{END} 请选择设备 (1/2, 默认=1): ").strip() or '1'
            if choice in ['1', '2']:
                return 'cpu' if choice == '1' else 'cuda'
            print(f"{RED}无效选择，请输入 1 或 2{END}")

    def get_num_threads(self):
        """选择并行线程数"""
        print(f"\n{BOLD}选择并行环境数量:{END}")
        print(f"  较少线程 = 更快启动, 较慢训练")
        print(f"  较多线程 = 较慢启动, 更快训练")
        print(f"  {YELLOW}推荐: 16-64{END}")

        while True:
            choice = input(f"\n{GREEN}➜{END} 并行环境数 (默认=16): ").strip() or '16'
            try:
                num = int(choice)
                if 1 <= num <= 256:
                    return num
                print(f"{RED}请输入 1-256 之间的数字{END}")
            except ValueError:
                print(f"{RED}请输入有效的数字{END}")

    def create_temp_config(self, base_config, device, num_threads):
        """创建临时配置文件"""
        import json
        import re

        config_path = self.root_dir / base_config
        temp_config_path = self.root_dir / 'TEMP' / 'run_config.jsonc'
        temp_config_path.parent.mkdir(exist_ok=True)

        # 读取基础配置
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 移除注释以解析JSON
        content_no_comment = re.sub(r'//.*', '', content)
        config_data = json.loads(content_no_comment)

        # 修改配置
        if 'config.py->GlobalConfig' in config_data:
            config_data['config.py->GlobalConfig']['device'] = device
            config_data['config.py->GlobalConfig']['num_threads'] = num_threads

            # Windows兼容：减少测试频率
            if 'test_interval' in config_data['config.py->GlobalConfig']:
                config_data['config.py->GlobalConfig']['test_interval'] = str(num_threads * 4)

        # 保存临时配置
        with open(temp_config_path, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=4, ensure_ascii=False)

        return str(temp_config_path.relative_to(self.root_dir))

    def run_experiment(self, config_file, device=None, num_threads=None):
        """运行实验"""
        # 询问运行参数
        if device is None:
            device = self.get_device_choice()

        if num_threads is None:
            num_threads = self.get_num_threads()

        # 创建临时配置
        print(f"\n{YELLOW}[准备] 生成运行配置...{END}")
        temp_config = self.create_temp_config(config_file, device, num_threads)

        print(f"\n{GREEN}{'='*70}{END}")
        print(f"{BOLD}准备启动实验:{END}")
        print(f"  配置文件: {CYAN}{config_file}{END}")
        print(f"  运行设备: {CYAN}{device.upper()}{END}")
        print(f"  并行环境: {CYAN}{num_threads}{END}")
        print(f"{GREEN}{'='*70}{END}\n")

        confirm = input(f"{YELLOW}确认启动? (y/n, 默认=y): {END}").strip().lower() or 'y'

        if confirm != 'y':
            print(f"{RED}已取消{END}")
            return

        # 运行实验
        print(f"\n{GREEN}🚀 正在启动实验...{END}\n")

        cmd = [sys.executable, 'main.py', '--cfg', temp_config]

        try:
            subprocess.run(cmd, cwd=str(self.root_dir))
        except KeyboardInterrupt:
            print(f"\n\n{YELLOW}⚠ 实验被用户中断{END}")
        except Exception as e:
            print(f"\n{RED}✗ 运行出错: {e}{END}")

    def run(self):
        """主运行循环"""
        self.print_banner()

        # 检查环境
        if not self.check_environment():
            input(f"\n{RED}按回车键退出...{END}")
            return

        while True:
            self.show_menu()
            choice = input(f"{GREEN}➜{END} 请选择 (1-{len(self.configs)}/c/q): ").strip().lower()

            if choice == 'q':
                print(f"\n{CYAN}再见! 👋{END}\n")
                break

            elif choice == 'c':
                config_path = input(f"\n{GREEN}➜{END} 请输入配置文件路径: ").strip()
                if os.path.exists(config_path):
                    self.run_experiment(config_path)
                else:
                    print(f"{RED}✗ 文件不存在: {config_path}{END}")
                    input(f"按回车继续...")

            elif choice in self.configs:
                config = self.configs[choice]
                print(f"\n{BOLD}已选择: {config['name']}{END}")
                self.run_experiment(config['file'])

            else:
                print(f"{RED}无效选择，请重试{END}")

def main():
    launcher = DCALauncher()
    launcher.run()

if __name__ == '__main__':
    main()
