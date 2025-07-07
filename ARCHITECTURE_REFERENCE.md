# 多智能体系统架构参考资料

## Anthropic多智能体研究系统架构

### 核心架构模式
- **Orchestrator-Worker模式**: Lead agent协调，subagents并行执行
- **动态任务分解**: 根据查询复杂度自动分解任务
- **并行处理**: 多个subagents同时工作，提高效率
- **状态管理**: 分布式上下文管理和错误恢复

### 关键设计原则

#### 1. Prompt Engineering
- **Think like your agents**: 理解agent行为模式
- **Teach the orchestrator how to delegate**: 明确任务分配
- **Scale effort to query complexity**: 根据复杂度调整资源
- **Tool design and selection are critical**: 工具接口设计至关重要
- **Let agents improve themselves**: 自我优化能力
- **Start wide, then narrow down**: 先广后精的搜索策略
- **Guide the thinking process**: 引导思考过程
- **Parallel tool calling**: 并行工具调用提升性能

#### 2. 系统架构特点
- **Multi-agent coordination**: 多agent协调机制
- **Separation of concerns**: 关注点分离
- **Context window management**: 上下文窗口管理
- **Token efficiency**: 令牌使用效率优化
- **Error handling**: 错误处理和恢复机制

#### 3. 评估和测试
- **Start evaluating immediately**: 立即开始评估
- **LLM-as-judge evaluation**: LLM作为评判者
- **Human evaluation**: 人工评估补充
- **End-state evaluation**: 终态评估
- **Long-horizon conversation management**: 长对话管理

### Prompt设计模式

#### Citations Agent
- 专门负责为研究报告添加正确引用
- 保持内容100%不变，只添加引用
- 避免不必要的引用，专注于关键事实
- 引用完整的语义单元，避免句子碎片化

#### Research Lead Agent
- 分析和分解用户查询
- 确定查询类型（深度优先/广度优先/直接查询）
- 制定详细研究计划
- 协调subagents执行
- 综合结果并生成最终报告

#### Research Subagent
- 执行具体研究任务
- 使用OODA循环（观察-定向-决策-行动）
- 并行工具调用提高效率
- 评估信息质量和来源可靠性
- 向lead agent报告结果

### 技术实现要点

#### 1. 工具设计
- 清晰的工具描述和用途
- 明确的输入输出格式
- 错误处理机制
- 性能优化

#### 2. 状态管理
- 分布式上下文管理
- 检查点机制
- 错误恢复策略
- 长对话支持

#### 3. 性能优化
- 并行执行
- 令牌使用优化
- 缓存机制
- 资源分配

## 当前项目分析

### 现有架构
- 基于OpenAI Agents SDK
- 游戏数据分析专业化agents
- FastAPI后端 + Next.js前端
- 简单的agent路由机制

### 优化机会
1. **引入orchestrator-worker模式**
2. **实现动态任务分解**
3. **添加并行处理能力**
4. **优化prompt设计**
5. **集成MCP工具支持**
6. **改进错误处理和状态管理**

### 目标架构
- Lead Agent: 任务分析和协调
- Specialized Subagents: 并行执行具体分析
- MCP Integration: 任务管理和可视化
- Enhanced UI: 更自然的交互体验
