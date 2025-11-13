# DCA 实验快速入门指南 🚀

## 📋 目录

- [环境要求](#环境要求)
- [一键启动](#一键启动)
- [实验类型说明](#实验类型说明)
- [配置文件说明](#配置文件说明)
- [常见问题](#常见问题)

---

## 🔧 环境要求

### 必需软件
- **Python**: 3.7 或更高版本
- **操作系统**: Windows 10/11 (Linux也支持)

### Python依赖包
```bash
pip install numpy torch gym scipy numba
```

或使用项目的 requirements.txt:
```bash
pip install -r requirements.txt
```

---

## 🎮 一键启动

### Windows 用户

**方法 1: 双击批处理文件**
```
直接双击: run_dca.bat
```

**方法 2: 命令行**
```bash
python run_dca.py
```

### Linux/Mac 用户

```bash
python run_dca.py
```

---

## 🎯 实验类型说明

### 1️⃣ DCA - 单队训练 (推荐新手)

**场景**: 你的 RL 智能体队伍 vs 脚本 AI 对手

```
配置: DOCS/examples/dca/example_dca.jsonc
智能体数量: 50 (蓝方 RL) vs 55 (红方脚本AI)
训练难度: ⭐⭐⭐
```

**适用场景**:
- 学习基础的多智能体协作
- 测试新算法
- 快速原型验证

**胜利条件**:
- 消灭所有敌方单位
- 或在时间结束时存活率更高

---

### 2️⃣ DCA_MULTITEAM - 双队对战

**场景**: 两支 RL 队伍相互竞争

```
配置: DOCS/examples/dca/conc_mt_dca_2team.jsonc
智能体数量: 50 (蓝方) vs 50 (红方)
训练难度: ⭐⭐⭐⭐
```

**适用场景**:
- 研究竞争性多智能体学习
- 测试对抗性策略
- 自我博弈训练

**胜利判定**:
- 基于最终存活智能体数量排名
- 第1名: +10 奖励
- 第2名: 0 奖励

---

### 3️⃣ DCA_MULTITEAM - 三队大乱斗

**场景**: 三支 RL 队伍混战

```
配置: DOCS/examples/dca/conc_mt_dca.jsonc
智能体数量: 25 (蓝方) vs 25 (红方) vs 25 (绿方)
训练难度: ⭐⭐⭐⭐⭐
```

**适用场景**:
- 复杂多方博弈研究
- 联盟与背叛策略
- 高级竞争场景

**胜利判定**:
- 第1名: +20 奖励
- 第2名: +10 奖励
- 第3名: 0 奖励
- 平局: -10 惩罚

---

### 4️⃣ DCA - 大规模战斗

**场景**: 大规模对抗 (100+ 智能体)

```
配置: DOCS/examples/dca/adca_100vs+.jsonc
智能体数量: 100 (蓝方) vs 105 (红方)
训练难度: ⭐⭐⭐⭐
```

**适用场景**:
- 可扩展性测试
- 大规模协作研究
- 性能压力测试

---

## ⚙️ 配置文件说明

### 核心配置参数

#### 全局配置 (GlobalConfig)

```jsonc
"config.py->GlobalConfig": {
    "note": "实验名称",           // 实验结果保存路径
    "env_name": "dca",           // 环境类型: dca 或 dca_multiteam
    "num_threads": 64,           // 并行环境数量 (越多训练越快)
    "device": "cuda",            // 使用设备: cpu 或 cuda
    "seed": 22333,               // 随机种子
    "max_n_episode": 1000000     // 最大训练轮数
}
```

#### 环境配置 (ScenarioConfig)

**DCA 单队训练**:
```jsonc
"MISSION.dca.collective_assault_parallel_run.py->ScenarioConfig": {
    "num_guards": 50,            // RL控制的守卫数量
    "num_attackers": 55,         // 脚本AI攻击者数量
    "MaxEpisodeStep": 180,       // 每局最大步数
    "introduce_terrain": true,   // 是否启用地形
    "render": false              // 是否渲染 (仅0号环境)
}
```

**DCA_MULTITEAM 多队对战**:
```jsonc
"MISSION.dca_multiteam.collective_assault_parallel_run.py->ScenarioConfig": {
    "N_TEAM": 2,                 // 队伍数量 (2-N)
    "N_AGENT_EACH_TEAM": [50, 50], // 每队智能体数量
    "MaxEpisodeStep": 150,       // 每局最大步数
    "TEAM_NAMES": [              // 每队使用的算法
        "ALGORITHM.conc_mt.foundation->ReinforceAlgorithmFoundation",
        "TEMP.TEAM2.ALGORITHM.conc_mt.foundation->ReinforceAlgorithmFoundation"
    ]
}
```

#### 算法配置 (AlgorithmConfig)

```jsonc
"ALGORITHM.conc_mt.foundation.py->AlgorithmConfig": {
    "lr": 0.0003,                // 学习率
    "gamma": 0.99,               // 折扣因子
    "ppo_epoch": 24,             // PPO训练轮数
    "train_traj_needed": 32      // 训练所需轨迹数
}
```

---

## 🎨 智能体动作空间

每个智能体有 **7 种离散动作**:

| 动作编号 | 动作名称 | 说明 |
|---------|---------|------|
| 0 | 无操作 | 保持当前状态 |
| 1 | +X 移动 | 向X正方向移动 |
| 2 | -X 移动 | 向X负方向移动 |
| 3 | +Y 移动 | 向Y正方向移动 |
| 4 | -Y 移动 | 向Y负方向移动 |
| 5 | 左旋转 | 逆时针旋转 |
| 6 | 右旋转 | 顺时针旋转 |

**注意**: 射击自动启用 (can_fire = True)

---

## 📊 训练监控

### 查看训练日志

训练过程中会输出:
```
[task runner]: (实验名称) Finished episode 64, frame 11520.
  | team-0: win rate: 0.450, recent reward 12.340
```

### 可视化渲染

在配置文件中设置:
```jsonc
"render": true  // 启用3D可视化 (仅0号环境)
```

然后访问: `TEMP/v2d_logger/` 查看渲染结果

---

## 🐛 常见问题

### Q1: ImportError: No module named 'xxx'

**解决方法**:
```bash
pip install xxx
# 或
pip install -r requirements.txt
```

### Q2: CUDA out of memory

**解决方法**:
1. 减少并行环境数量 (num_threads)
2. 使用 CPU 训练: `"device": "cpu"`
3. 减少智能体数量

### Q3: 训练速度太慢

**优化建议**:
1. **增加并行环境**: `"num_threads": 64` → `128`
2. **使用 GPU**: `"device": "cuda"`
3. **减少测试频率**: `"test_interval": 2048` → `4096`
4. **关闭渲染**: `"render": false`

### Q4: Windows下进程池错误

**解决方法**:
确保在配置中设置:
```jsonc
"fold": 1  // Windows推荐使用1
```

### Q5: 如何恢复训练?

在算法配置中设置:
```jsonc
"load_checkpoint": true,
"checkpoint_path": "TEMP/your_experiment/checkpoints/"
```

---

## 📝 自定义配置示例

### 创建快速调试配置

**文件**: `DOCS/examples/dca/debug_dca.jsonc`

```jsonc
{
    "config.py->GlobalConfig": {
        "note": "debug_run",
        "env_name": "dca",
        "num_threads": 4,        // 少量线程快速启动
        "device": "cpu",         // CPU调试
        "max_n_episode": 100,    // 少量episode
        "test_interval": 10      // 频繁测试
    },
    "MISSION.dca.collective_assault_parallel_run.py->ScenarioConfig": {
        "num_guards": 10,        // 少量智能体
        "num_attackers": 12,
        "MaxEpisodeStep": 50,    // 短episode
        "render": true           // 启用渲染观察
    }
}
```

---

## 🚀 进阶使用

### 1. 使用自己的算法

将你的算法放在 `ALGORITHM/your_algorithm/` 下,然后在配置中引用:

```jsonc
"TEAM_NAMES": [
    "ALGORITHM.your_algorithm.foundation->YourAlgorithmClass"
]
```

### 2. 修改奖励函数

编辑 `MISSION/dca/collective_assault_env.py` 的 `reward()` 方法

### 3. 自定义观察空间

编辑 `MISSION/dca/collective_assault_env.py` 的 `observation()` 方法

---

## 📚 相关文档

- **完整文档**: [HMAP Documentation](https://github.com/your-repo)
- **算法示例**: `ALGORITHM/example_foundation.py`
- **环境API**: `MISSION/dca/collective_assault_env.py`

---

## 💡 提示与技巧

1. **先小后大**: 从少量智能体和线程开始测试
2. **渐进训练**: 先训练简单场景,再增加难度
3. **保存检查点**: 定期保存训练进度
4. **监控指标**: 关注 win rate 和 reward 变化趋势
5. **可视化**: 使用渲染功能观察智能体行为

---

## 🎓 学习路径建议

### 初级 (第1-2周)
1. 运行 DCA 单队训练
2. 理解基础配置参数
3. 观察训练曲线

### 中级 (第3-4周)
1. 尝试 DCA_MULTITEAM 双队对战
2. 调整算法超参数
3. 分析竞争策略

### 高级 (第5周+)
1. 三队大乱斗实验
2. 自定义算法实现
3. 大规模场景测试

---

**祝你实验顺利! 🎉**

有问题请查看 issues 或联系维护者。
