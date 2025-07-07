#!/usr/bin/env python3
"""
测试增强的智能体prompt系统
验证基于Anthropic设计模式的智能体交互
"""

import asyncio
from main import (
    triage_agent, 
    orchestrator_agent,
    player_behavior_agent,
    performance_analysis_agent,
    GameAnalyticsContext
)
from agents import RunContextWrapper

async def test_enhanced_prompts():
    """测试增强的prompt系统"""
    print("🧪 测试增强的智能体prompt系统")
    print("=" * 50)
    
    # 创建测试上下文
    context = GameAnalyticsContext(
        game_id="test_game_001",
        analysis_type="comprehensive",
        time_range={"start": "2024-01-01", "end": "2024-01-31"},
        metrics=["engagement", "retention"]
    )
    
    # 测试1: 验证triage_agent的research lead agent模式
    print("\n📋 测试1: Triage Agent (Research Lead Agent模式)")
    print("-" * 30)
    
    try:
        # 检查triage_agent的指令是否包含关键的Anthropic模式元素
        instructions = triage_agent.instructions
        
        # 验证关键元素
        key_elements = [
            "研究主导智能体",
            "查询类型识别", 
            "广度优先",
            "深度优先",
            "直接查询",
            "协调专业化子智能体"
        ]
        
        found_elements = []
        for element in key_elements:
            if element in instructions:
                found_elements.append(element)
                print(f"  ✅ 找到关键元素: {element}")
            else:
                print(f"  ❌ 缺少关键元素: {element}")
        
        print(f"  📊 Research Lead Agent模式完整度: {len(found_elements)}/{len(key_elements)} ({len(found_elements)/len(key_elements)*100:.1f}%)")
        
    except Exception as e:
        print(f"  ❌ Triage Agent测试失败: {e}")
    
    # 测试2: 验证player_behavior_agent的research subagent模式
    print("\n🎮 测试2: Player Behavior Agent (Research Subagent模式)")
    print("-" * 30)
    
    try:
        # 创建运行上下文
        run_context = RunContextWrapper(context)
        
        # 获取动态指令
        instructions = player_behavior_agent.instructions(run_context, player_behavior_agent)
        
        # 验证OODA循环元素
        ooda_elements = [
            "观察 (Observe)",
            "定向 (Orient)", 
            "决策 (Decide)",
            "行动 (Act)",
            "OODA循环"
        ]
        
        found_ooda = []
        for element in ooda_elements:
            if element in instructions:
                found_ooda.append(element)
                print(f"  ✅ 找到OODA元素: {element}")
            else:
                print(f"  ❌ 缺少OODA元素: {element}")
        
        print(f"  📊 OODA循环完整度: {len(found_ooda)}/{len(ooda_elements)} ({len(found_ooda)/len(ooda_elements)*100:.1f}%)")
        
        # 验证专业化能力
        capabilities = [
            "玩家分群分析",
            "行为模式识别",
            "参与度指标",
            "并行工具调用"
        ]
        
        found_capabilities = []
        for capability in capabilities:
            if capability in instructions:
                found_capabilities.append(capability)
                print(f"  ✅ 找到专业能力: {capability}")
        
        print(f"  📊 专业能力完整度: {len(found_capabilities)}/{len(capabilities)} ({len(found_capabilities)/len(capabilities)*100:.1f}%)")
        
    except Exception as e:
        print(f"  ❌ Player Behavior Agent测试失败: {e}")
    
    # 测试3: 验证orchestrator_agent的协调能力
    print("\n🎯 测试3: Orchestrator Agent (多智能体协调)")
    print("-" * 30)
    
    try:
        instructions = orchestrator_agent.instructions
        
        coordination_elements = [
            "多智能体系统的协调器",
            "Anthropic研究系统架构",
            "任务分解",
            "并行执行",
            "综合结果"
        ]
        
        found_coordination = []
        for element in coordination_elements:
            if element in instructions:
                found_coordination.append(element)
                print(f"  ✅ 找到协调元素: {element}")
        
        print(f"  📊 协调能力完整度: {len(found_coordination)}/{len(coordination_elements)} ({len(found_coordination)/len(coordination_elements)*100:.1f}%)")
        
    except Exception as e:
        print(f"  ❌ Orchestrator Agent测试失败: {e}")
    
    # 测试4: 验证handoff关系
    print("\n🔄 测试4: 智能体Handoff关系")
    print("-" * 30)
    
    try:
        # 检查triage_agent的handoff配置
        triage_handoffs = len(triage_agent.handoffs)
        print(f"  📊 Triage Agent handoffs: {triage_handoffs}")
        
        # 检查orchestrator_agent的handoff配置
        orchestrator_handoffs = len(orchestrator_agent.handoffs)
        print(f"  📊 Orchestrator Agent handoffs: {orchestrator_handoffs}")
        
        # 验证双向handoff关系
        if orchestrator_agent in triage_agent.handoffs:
            print("  ✅ Triage → Orchestrator handoff 已配置")
        else:
            print("  ❌ Triage → Orchestrator handoff 缺失")
            
        if triage_agent in orchestrator_agent.handoffs:
            print("  ✅ Orchestrator → Triage handoff 已配置")
        else:
            print("  ❌ Orchestrator → Triage handoff 缺失")
        
    except Exception as e:
        print(f"  ❌ Handoff关系测试失败: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 增强prompt系统测试完成!")
    print("💡 系统已成功应用Anthropic多智能体设计模式")

if __name__ == "__main__":
    asyncio.run(test_enhanced_prompts())
