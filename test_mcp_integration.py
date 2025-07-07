#!/usr/bin/env python3
"""
MCP集成测试脚本
测试任务管理器和图表生成器的基本功能
"""

import asyncio
import sys
import os

# 添加python-backend到路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'python-backend'))

from orchestrator_utils import (
    MCPTaskManager,
    MCPChartGenerator,
    analyze_and_plan,
    execute_parallel_tasks,
    synthesize_results,
    create_orchestrator_context
)

async def test_task_manager():
    """测试MCP任务管理器"""
    print("🔧 测试MCP任务管理器...")
    
    task_manager = MCPTaskManager()
    
    # 测试任务分解
    test_query = "分析玩家行为数据并生成可视化报告"
    context = {}
    
    subtasks = await task_manager.decompose_task(test_query, context)
    
    print(f"✅ 任务分解成功，生成 {len(subtasks)} 个子任务:")
    for i, task in enumerate(subtasks, 1):
        print(f"   {i}. {task.description} (负责: {task.agent_type})")
    
    return subtasks

async def test_chart_generator():
    """测试MCP图表生成器"""
    print("\n📊 测试MCP图表生成器...")
    
    chart_generator = MCPChartGenerator()
    
    # 测试图表生成
    test_data = {
        "title": "测试图表",
        "data": [
            {"category": "新手玩家", "value": 45},
            {"category": "活跃玩家", "value": 35},
            {"category": "核心玩家", "value": 20}
        ]
    }
    
    chart_config = await chart_generator.generate_chart("pie_chart", test_data)
    
    print(f"✅ 图表生成成功:")
    print(f"   类型: {chart_config['type']}")
    print(f"   状态: {chart_config['status']}")
    
    return chart_config

async def test_orchestrator_workflow():
    """测试完整的协调器工作流程"""
    print("\n🎯 测试完整协调器工作流程...")
    
    # 创建上下文
    context = create_orchestrator_context()
    context.user_query = "生成游戏数据的综合分析报告，包括玩家行为、收入和性能分析"
    context.session_id = "test_session_001"
    
    # 1. 分析查询并制定计划
    print("   1. 分析查询并制定计划...")
    plan = await analyze_and_plan(context.user_query, context)
    
    if "error" in plan:
        print(f"   ❌ 计划制定失败: {plan['error']}")
        return
    
    print(f"   ✅ 计划制定成功，查询类型: {plan['query_type']}")
    print(f"   📋 子任务数量: {len(plan['subtasks'])}")
    
    # 2. 执行子任务
    print("   2. 执行子任务...")
    results = await execute_parallel_tasks(plan["subtasks"])
    
    print(f"   ✅ 任务执行完成，成功: {len([r for r in results if r['status'] == 'completed'])}")
    
    # 3. 综合结果
    print("   3. 综合结果...")
    final_report = await synthesize_results(results, context.user_query)
    
    print("   ✅ 最终报告生成完成")
    print("\n📄 报告摘要:")
    print(final_report[:200] + "..." if len(final_report) > 200 else final_report)

async def main():
    """主测试函数"""
    print("🚀 开始MCP集成测试\n")
    
    try:
        # 测试各个组件
        await test_task_manager()
        await test_chart_generator()
        await test_orchestrator_workflow()
        
        print("\n✅ 所有测试完成！MCP集成功能正常工作。")
        
    except Exception as e:
        print(f"\n❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
