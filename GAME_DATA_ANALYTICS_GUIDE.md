# 游戏数据分析系统开发指南

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
![NextJS](https://img.shields.io/badge/Built_with-NextJS-blue)
![OpenAI API](https://img.shields.io/badge/Powered_by-OpenAI_API-orange)
![Python](https://img.shields.io/badge/Backend-Python-green)

## 项目概述

本项目是一个基于AI代理的游戏数据分析系统，旨在为游戏开发者和运营团队提供智能化的数据分析支持。系统采用多代理架构，每个代理专门负责不同类型的游戏数据分析任务。

## 系统架构

### 核心组件

1. **Python后端** - 基于FastAPI的AI代理编排系统
2. **Next.js前端** - 数据可视化和交互界面
3. **AI代理系统** - 专业化的数据分析代理

### 代理架构设计

#### 主要代理类型

1. **分流代理 (Triage Agent)**
   - 负责理解用户查询意图
   - 将请求路由到合适的专业代理
   - 处理多轮对话的上下文管理

2. **玩家行为分析代理 (Player Behavior Agent)**
   - 分析玩家游戏行为模式
   - 识别玩家类型和偏好
   - 提供个性化推荐建议

3. **游戏性能分析代理 (Performance Analytics Agent)**
   - 监控游戏性能指标
   - 分析服务器负载和响应时间
   - 识别性能瓶颈和优化建议

4. **收入分析代理 (Revenue Analytics Agent)**
   - 分析游戏收入数据
   - 跟踪付费转化率
   - 提供商业化策略建议

5. **留存分析代理 (Retention Analytics Agent)**
   - 分析玩家留存率
   - 识别流失风险玩家
   - 提供留存优化策略

6. **数据可视化代理 (Visualization Agent)**
   - 生成各类数据图表
   - 创建交互式仪表板
   - 导出分析报告

### 数据模型

#### 游戏分析上下文 (GameAnalyticsContext)

```python
class GameAnalyticsContext(BaseModel):
    game_id: str | None = None
    player_id: str | None = None
    time_range: dict | None = None  # {"start": "2024-01-01", "end": "2024-01-31"}
    analysis_type: str | None = None
    metrics: list[str] | None = None
    filters: dict | None = None
```

#### 支持的分析类型

- `player_behavior` - 玩家行为分析
- `performance` - 性能分析
- `revenue` - 收入分析
- `retention` - 留存分析
- `engagement` - 参与度分析
- `conversion` - 转化分析

## 功能特性

### 核心功能

1. **智能查询理解**
   - 自然语言查询解析
   - 意图识别和参数提取
   - 多轮对话支持

2. **多维度数据分析**
   - 玩家行为分析
   - 游戏性能监控
   - 收入和转化分析
   - 留存和流失分析

3. **可视化展示**
   - 实时数据仪表板
   - 交互式图表
   - 自定义报告生成

4. **智能洞察**
   - 异常检测
   - 趋势预测
   - 优化建议

### 安全特性

1. **输入验证**
   - 查询相关性检查
   - 恶意输入防护
   - 数据访问权限控制

2. **数据保护**
   - 敏感数据脱敏
   - 访问日志记录
   - 合规性检查

## 技术栈

### 后端技术
- **Python 3.9+**
- **FastAPI** - Web框架
- **OpenAI Agents SDK** - AI代理编排
- **Pydantic** - 数据验证
- **Uvicorn** - ASGI服务器

### 前端技术
- **Next.js 15** - React框架
- **TypeScript** - 类型安全
- **Tailwind CSS** - 样式框架
- **Radix UI** - 组件库
- **Lucide React** - 图标库

### 数据分析
- **Pandas** - 数据处理
- **NumPy** - 数值计算
- **Plotly** - 数据可视化
- **Scikit-learn** - 机器学习

## 开发原则

### 设计原则

1. **如无必要，不增实体** - 复用现有组件和架构
2. **专业化代理** - 每个代理专注特定分析领域
3. **可扩展性** - 支持新代理和功能的轻松添加
4. **用户友好** - 直观的界面和自然的交互方式

### 代码规范

1. **类型安全** - 使用TypeScript和Pydantic
2. **错误处理** - 完善的异常处理机制
3. **日志记录** - 详细的操作日志
4. **测试覆盖** - 单元测试和集成测试

## 部署指南

### 环境要求

- Python 3.9+
- Node.js 18+
- OpenAI API Key

### 本地开发

1. **后端启动**
```bash
cd python-backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m uvicorn api:app --reload --port 8000
```

2. **前端启动**
```bash
cd ui
npm install
npm run dev
```

### 环境变量

```bash
# OpenAI配置
OPENAI_API_KEY=your_api_key

# 数据库配置（如需要）
DATABASE_URL=your_database_url

# 其他配置
ENVIRONMENT=development
LOG_LEVEL=INFO
```

## 扩展指南

### 添加新代理

1. 在`main.py`中定义新代理
2. 实现相关工具函数
3. 配置代理间的交接逻辑
4. 更新前端界面显示

### 添加新分析类型

1. 扩展`GameAnalyticsContext`模型
2. 实现对应的分析工具
3. 更新代理指令和路由逻辑
4. 添加前端可视化组件

## 许可证

本项目采用MIT许可证。详见[LICENSE](LICENSE)文件。
