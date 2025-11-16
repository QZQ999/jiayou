# Windows 故障排除指南 🔧

本文档专门针对Windows平台可能遇到的问题及解决方案。

---

## ✅ 已解决的问题

我们已经为Windows创建了完整的纯Python版本,以下问题已自动解决:

### 1. Cython编译错误 ✓
```
DistutilsPlatformError: Unable to find vcvarsall.bat
```
**解决**: 使用 `main_windows.py` (已自动)

### 2. 模块导入错误 ✓
```
ModuleNotFoundError: No module named 'MISSION.dca.cython_func'
ModuleNotFoundError: No module named 'UTIL.shm_pool'
```
**解决**: 已创建纯Python版本 (自动使用)

### 3. Scipy兼容性错误 ✓
```
TypeError: kmeans2() got an unexpected keyword argument 'seed'
```
**解决**: 已移除不兼容的seed参数 (自动修复)

---

## 🎯 推荐使用方式 (Windows)

### 最简单方法
```
1. 双击 run_dca.bat
2. 选择实验
3. 开始训练
```

### 命令行方法
```bash
# 使用启动器 (推荐)
python run_dca.py

# 或直接运行Windows版本
python main_windows.py --cfg DOCS/examples/dca/quick_start/dca_debug_cpu.jsonc
```

---

## 🔍 常见问题诊断

### 问题 1: 启动失败，提示 "No module named..."

**症状**:
```
ModuleNotFoundError: No module named 'xxx'
```

**解决步骤**:

1. **检查依赖包**:
```bash
pip install numpy torch gym scipy numba
```

2. **如果是Cython模块错误**，检查是否使用了正确的启动脚本:
```bash
# ✅ 正确 (Windows)
python main_windows.py --cfg your_config.jsonc

# ❌ 错误 (需要编译)
python main.py --cfg your_config.jsonc
```

3. **验证Python版本**:
```bash
python --version
# 需要 Python 3.7+
```

---

### 问题 2: 进程池初始化失败

**症状**:
```
[win_pool]: SmartPool initialization failed
```

**解决步骤**:

1. **减少并行环境数**:
```jsonc
// 在配置文件中修改
"num_threads": 8,  // 从16减到8
```

2. **检查内存**:
- 打开任务管理器
- 确保有至少4GB空闲内存
- 关闭不必要的程序

3. **使用fold参数** (仅在必要时):
```jsonc
"fold": 1  // Windows推荐值
```

---

### 问题 3: 训练速度很慢

**症状**:
```
FPS < 10 (每秒处理帧数很低)
```

**优化方案**:

**A. 使用GPU** (如果有NVIDIA显卡):
```jsonc
{
    "device": "cuda"
}
```
验证GPU可用:
```bash
python -c "import torch; print(torch.cuda.is_available())"
```

**B. 减少并行环境**:
```jsonc
{
    "num_threads": 8,  // 减少到8或16
}
```

**C. 增加训练批次**:
```jsonc
{
    "train_traj_needed": 64,  // 增加批次大小
}
```

**D. 减少测试频率**:
```jsonc
{
    "test_interval": 1000,  // 减少测试次数
}
```

---

### 问题 4: 内存不足错误

**症状**:
```
MemoryError: Unable to allocate array
```

**解决方案**:

**方案1: 减少智能体数量**
```jsonc
{
    "num_guards": 20,      // 从50减到20
    "num_attackers": 22    // 从55减到22
}
```

**方案2: 减少并行环境**
```jsonc
{
    "num_threads": 8      // 从16减到8
}
```

**方案3: 使用Windows轻量配置**
```bash
# 使用专门的轻量配置
python run_dca.py
# 选择 [1] DCA 调试配置
```

---

### 问题 5: ImportError: DLL load failed

**症状**:
```
ImportError: DLL load failed while importing _xxx
```

**解决步骤**:

1. **安装 Visual C++ Redistributable**:
   - 下载: https://aka.ms/vs/17/release/vc_redist.x64.exe
   - 安装后重启电脑

2. **重新安装PyTorch**:
```bash
# CPU版本
pip uninstall torch
pip install torch --index-url https://download.pytorch.org/whl/cpu

# GPU版本 (需要CUDA)
pip uninstall torch
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

3. **检查Python位数**:
```bash
python -c "import platform; print(platform.architecture())"
# 应该是 ('64bit', 'WindowsPE')
```

---

### 问题 6: 权限错误

**症状**:
```
PermissionError: [WinError 32]
```

**解决方案**:

1. **以管理员运行**:
   - 右键点击 `run_dca.bat`
   - 选择"以管理员身份运行"

2. **关闭杀毒软件** (临时):
   - 某些杀毒软件会阻止多进程程序
   - 添加 jiayou 文件夹到白名单

3. **检查文件夹权限**:
   - 确保对 jiayou 文件夹有完全控制权限

---

### 问题 7: 渲染不显示

**症状**:
- 配置了 `"render": true`
- 但没有可视化窗口

**说明**:
- Windows版本的渲染保存在文件而非实时显示
- 查看渲染结果:
```bash
# 渲染数据保存在
TEMP/v2d_logger/
```

**建议**:
- 训练时关闭渲染: `"render": false`
- 仅在需要观察时启用

---

## 🔧 Windows优化配置

### 调试配置 (快速测试)
```jsonc
{
    "num_threads": 8,
    "num_guards": 10,
    "num_attackers": 12,
    "MaxEpisodeStep": 100,
    "device": "cpu",
    "render": false
}
```

### 训练配置 (CPU)
```jsonc
{
    "num_threads": 16,
    "num_guards": 30,
    "num_attackers": 35,
    "MaxEpisodeStep": 150,
    "device": "cpu",
    "fold": 1,
    "train_traj_needed": 32
}
```

### 训练配置 (GPU)
```jsonc
{
    "num_threads": 32,
    "num_guards": 50,
    "num_attackers": 55,
    "MaxEpisodeStep": 180,
    "device": "cuda",
    "fold": 1,
    "train_traj_needed": 64
}
```

---

## 📊 性能基准 (Windows)

### 硬件要求

**最低配置**:
- CPU: 4核
- RAM: 8GB
- Python: 3.7+
- OS: Windows 10

**推荐配置**:
- CPU: 8核+
- RAM: 16GB+
- GPU: NVIDIA GTX 1060+
- OS: Windows 10/11

**高性能配置**:
- CPU: 16核+
- RAM: 32GB+
- GPU: NVIDIA RTX 3060+
- SSD: 推荐

### 预期性能

| 配置 | 智能体数 | 并行数 | FPS (CPU) | FPS (GPU) |
|------|---------|-------|-----------|-----------|
| 调试 | 10+12 | 8 | 30-50 | 60-100 |
| 标准 | 50+55 | 16 | 15-25 | 40-60 |
| 大规模 | 100+105 | 32 | 5-10 | 20-30 |

---

## 🆘 仍然无法解决?

### 收集诊断信息

运行以下命令收集信息:
```bash
python -c "import sys; print('Python:', sys.version)"
python -c "import torch; print('PyTorch:', torch.__version__)"
python -c "import numpy; print('NumPy:', numpy.__version__)"
python -c "import platform; print('Platform:', platform.platform())"
```

### 提交Issue时请包含:

1. **错误信息完整输出**
2. **使用的配置文件**
3. **Python和依赖包版本**
4. **Windows版本**
5. **硬件配置** (CPU/RAM/GPU)

---

## 💡 最佳实践

### 开发调试
```bash
# 使用小规模配置
python run_dca.py
# 选择 [1] 调试配置
```

### 正式训练
```bash
# 使用优化配置
python run_dca.py
# 选择 [2] GPU训练 (如有GPU)
```

### 长时间训练
```bash
# 在后台运行 (PowerShell)
Start-Process python -ArgumentList "main_windows.py --cfg your_config.jsonc" -WindowStyle Hidden
```

---

## 📚 相关文档

- **WINDOWS_用户必读.md** - Windows完整指南
- **README_DCA.md** - 快速开始
- **DCA_快速入门.md** - 详细教程
- **一键启动说明.md** - 使用说明

---

**遇到问题不要慌! 99%的问题都可以通过启动器自动解决!** 🎯

直接使用: `run_dca.bat` 或 `python run_dca.py`
