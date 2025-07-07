"""
Enhanced Multi-Agent Orchestrator System
增强的多智能体协调器系统

基于Anthropic多智能体研究系统架构模式设计
"""

import asyncio
import json
import logging
import time
from typing import Dict, List, Any, Optional, Tuple, Union
from pydantic import BaseModel, Field
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime, timedelta
import uuid

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =========================
# 核心数据模型
# =========================

class QueryComplexity(Enum):
    """查询复杂度分类"""
    SIMPLE = "simple"           # 单一领域，直接查询
    MODERATE = "moderate"       # 2-3个领域，需要协调
    COMPLEX = "complex"         # 多领域，深度分析
    COMPREHENSIVE = "comprehensive"  # 全面分析，需要所有领域

class ExecutionStrategy(Enum):
    """执行策略"""
    DIRECT = "direct"           # 直接转交单一Agent
    SEQUENTIAL = "sequential"   # 顺序执行
    PARALLEL = "parallel"       # 并行执行
    HYBRID = "hybrid"          # 混合执行（部分并行，部分顺序）

class TaskPriority(Enum):
    """任务优先级"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

class TaskStatus(Enum):
    """任务状态"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class SubTask:
    """增强的子任务定义"""
    id: str
    description: str
    agent_type: str
    priority: TaskPriority
    dependencies: List[str] = None
    estimated_duration: float = 30.0  # 预估执行时间（秒）
    timeout: float = 120.0  # 超时时间（秒）
    retry_count: int = 0
    max_retries: int = 2
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []
        if self.metadata is None:
            self.metadata = {}

@dataclass
class ExecutionPlan:
    """执行计划"""
    query: str
    complexity: QueryComplexity
    strategy: ExecutionStrategy
    subtasks: List[SubTask]
    expected_duration: float
    parallel_groups: List[List[str]] = None  # 并行执行组
    sequential_order: List[str] = None       # 顺序执行顺序
    
    def __post_init__(self):
        if self.parallel_groups is None:
            self.parallel_groups = []
        if self.sequential_order is None:
            self.sequential_order = []

class OrchestratorState(BaseModel):
    """协调器状态"""
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_query: str = ""
    execution_plan: Optional[Dict[str, Any]] = None
    active_tasks: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    completed_tasks: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    failed_tasks: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    total_duration: Optional[float] = None
    success_rate: float = 0.0
    
# =========================
# 智能查询分析器
# =========================

class QueryAnalyzer:
    """智能查询分析器"""
    
    # 领域关键词映射
    DOMAIN_KEYWORDS = {
        'player_behavior': ['玩家', '行为', '分群', '参与度', '活跃', '留存', 'player', 'behavior', 'engagement'],
        'performance': ['性能', '服务器', '延迟', '崩溃', '负载', 'performance', 'server', 'latency', 'crash'],
        'revenue': ['收入', '营收', '付费', '变现', '收益', 'revenue', 'monetization', 'payment'],
        'retention': ['留存', '流失', '回归', '生命周期', 'retention', 'churn', 'lifecycle'],
        'visualization': ['图表', '可视化', '仪表板', '报告', 'chart', 'visualization', 'dashboard', 'report']
    }
    
    # 复杂度指标
    COMPLEXITY_INDICATORS = {
        'simple': ['单个', '简单', '快速', '基本'],
        'moderate': ['比较', '对比', '分析', '详细'],
        'complex': ['深入', '全面', '综合', '多维度'],
        'comprehensive': ['完整', '整体', '全方位', '系统性']
    }
    
    @classmethod
    def analyze_query(cls, query: str) -> Tuple[QueryComplexity, List[str], ExecutionStrategy]:
        """分析查询，返回复杂度、涉及领域和执行策略"""
        query_lower = query.lower()
        
        # 1. 识别涉及的领域
        involved_domains = []
        for domain, keywords in cls.DOMAIN_KEYWORDS.items():
            if any(keyword in query_lower for keyword in keywords):
                involved_domains.append(domain)
        
        # 如果没有明确领域，默认为综合分析
        if not involved_domains:
            involved_domains = ['player_behavior', 'performance', 'revenue', 'retention']
        
        # 2. 判断复杂度
        complexity = cls._determine_complexity(query_lower, len(involved_domains))
        
        # 3. 确定执行策略
        strategy = cls._determine_strategy(complexity, involved_domains)
        
        return complexity, involved_domains, strategy
    
    @classmethod
    def _determine_complexity(cls, query: str, domain_count: int) -> QueryComplexity:
        """确定查询复杂度"""
        # 基于关键词判断
        for complexity, indicators in cls.COMPLEXITY_INDICATORS.items():
            if any(indicator in query for indicator in indicators):
                return QueryComplexity(complexity)
        
        # 基于涉及领域数量判断
        if domain_count == 1:
            return QueryComplexity.SIMPLE
        elif domain_count <= 2:
            return QueryComplexity.MODERATE
        elif domain_count <= 3:
            return QueryComplexity.COMPLEX
        else:
            return QueryComplexity.COMPREHENSIVE
    
    @classmethod
    def _determine_strategy(cls, complexity: QueryComplexity, domains: List[str]) -> ExecutionStrategy:
        """确定执行策略"""
        if complexity == QueryComplexity.SIMPLE and len(domains) == 1:
            return ExecutionStrategy.DIRECT
        elif complexity in [QueryComplexity.MODERATE, QueryComplexity.COMPLEX]:
            return ExecutionStrategy.PARALLEL
        else:
            return ExecutionStrategy.HYBRID

# =========================
# 任务分解引擎
# =========================

class TaskDecomposer:
    """智能任务分解引擎"""
    
    @classmethod
    def decompose_query(cls, query: str, complexity: QueryComplexity, 
                       domains: List[str], strategy: ExecutionStrategy) -> List[SubTask]:
        """将查询分解为子任务"""
        subtasks = []
        
        # 根据复杂度和策略生成任务
        if strategy == ExecutionStrategy.DIRECT:
            subtasks = cls._create_direct_tasks(query, domains[0])
        elif strategy == ExecutionStrategy.PARALLEL:
            subtasks = cls._create_parallel_tasks(query, domains)
        elif strategy == ExecutionStrategy.HYBRID:
            subtasks = cls._create_hybrid_tasks(query, domains)
        else:  # SEQUENTIAL
            subtasks = cls._create_sequential_tasks(query, domains)
        
        # 添加可视化任务（如果需要）
        if len(subtasks) > 1 or complexity != QueryComplexity.SIMPLE:
            viz_task = SubTask(
                id=f"viz_{uuid.uuid4().hex[:8]}",
                description=f"为查询'{query}'生成综合可视化报告",
                agent_type="visualization",
                priority=TaskPriority.MEDIUM,
                dependencies=[task.id for task in subtasks],
                estimated_duration=20.0
            )
            subtasks.append(viz_task)
        
        return subtasks
    
    @classmethod
    def _create_direct_tasks(cls, query: str, domain: str) -> List[SubTask]:
        """创建直接执行任务"""
        task_id = f"{domain}_{uuid.uuid4().hex[:8]}"
        return [SubTask(
            id=task_id,
            description=f"执行{domain}分析: {query}",
            agent_type=domain,
            priority=TaskPriority.HIGH,
            estimated_duration=45.0
        )]
    
    @classmethod
    def _create_parallel_tasks(cls, query: str, domains: List[str]) -> List[SubTask]:
        """创建并行执行任务"""
        tasks = []
        for domain in domains:
            task_id = f"{domain}_{uuid.uuid4().hex[:8]}"
            tasks.append(SubTask(
                id=task_id,
                description=f"并行执行{domain}分析: {query}",
                agent_type=domain,
                priority=TaskPriority.HIGH,
                estimated_duration=30.0
            ))
        return tasks
    
    @classmethod
    def _create_hybrid_tasks(cls, query: str, domains: List[str]) -> List[SubTask]:
        """创建混合执行任务"""
        tasks = []
        
        # 第一阶段：基础数据收集（并行）
        base_tasks = []
        for domain in domains[:3]:  # 前3个领域并行
            task_id = f"{domain}_base_{uuid.uuid4().hex[:8]}"
            task = SubTask(
                id=task_id,
                description=f"基础{domain}数据收集: {query}",
                agent_type=domain,
                priority=TaskPriority.HIGH,
                estimated_duration=25.0
            )
            base_tasks.append(task)
            tasks.append(task)
        
        # 第二阶段：深度分析（依赖第一阶段）
        if len(domains) > 3:
            for domain in domains[3:]:
                task_id = f"{domain}_deep_{uuid.uuid4().hex[:8]}"
                task = SubTask(
                    id=task_id,
                    description=f"深度{domain}分析: {query}",
                    agent_type=domain,
                    priority=TaskPriority.MEDIUM,
                    dependencies=[t.id for t in base_tasks],
                    estimated_duration=40.0
                )
                tasks.append(task)
        
        return tasks
    
    @classmethod
    def _create_sequential_tasks(cls, query: str, domains: List[str]) -> List[SubTask]:
        """创建顺序执行任务"""
        tasks = []
        prev_task_id = None
        
        for i, domain in enumerate(domains):
            task_id = f"{domain}_seq_{uuid.uuid4().hex[:8]}"
            dependencies = [prev_task_id] if prev_task_id else []
            
            task = SubTask(
                id=task_id,
                description=f"顺序执行{domain}分析: {query}",
                agent_type=domain,
                priority=TaskPriority.HIGH,
                dependencies=dependencies,
                estimated_duration=35.0
            )
            tasks.append(task)
            prev_task_id = task_id
        
        return tasks

# =========================
# 并行执行引擎
# =========================

class ParallelExecutionEngine:
    """高效的并行任务执行引擎"""

    def __init__(self, max_concurrent_tasks: int = 5):
        self.max_concurrent_tasks = max_concurrent_tasks
        self.running_tasks: Dict[str, asyncio.Task] = {}
        self.task_results: Dict[str, Dict[str, Any]] = {}
        self.task_errors: Dict[str, str] = {}

    async def execute_plan(self, plan: ExecutionPlan, agent_mapping: Dict[str, Any]) -> Dict[str, Any]:
        """执行完整的执行计划"""
        logger.info(f"开始执行计划: {plan.strategy.value} 策略，{len(plan.subtasks)} 个任务")

        start_time = datetime.now()

        try:
            if plan.strategy == ExecutionStrategy.DIRECT:
                results = await self._execute_direct(plan.subtasks, agent_mapping)
            elif plan.strategy == ExecutionStrategy.PARALLEL:
                results = await self._execute_parallel(plan.subtasks, agent_mapping)
            elif plan.strategy == ExecutionStrategy.SEQUENTIAL:
                results = await self._execute_sequential(plan.subtasks, agent_mapping)
            else:  # HYBRID
                results = await self._execute_hybrid(plan, agent_mapping)

            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            return {
                'status': 'completed',
                'results': results,
                'duration': duration,
                'success_rate': self._calculate_success_rate(results),
                'execution_summary': self._generate_execution_summary(results, duration)
            }

        except Exception as e:
            logger.error(f"执行计划失败: {e}")
            return {
                'status': 'failed',
                'error': str(e),
                'partial_results': self.task_results
            }

    async def _execute_direct(self, tasks: List[SubTask], agent_mapping: Dict[str, Any]) -> List[Dict[str, Any]]:
        """直接执行单个任务"""
        if not tasks:
            return []

        task = tasks[0]
        result = await self._execute_single_task(task, agent_mapping)
        return [result]

    async def _execute_parallel(self, tasks: List[SubTask], agent_mapping: Dict[str, Any]) -> List[Dict[str, Any]]:
        """并行执行所有任务"""
        # 按依赖关系分组
        dependency_groups = self._group_by_dependencies(tasks)
        all_results = []

        for group in dependency_groups:
            # 并行执行当前组的任务
            group_tasks = [self._execute_single_task(task, agent_mapping) for task in group]
            group_results = await asyncio.gather(*group_tasks, return_exceptions=True)

            # 处理结果和异常
            processed_results = []
            for i, result in enumerate(group_results):
                if isinstance(result, Exception):
                    processed_results.append({
                        'task_id': group[i].id,
                        'status': 'failed',
                        'error': str(result)
                    })
                else:
                    processed_results.append(result)

            all_results.extend(processed_results)

        return all_results

    async def _execute_sequential(self, tasks: List[SubTask], agent_mapping: Dict[str, Any]) -> List[Dict[str, Any]]:
        """顺序执行任务"""
        results = []

        for task in tasks:
            # 检查依赖是否满足
            if not self._check_dependencies(task, results):
                results.append({
                    'task_id': task.id,
                    'status': 'failed',
                    'error': '依赖任务未完成'
                })
                continue

            result = await self._execute_single_task(task, agent_mapping)
            results.append(result)

            # 如果任务失败且是关键任务，停止执行
            if result['status'] == 'failed' and task.priority == TaskPriority.CRITICAL:
                logger.error(f"关键任务失败，停止执行: {task.id}")
                break

        return results

    async def _execute_hybrid(self, plan: ExecutionPlan, agent_mapping: Dict[str, Any]) -> List[Dict[str, Any]]:
        """混合执行策略"""
        all_results = []

        # 执行并行组
        for parallel_group in plan.parallel_groups:
            group_tasks = [task for task in plan.subtasks if task.id in parallel_group]
            group_results = await self._execute_parallel(group_tasks, agent_mapping)
            all_results.extend(group_results)

        # 执行顺序任务
        sequential_tasks = [task for task in plan.subtasks if task.id in plan.sequential_order]
        if sequential_tasks:
            sequential_results = await self._execute_sequential(sequential_tasks, agent_mapping)
            all_results.extend(sequential_results)

        return all_results

    async def _execute_single_task(self, task: SubTask, agent_mapping: Dict[str, Any]) -> Dict[str, Any]:
        """执行单个任务"""
        task.start_time = datetime.now()
        task.status = TaskStatus.RUNNING

        try:
            # 获取对应的Agent
            agent = agent_mapping.get(task.agent_type)
            if not agent:
                raise ValueError(f"未找到Agent类型: {task.agent_type}")

            # 创建任务上下文
            from main import GameAnalyticsContext
            context = GameAnalyticsContext(
                game_id=task.metadata.get('game_id', 'demo_game') if task.metadata else 'demo_game',
                analysis_type=task.agent_type,
                time_range={"start": "2024-01-01", "end": "2024-12-31"},
                metrics=[task.agent_type]
            )

            # 执行任务（带超时）
            result = await asyncio.wait_for(
                self._call_agent_tool(agent, task, context),
                timeout=task.timeout
            )

            task.end_time = datetime.now()
            task.status = TaskStatus.COMPLETED
            task.result = result

            return {
                'task_id': task.id,
                'description': task.description,
                'agent_type': task.agent_type,
                'status': 'completed',
                'result': result,
                'duration': (task.end_time - task.start_time).total_seconds(),
                'priority': task.priority.value
            }

        except asyncio.TimeoutError:
            task.status = TaskStatus.FAILED
            task.error = f"任务超时 ({task.timeout}秒)"
            logger.error(f"任务超时: {task.id}")

            return {
                'task_id': task.id,
                'description': task.description,
                'agent_type': task.agent_type,
                'status': 'timeout',
                'error': task.error,
                'duration': task.timeout
            }

        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            logger.error(f"任务执行失败 {task.id}: {e}")

            # 重试机制
            if task.retry_count < task.max_retries:
                task.retry_count += 1
                logger.info(f"重试任务 {task.id} (第{task.retry_count}次)")
                await asyncio.sleep(2 ** task.retry_count)  # 指数退避
                return await self._execute_single_task(task, agent_mapping)

            return {
                'task_id': task.id,
                'description': task.description,
                'agent_type': task.agent_type,
                'status': 'failed',
                'error': task.error,
                'retry_count': task.retry_count
            }

    async def _call_agent_tool(self, agent: Any, task: SubTask, context: Any) -> Dict[str, Any]:
        """调用Agent工具"""
        if not agent.tools:
            raise ValueError(f"Agent {task.agent_type} 没有可用工具")

        tool = agent.tools[0]  # 使用第一个工具

        if task.agent_type == "visualization":
            return await tool(
                context=context,
                chart_type=task.metadata.get("chart_type", "line") if task.metadata else "line",
                data_description=task.description,
                title=task.metadata.get("title", "") if task.metadata else ""
            )
        else:
            return await tool(
                context=context,
                query=task.description
            )

    def _group_by_dependencies(self, tasks: List[SubTask]) -> List[List[SubTask]]:
        """按依赖关系分组任务"""
        groups = []
        remaining_tasks = tasks.copy()
        completed_task_ids = set()

        while remaining_tasks:
            current_group = []

            # 找到没有未完成依赖的任务
            for task in remaining_tasks[:]:
                if all(dep_id in completed_task_ids for dep_id in task.dependencies):
                    current_group.append(task)
                    remaining_tasks.remove(task)

            if not current_group:
                # 如果没有可执行的任务，说明存在循环依赖
                logger.warning("检测到循环依赖，强制执行剩余任务")
                current_group = remaining_tasks
                remaining_tasks = []

            groups.append(current_group)
            completed_task_ids.update(task.id for task in current_group)

        return groups

    def _check_dependencies(self, task: SubTask, completed_results: List[Dict[str, Any]]) -> bool:
        """检查任务依赖是否满足"""
        completed_task_ids = {result['task_id'] for result in completed_results
                            if result['status'] == 'completed'}
        return all(dep_id in completed_task_ids for dep_id in task.dependencies)

    def _calculate_success_rate(self, results: List[Dict[str, Any]]) -> float:
        """计算成功率"""
        if not results:
            return 0.0

        successful = len([r for r in results if r['status'] == 'completed'])
        return (successful / len(results)) * 100

    def _generate_execution_summary(self, results: List[Dict[str, Any]], duration: float) -> Dict[str, Any]:
        """生成执行摘要"""
        total_tasks = len(results)
        successful_tasks = len([r for r in results if r['status'] == 'completed'])
        failed_tasks = len([r for r in results if r['status'] == 'failed'])
        timeout_tasks = len([r for r in results if r['status'] == 'timeout'])

        return {
            'total_tasks': total_tasks,
            'successful_tasks': successful_tasks,
            'failed_tasks': failed_tasks,
            'timeout_tasks': timeout_tasks,
            'success_rate': (successful_tasks / total_tasks) * 100 if total_tasks > 0 else 0,
            'total_duration': duration,
            'avg_task_duration': duration / total_tasks if total_tasks > 0 else 0
        }

# =========================
# 增强协调器
# =========================

class EnhancedOrchestrator:
    """增强的多智能体协调器"""

    def __init__(self, agent_mapping: Dict[str, Any]):
        self.agent_mapping = agent_mapping
        self.query_analyzer = QueryAnalyzer()
        self.task_decomposer = TaskDecomposer()
        self.execution_engine = ParallelExecutionEngine()
        self.state = OrchestratorState()

    async def orchestrate(self, user_query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """协调执行用户查询"""
        self.state.user_query = user_query
        self.state.start_time = datetime.now()

        try:
            # 1. 分析查询
            complexity, domains, strategy = self.query_analyzer.analyze_query(user_query)
            logger.info(f"查询分析: 复杂度={complexity.value}, 领域={domains}, 策略={strategy.value}")

            # 2. 分解任务
            subtasks = self.task_decomposer.decompose_query(user_query, complexity, domains, strategy)
            logger.info(f"任务分解: 生成{len(subtasks)}个子任务")

            # 3. 创建执行计划
            execution_plan = ExecutionPlan(
                query=user_query,
                complexity=complexity,
                strategy=strategy,
                subtasks=subtasks,
                expected_duration=sum(task.estimated_duration for task in subtasks)
            )

            # 4. 执行计划
            execution_result = await self.execution_engine.execute_plan(execution_plan, self.agent_mapping)

            # 5. 综合结果
            final_report = await self._synthesize_results(
                execution_result['results'],
                user_query,
                execution_result.get('execution_summary', {})
            )

            self.state.end_time = datetime.now()
            self.state.total_duration = (self.state.end_time - self.state.start_time).total_seconds()
            self.state.success_rate = execution_result.get('success_rate', 0)

            return {
                'status': 'success',
                'query': user_query,
                'complexity': complexity.value,
                'strategy': strategy.value,
                'execution_summary': execution_result.get('execution_summary', {}),
                'final_report': final_report,
                'session_info': {
                    'session_id': self.state.session_id,
                    'total_duration': self.state.total_duration,
                    'success_rate': self.state.success_rate
                }
            }

        except Exception as e:
            logger.error(f"协调执行失败: {e}")
            return {
                'status': 'error',
                'query': user_query,
                'error': str(e),
                'session_id': self.state.session_id
            }

    async def _synthesize_results(self, results: List[Dict[str, Any]],
                                user_query: str, execution_summary: Dict[str, Any]) -> str:
        """综合分析结果并生成最终报告"""
        try:
            # 按智能体类型组织结果
            by_agent = {}
            for result in results:
                if result['status'] == 'completed':
                    agent_type = result['agent_type']
                    if agent_type not in by_agent:
                        by_agent[agent_type] = []
                    by_agent[agent_type].append(result)

            # 生成综合报告
            report = f"""# 📊 游戏数据分析报告

## 🎯 查询内容
**{user_query}**

## 📈 执行概况
- **总任务数**: {execution_summary.get('total_tasks', 0)}
- **成功完成**: {execution_summary.get('successful_tasks', 0)}
- **执行时长**: {execution_summary.get('total_duration', 0):.2f}秒
- **成功率**: {execution_summary.get('success_rate', 0):.1f}%

## 🔍 分析结果
"""

            # 添加各智能体的分析结果
            agent_names = {
                'player_behavior': '🎮 玩家行为分析',
                'performance': '⚡ 性能分析',
                'revenue': '💰 收入分析',
                'retention': '🔄 留存分析',
                'visualization': '📊 数据可视化'
            }

            for agent_type, agent_results in by_agent.items():
                agent_name = agent_names.get(agent_type, f'🤖 {agent_type.title()}')
                report += f"\n### {agent_name}\n"

                for result in agent_results:
                    if isinstance(result['result'], dict):
                        # 格式化结构化结果
                        report += self._format_structured_result(result['result'])
                    else:
                        # 直接显示文本结果
                        report += f"- {result['result']}\n"

            # 添加总结和建议
            report += f"\n## 💡 总结与建议\n"
            report += self._generate_insights(by_agent, user_query)

            return report.strip()

        except Exception as e:
            logger.error(f"结果综合失败: {e}")
            return f"❌ 结果综合出现错误: {str(e)}"

    def _format_structured_result(self, result: Dict[str, Any]) -> str:
        """格式化结构化结果"""
        formatted = ""
        for key, value in result.items():
            if isinstance(value, dict):
                formatted += f"- **{key}**: {json.dumps(value, ensure_ascii=False, indent=2)}\n"
            elif isinstance(value, list):
                formatted += f"- **{key}**: {', '.join(map(str, value))}\n"
            else:
                formatted += f"- **{key}**: {value}\n"
        return formatted

    def _generate_insights(self, results_by_agent: Dict[str, List[Dict[str, Any]]], query: str) -> str:
        """生成洞察和建议"""
        insights = []

        # 基于结果生成通用洞察
        if 'player_behavior' in results_by_agent:
            insights.append("🎯 建议关注玩家分群特征，针对不同类型玩家制定个性化策略")

        if 'performance' in results_by_agent:
            insights.append("⚡ 持续监控性能指标，及时发现和解决性能瓶颈")

        if 'revenue' in results_by_agent:
            insights.append("💰 优化变现策略，提高付费转化率和用户价值")

        if 'retention' in results_by_agent:
            insights.append("🔄 重点关注新用户留存，建立有效的用户生命周期管理")

        if len(results_by_agent) > 2:
            insights.append("📊 建议建立综合数据仪表板，实现多维度数据监控")

        return "\n".join(f"- {insight}" for insight in insights)
