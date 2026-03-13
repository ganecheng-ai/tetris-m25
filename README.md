# Tetris M25 俄罗斯方块游戏

一个使用 Python 和 Pygame 开发的经典俄罗斯方块游戏，支持简体中文界面。

## 功能特性

- 7种经典方块类型 (I, O, T, S, Z, J, L)
- 方块旋转、左右移动、软降、硬降
- 分数和等级系统
- 消行得分 (单行/双行/三行/四行)
- 游戏暂停功能
- 简体中文界面
- 完善的日志系统

## 操作说明

| 按键 | 功能 |
|------|------|
| ← → | 左右移动 |
| ↑ | 顺时针旋转 |
| ↓ | 软降 (加快下落) |
| 空格 | 硬降 (直接落底) |
| P | 暂停/继续 |
| ESC | 返回主菜单 |

## 运行方式

### 安装依赖

```bash
pip install -e .
```

或

```bash
pip install pygame
```

### 运行游戏

```bash
python3 -m tetris.main
```

或

```bash
python3 tetris/main.py
```

## 项目结构

```
tetris-m25/
├── tetris/
│   ├── __init__.py      # 包初始化
│   ├── main.py          # 主程序入口
│   ├── game.py          # 游戏核心逻辑
│   ├── tetromino.py     # 方块定义
│   ├── renderer.py      # 界面渲染
│   └── logger.py        # 日志系统
├── tests/
│   └── test_game.py     # 测试用例
├── pyproject.toml       # 项目配置
└── README.md            # 项目说明
```

## 开发说明

- Python 3.8+
- GUI框架: Pygame
- 代码质量优先

## 版本

当前版本: 0.1.1