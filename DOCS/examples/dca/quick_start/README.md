# DCA 快速启动配置模板 🚀

本目录包含精心设计的 DCA 实验配置模板,帮助你快速开始训练!

## 📁 配置文件列表

### 1. `dca_debug_cpu.jsonc` - 调试配置 ⚡
**适合**: 新手入门、快速测试、代码调试

```
智能体数量: 10 vs 12
并行环境: 8
运行设备: CPU
Episode时长: 100步
特点: 快速启动、启用渲染
```

**使用场景**:
- 第一次运行DCA
- 调试新功能
- 观察智能体行为
- 验证环境设置

**预计运行时间**: 几分钟即可看到初步结果

---

### 2. `dca_train_gpu.jsonc` - 正式训练配置 🔥
**适合**: GPU训练、完整实验、论文结果

```
智能体数量: 50 vs 55
并行环境: 64
运行设备: CUDA (GPU)
Episode时长: 180步
特点: 高性能、大规模并行
```

**使用场景**:
- 正式实验训练
- 性能基准测试
- 发表论文数据

**预计运行时间**: 数小时到数天 (取决于收敛情况)

---

### 3. `dca_multiteam_2v2_cpu.jsonc` - 双队对战配置 ⚔️
**适合**: 多智能体竞争研究、CPU训练

```
队伍数量: 2
每队智能体: 20
并行环境: 16
运行设备: CPU
特点: 自我博弈、竞争学习
```

**使用场景**:
- 研究竞争性策略
- 自我博弈训练
- 对抗性学习

**预计运行时间**: 中等 (CPU可能需要更长时间)

---

## 🎯 选择指南

### 我应该选择哪个配置?

**如果你是新手** → `dca_debug_cpu.jsonc`
- ✅ 快速启动
- ✅ 低资源消耗
- ✅ 易于调试

**如果你有GPU** → `dca_train_gpu.jsonc`
- ✅ 最快训练速度
- ✅ 完整实验配置
- ✅ 适合发表成果

**如果你研究竞争** → `dca_multiteam_2v2_cpu.jsonc`
- ✅ 多队博弈
- ✅ 复杂策略涌现
- ✅ CPU友好

---

## 🚀 快速开始

### 方法1: 使用启动器 (推荐)

```bash
# Windows: 双击
run_dca.bat

# 或者
python run_dca.py
```

然后在菜单中选择对应的配置。

### 方法2: 命令行直接运行

```bash
# 调试配置
python main.py --cfg DOCS/examples/dca/quick_start/dca_debug_cpu.jsonc

# GPU训练
python main.py --cfg DOCS/examples/dca/quick_start/dca_train_gpu.jsonc

# 双队对战
python main.py --cfg DOCS/examples/dca/quick_start/dca_multiteam_2v2_cpu.jsonc
```

---

## ⚙️ 配置参数对照表

| 参数 | debug_cpu | train_gpu | multiteam_2v2 |
|------|-----------|-----------|---------------|
| **智能体总数** | 22 | 105 | 40 |
| **并行环境** | 8 | 64 | 16 |
| **运行设备** | CPU | GPU | CPU |
| **Episode长度** | 100 | 180 | 120 |
| **训练轨迹** | 8 | 64 | 16 |
| **学习率** | 0.001 | 0.0005 | 0.0003 |
| **启用地形** | ❌ | ✅ | ❌ |
| **启用渲染** | ✅ | ❌ | ✅ |

---

## 🔧 自定义配置

### 修改智能体数量

```jsonc
"num_guards": 50,      // 你的RL队伍
"num_attackers": 55    // 对手数量
```

### 调整训练速度

```jsonc
// 更快 (使用更多资源)
"num_threads": 128,
"train_traj_needed": 128

// 更慢但稳定
"num_threads": 16,
"train_traj_needed": 16
```

### 切换设备

```jsonc
"device": "cpu"    // CPU训练
"device": "cuda"   // GPU训练 (需要NVIDIA显卡)
```

### 启用/禁用渲染

```jsonc
"render": true     // 启用 (可观察但变慢)
"render": false    // 禁用 (更快训练)
```

---

## 📊 预期结果

### DCA 单队训练

**前100个episode**:
- Win rate: 0% - 30%
- Reward: -50 到 0

**500-1000个episode**:
- Win rate: 40% - 60%
- Reward: 0 到 +30

**充分训练后** (5000+ episodes):
- Win rate: 60% - 80%
- Reward: +30 到 +60

### DCA_MULTITEAM 双队

**初期** (0-500 episodes):
- 各队 win rate 接近 50% (随机)

**中期** (500-2000):
- 策略分化,可能出现优势队

**后期** (2000+):
- 趋向平衡 (Nash equilibrium)

---

## 💡 优化建议

### CPU用户

1. **减少并行数**: `num_threads: 8-16`
2. **减少智能体**: `num_guards: 20-30`
3. **缩短episode**: `MaxEpisodeStep: 100`
4. **关闭地形**: `introduce_terrain: false`

### GPU用户

1. **增加并行数**: `num_threads: 64-128`
2. **增加批次**: `train_traj_needed: 64-128`
3. **启用地形**: `introduce_terrain: true`
4. **关闭渲染**: `render: false`

### 内存不足

1. **减少并行数**: `num_threads`
2. **使用fold**: `fold: 2-4`
3. **减少智能体数量**

---

## 🐛 故障排除

### 启动很慢
→ 正常现象,首次初始化需要时间
→ 减少 `num_threads` 可加快启动

### CUDA错误
→ 检查GPU驱动和PyTorch版本
→ 或改用 `"device": "cpu"`

### 内存溢出
→ 减少 `num_threads`
→ 减少智能体数量
→ 增加 `fold` 值

---

## 📚 下一步

完成快速开始后,你可以:

1. **阅读完整文档**: `DCA_快速入门.md`
2. **尝试自定义算法**: `ALGORITHM/`
3. **修改奖励函数**: `MISSION/dca/collective_assault_env.py`
4. **探索可视化**: 启用 `render: true`

---

**Happy Training! 🎉**

有问题请查看主文档或提交 issue。
