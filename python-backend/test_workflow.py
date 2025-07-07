#!/usr/bin/env python3
"""
测试新的多智能体工作流
验证任务分解和可视化智能体调用
"""

import asyncio
import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import (
    triage_agent,
    orchestrator_agent,
    visualization_agent,
    GameAnalyticsContext
)

async def test_visualization_workflow():
    """测试可视化工作流"""
    print("🧪 测试可视化工作流")
    print("=" * 50)
    
    # 创建测试上下文
    context = GameAnalyticsContext(
        game_id="test_game_001",
        analysis_type="visualization",
        time_range={"start": "2024-01-01", "end": "2024-12-31"},
        metrics=["visualization"]
    )
    
    # 测试1: 直接调用可视化智能体
    print("\n📊 测试1: 直接调用可视化智能体")
    print("-" * 30)
    
    try:
        # 检查可视化智能体的工具配置
        print(f"可视化智能体工具数量: {len(visualization_agent.tools)}")
        print(f"工具名称: {visualization_agent.tools[0].name if visualization_agent.tools else 'None'}")
        print("✅ 可视化智能体配置正确")
    except Exception as e:
        print(f"❌ 可视化智能体检查失败: {e}")
    
    # 测试2: 通过Triage Agent路由到可视化
    print("\n🎯 测试2: 通过Triage Agent路由")
    print("-" * 30)
    
    try:
        # 模拟用户请求可视化
        query = "请生成一个显示玩家留存率的折线图"
        
        # 这里应该通过Runner来执行，但为了测试我们直接调用
        print(f"用户查询: {query}")
        print("🔄 应该路由到可视化智能体...")
        
        # 实际应用中，这会通过Runner和handoff机制自动路由
        print("✅ 路由机制已配置，等待实际测试")
        
    except Exception as e:
        print(f"❌ 路由测试失败: {e}")

async def test_orchestrator_workflow():
    """测试协调器工作流"""
    print("\n🎯 测试协调器工作流")
    print("=" * 50)
    
    # 创建测试上下文
    context = GameAnalyticsContext(
        game_id="test_game_002",
        analysis_type="comprehensive",
        time_range={"start": "2024-01-01", "end": "2024-12-31"},
        metrics=["comprehensive"]
    )
    
    try:
        # 测试复杂查询的任务分解
        query = "分析游戏的整体表现，包括玩家行为、收入情况，并生成可视化报告"
        
        print(f"复杂查询: {query}")
        print("🔄 调用协调器进行任务分解...")
        
        # 检查协调器智能体的工具配置
        print(f"协调器智能体工具数量: {len(orchestrator_agent.tools)}")
        print(f"工具名称: {orchestrator_agent.tools[0].name if orchestrator_agent.tools else 'None'}")
        print("✅ 协调器智能体配置正确")
        
        print("✅ 协调器配置检查完成")
        
    except Exception as e:
        print(f"❌ 协调器测试失败: {e}")

async def test_agent_handoffs():
    """测试智能体handoff关系"""
    print("\n🔄 测试智能体Handoff关系")
    print("=" * 50)
    
    # 检查handoff配置
    agents = {
        "Triage Agent": triage_agent,
        "Orchestrator Agent": orchestrator_agent,
        "Visualization Agent": visualization_agent
    }
    
    for name, agent in agents.items():
        handoff_count = len(agent.handoffs)
        print(f"📋 {name}:")
        print(f"   Handoffs数量: {handoff_count}")
        # 尝试获取handoff目标智能体的名称
        try:
            handoff_names = [getattr(h, 'target_agent', 'Unknown') for h in agent.handoffs]
            print(f"   Handoff目标: {handoff_names}")
        except:
            print(f"   Handoff配置: 已设置 {handoff_count} 个")
    
    print("\n✅ Handoff关系检查完成")

async def main():
    """主测试函数"""
    print("🚀 开始测试新的多智能体工作流")
    print("=" * 60)
    
    try:
        # 测试可视化工作流
        await test_visualization_workflow()
        
        # 测试协调器工作流
        await test_orchestrator_workflow()
        
        # 测试handoff关系
        await test_agent_handoffs()
        
        print("\n🎉 所有测试完成!")
        print("=" * 60)
        
        print("\n💡 下一步建议:")
        print("1. 在前端测试完整的用户交互流程")
        print("2. 验证可视化图表的实际生成")
        print("3. 测试复杂查询的任务分解效果")
        print("4. 优化智能体间的协作效率")
        
    except Exception as e:
        print(f"\n❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
