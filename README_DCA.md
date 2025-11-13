# DCA 实验环境 - 快速开始 🚀

> Collective Assault 多智能体强化学习环境

## ⚡ 一键启动 (最快方式)

### Windows 用户
```
双击运行: run_dca.bat
```

### Linux/Mac 用户
```bash
python run_dca.py
```

---

## 📋 可用实验

启动器提供 **7 种预配置实验**:

### 🚀 快速开始 (推荐新手)
1. **DCA 调试配置 - CPU** ⭐ 新手首选
   - 10 vs 12 智能体
   - CPU运行, 快速测试

2. **DCA 正式训练 - GPU**
   - 50 vs 55 智能体
   - GPU加速

3. **DCA_MULTITEAM 双队对战 - CPU**
   - 2队 x 20 智能体
   - 竞争学习

### 📚 更多配置
- 标准单队训练
- 双队/三队对战
- 大规模战斗 (100+ 智能体)

---

## 📚 详细文档

- **新手入门**: 阅读 `DCA_快速入门.md`
- **使用说明**: 阅读 `一键启动说明.md`
- **配置模板**: 查看 `DOCS/examples/dca/quick_start/`

---

## 🎯 快速测试 (30秒开始)

```bash
# 1. 启动
python run_dca.py

# 2. 选择实验
输入: 1

# 3. 使用默认参数
直接回车

# 4. 开始训练!
```

---

## 🛠 环境要求

- Python 3.7+
- Windows 10/11 或 Linux
- 依赖: `pip install numpy torch gym scipy`

---

## 📦 项目结构

```
├── run_dca.py              ⭐ 启动器
├── run_dca.bat             ⭐ Windows快捷方式
├── DCA_快速入门.md         📚 完整指南
├── DOCS/examples/dca/      ⚙️ 配置文件
├── MISSION/dca/            🎮 DCA环境
└── MISSION/dca_multiteam/  🎮 多队环境
```

---

## 🎮 环境介绍

### DCA (单队训练)
- **场景**: 你的RL队伍 vs 脚本AI对手
- **适合**: 学习基础协作、算法测试

### DCA_MULTITEAM (多队竞争)
- **场景**: 2-N支队伍相互竞争
- **适合**: 研究竞争策略、博弈学习

---

## 💡 第一次使用?

1. 运行 `run_dca.bat` 或 `python run_dca.py`
2. 选择 `[1] DCA 调试配置 - CPU`
3. 观察智能体行为和训练过程
4. 阅读 `DCA_快速入门.md` 深入学习

---

## 🆘 需要帮助?

- **详细文档**: `DCA_快速入门.md`
- **配置说明**: `DOCS/examples/dca/quick_start/README.md`
- **常见问题**: 查看 `一键启动说明.md` 的故障排除部分

---

**开始你的多智能体强化学习之旅! 🎉**
