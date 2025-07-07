"""
Multi-Agent Orchestrator Utilities
多智能体协调器工具函数

提供任务分解、MCP集成等功能 - 增强版本
"""

import asyncio
import json
import logging
from typing import Dict, List, Any, Optional
from pydantic import BaseModel
from datetime import datetime

# 导入增强的协调器组件
from enhanced_orchestrator import (
    EnhancedOrchestrator,
    QueryAnalyzer,
    TaskDecomposer,
    ParallelExecutionEngine,
    OrchestratorState
)

# 导入真实的MCP集成
from mcp_integration import mcp_manager

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =========================
# 增强的协调器工具函数
# =========================

# 全局协调器实例
_orchestrator_instance: Optional[EnhancedOrchestrator] = None

async def initialize_orchestrator(agent_mapping: Dict[str, Any]) -> bool:
    """初始化增强协调器"""
    global _orchestrator_instance

    try:
        # 初始化MCP管理器
        mcp_initialized = await mcp_manager.initialize()
        if not mcp_initialized:
            logger.warning("MCP管理器初始化失败，将使用模拟模式")

        # 创建协调器实例
        _orchestrator_instance = EnhancedOrchestrator(agent_mapping)
        logger.info("增强协调器初始化成功")
        return True

    except Exception as e:
        logger.error(f"协调器初始化失败: {e}")
        return False

async def shutdown_orchestrator():
    """关闭协调器"""
    global _orchestrator_instance

    if mcp_manager.is_initialized:
        await mcp_manager.shutdown()

    _orchestrator_instance = None
    logger.info("协调器已关闭")

def get_orchestrator() -> Optional[EnhancedOrchestrator]:
    """获取协调器实例"""
    return _orchestrator_instance

# =========================
# 兼容性接口函数
# =========================

async def analyze_and_plan(query: str, context: OrchestratorState) -> Dict[str, Any]:
    """分析查询并制定计划 - 增强版本"""
    try:
        orchestrator = get_orchestrator()
        if not orchestrator:
            logger.error("协调器未初始化")
            return {"error": "协调器未初始化"}

        # 使用增强协调器分析查询
        complexity, domains, strategy = orchestrator.query_analyzer.analyze_query(query)

        # 分解任务
        subtasks = orchestrator.task_decomposer.decompose_query(query, complexity, domains, strategy)

        return {
            "query_type": complexity.value,
            "strategy": strategy.value,
            "domains": domains,
            "subtasks": [
                {
                    "id": task.id,
                    "description": task.description,
                    "agent_type": task.agent_type,
                    "priority": task.priority.value,
                    "dependencies": task.dependencies,
                    "estimated_duration": task.estimated_duration
                }
                for task in subtasks
            ],
            "expected_agents": len(set(task.agent_type for task in subtasks)),
            "parallel_execution": strategy.value in ["parallel", "hybrid"]
        }

    except Exception as e:
        logger.error(f"分析查询出现错误: {e}")
        return {"error": str(e)}
async def execute_parallel_tasks(subtasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """并行执行任务 - 增强版本"""
    try:
        orchestrator = get_orchestrator()
        if not orchestrator:
            logger.error("协调器未初始化")
            return []

        # 转换为SubTask对象
        from enhanced_orchestrator import SubTask, TaskPriority, TaskStatus
        task_objects = []
        for task_dict in subtasks:
            task = SubTask(
                id=task_dict["id"],
                description=task_dict["description"],
                agent_type=task_dict["agent_type"],
                priority=TaskPriority(task_dict.get("priority", 2)),
                dependencies=task_dict.get("dependencies", []),
                estimated_duration=task_dict.get("estimated_duration", 30.0)
            )
            task_objects.append(task)

        # 使用并行执行引擎
        results = await orchestrator.execution_engine._execute_parallel(
            task_objects,
            orchestrator.agent_mapping
        )

        return results

    except Exception as e:
        logger.error(f"并行执行失败: {e}")
        return []

async def synthesize_results(results: List[Dict[str, Any]], user_query: str) -> str:
    """综合分析结果并生成最终报告 - 增强版本"""
    try:
        orchestrator = get_orchestrator()
        if not orchestrator:
            logger.error("协调器未初始化")
            return "❌ 协调器未初始化，无法生成报告"

        # 使用增强协调器的结果综合功能
        execution_summary = {
            'total_tasks': len(results),
            'successful_tasks': len([r for r in results if r.get('status') == 'completed']),
            'total_duration': sum(r.get('duration', 0) for r in results),
            'success_rate': (len([r for r in results if r.get('status') == 'completed']) / len(results)) * 100 if results else 0
        }

        final_report = await orchestrator._synthesize_results(results, user_query, execution_summary)
        return final_report

    except Exception as e:
        logger.error(f"结果综合失败: {e}")
        return f"❌ 结果综合出现错误: {str(e)}"

# =========================
# 兼容性工具函数
# =========================

def create_orchestrator_context() -> OrchestratorState:
    """创建协调器上下文"""
    return OrchestratorState()

# 为了向后兼容，保留旧的接口名称
task_manager = mcp_manager.task_manager if hasattr(mcp_manager, 'task_manager') else None
chart_generator = mcp_manager.chart_generator if hasattr(mcp_manager, 'chart_generator') else None
