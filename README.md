# 游戏数据分析智能代理系统

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
![NextJS](https://img.shields.io/badge/Built_with-NextJS-blue)
![OpenAI API](https://img.shields.io/badge/Powered_by-OpenAI_API-orange)
![Python](https://img.shields.io/badge/Backend-Python-green)

本项目是一个基于AI代理的游戏数据分析系统，为游戏开发者和运营团队提供智能化的数据分析支持。系统采用多代理架构，每个代理专门负责不同类型的游戏数据分析任务。

## 系统组成

1. **Python后端** - 基于FastAPI的AI代理编排系统，处理数据分析逻辑
2. **Next.js前端** - 数据可视化界面，提供交互式分析体验

![系统架构图](screenshot.jpg)

## 快速开始

### 配置OpenAI API密钥

在终端中设置环境变量：

```bash
export OPENAI_API_KEY=your_api_key
```

或者在`python-backend`目录下创建`.env`文件：

```bash
OPENAI_API_KEY=your_api_key
```

详细配置说明请参考[OpenAI API文档](https://platform.openai.com/docs/libraries#create-and-export-an-api-key)。

### 安装依赖

安装后端依赖：

```bash
cd python-backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

安装前端依赖：

```bash
cd ui
npm install
```

### 启动应用

#### 方式一：同时启动前后端

```bash
cd ui
npm run dev
```

前端地址：[http://localhost:3000](http://localhost:3000)

#### 方式二：独立启动后端

```bash
cd python-backend
python -m uvicorn api:app --reload --port 8000
```

后端API地址：[http://localhost:8000](http://localhost:8000)

## 核心功能

### 智能代理系统

- **分流代理** - 理解用户查询意图，智能路由到专业代理
- **玩家行为分析代理** - 分析玩家游戏行为模式和偏好
- **性能分析代理** - 监控游戏性能指标和服务器状态
- **收入分析代理** - 分析游戏收入数据和付费转化
- **留存分析代理** - 分析玩家留存率和流失风险
- **可视化代理** - 生成数据图表和交互式仪表板

### 数据分析能力

- 多维度数据分析
- 实时性能监控
- 智能异常检测
- 趋势预测分析
- 个性化推荐

## 自定义扩展

系统采用模块化设计，支持轻松添加新的代理和分析功能。详细的扩展指南请参考[开发文档](GAME_DATA_ANALYTICS_GUIDE.md)。

## 使用示例

### 示例流程 #1：玩家行为分析

1. **查询玩家行为模式**
   - 用户："分析一下玩家ID 12345的游戏行为"
   - 分流代理识别意图，路由到玩家行为分析代理

2. **深度行为分析**
   - 玩家行为分析代理："我来分析玩家12345的行为数据。该玩家属于重度玩家类型，平均每日游戏时长3.5小时，偏好RPG和策略类游戏。"

3. **个性化推荐**
   - 用户："给这个玩家推荐一些合适的游戏内容"
   - 代理："基于该玩家的行为模式，推荐以下内容：新的副本挑战、限时活动参与、以及高级装备获取任务。"

### 示例流程 #2：收入分析

1. **收入数据查询**
   - 用户："显示本月的收入趋势"
   - 分流代理路由到收入分析代理

2. **收入分析报告**
   - 收入分析代理："本月收入呈上升趋势，总收入较上月增长15%。主要收入来源：内购道具(45%)、会员订阅(30%)、广告收入(25%)。"

3. **优化建议**
   - 用户："有什么提升收入的建议吗？"
   - 代理："建议优化付费转化漏斗，重点关注新手引导阶段的付费引导，预计可提升转化率8-12%。"

### 示例流程 #3：性能监控

1. **性能状态查询**
   - 用户："检查游戏服务器性能"
   - 系统路由到性能分析代理

2. **性能报告**
   - 性能分析代理："当前服务器状态良好，平均响应时间120ms，CPU使用率65%，内存使用率78%。检测到晚高峰时段有轻微延迟。"

3. **异常检测**
   - 代理自动检测："发现异常：服务器A在19:00-21:00时段响应时间超过阈值，建议进行负载均衡调整。"

这些示例展示了系统如何智能地将用户请求路由到合适的专业代理，并提供准确、有价值的游戏数据分析结果。

## 技术架构

### 后端技术栈
- **Python 3.9+** - 核心开发语言
- **FastAPI** - 高性能Web框架
- **OpenAI Agents SDK** - AI代理编排
- **Pydantic** - 数据验证和序列化
- **Uvicorn** - ASGI服务器

### 前端技术栈
- **Next.js 15** - React全栈框架
- **TypeScript** - 类型安全开发
- **Tailwind CSS** - 现代CSS框架
- **Radix UI** - 无障碍组件库
- **Lucide React** - 图标库

### 数据分析技术
- **Pandas** - 数据处理和分析
- **NumPy** - 数值计算
- **Plotly** - 交互式数据可视化
- **Scikit-learn** - 机器学习算法

## 贡献指南

欢迎提交Issue和Pull Request来改进本项目。请注意我们可能无法审查所有建议。

详细的开发指南请参考：[游戏数据分析系统开发指南](GAME_DATA_ANALYTICS_GUIDE.md)

## 许可证

本项目采用MIT许可证。详见[LICENSE](LICENSE)文件。
