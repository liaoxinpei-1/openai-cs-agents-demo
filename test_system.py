#!/usr/bin/env python3
"""
游戏数据分析系统功能测试脚本
测试后端API和分析功能的完整性
"""

import requests
import json
import time
from typing import Dict, Any

# 配置
BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"

def test_backend_health():
    """测试后端服务器健康状态"""
    try:
        # 测试聊天端点是否可访问
        response = requests.post(f"{BACKEND_URL}/chat", 
                               json={"message": ""}, 
                               timeout=5)
        print(f"✅ 后端服务器运行正常 (状态码: {response.status_code})")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ 后端服务器连接失败: {e}")
        return False

def test_chat_functionality():
    """测试聊天功能"""
    test_messages = [
        "你好，我想分析玩家行为数据",
        "显示收入分析报告",
        "生成玩家留存率图表",
        "分析游戏性能指标"
    ]
    
    conversation_id = None
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n🧪 测试消息 {i}: {message}")
        
        payload = {"message": message}
        if conversation_id:
            payload["conversation_id"] = conversation_id
            
        try:
            response = requests.post(f"{BACKEND_URL}/chat", 
                                   json=payload, 
                                   timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                conversation_id = data.get("conversation_id")
                current_agent = data.get("current_agent")
                messages = data.get("messages", [])
                
                print(f"✅ 响应成功")
                print(f"   当前代理: {current_agent}")
                print(f"   消息数量: {len(messages)}")
                
                if messages:
                    latest_message = messages[-1]["content"]
                    print(f"   最新回复: {latest_message[:100]}...")
                    
            else:
                print(f"❌ 请求失败 (状态码: {response.status_code})")
                print(f"   错误信息: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ 请求异常: {e}")
            
        time.sleep(1)  # 避免请求过快

def test_analytics_modules():
    """测试分析模块"""
    print("\n🔬 测试游戏分析模块...")
    
    try:
        # 导入并测试分析模块
        import sys
        sys.path.append('./python-backend')
        
        from game_analytics import (
            get_game_data,
            PlayerBehaviorAnalyzer,
            PerformanceAnalyzer,
            RevenueAnalyzer,
            RetentionAnalyzer,
            VisualizationGenerator
        )
        
        # 获取测试数据
        player_data, session_data = get_game_data()
        print(f"✅ 数据生成成功")
        print(f"   玩家数据: {len(player_data)} 行")
        print(f"   会话数据: {len(session_data)} 行")
        
        # 测试各个分析器
        analyzers = [
            ("玩家行为分析器", PlayerBehaviorAnalyzer, (player_data, session_data)),
            ("性能分析器", PerformanceAnalyzer, (session_data,)),
            ("收入分析器", RevenueAnalyzer, (player_data, session_data)),
            ("留存分析器", RetentionAnalyzer, (player_data, session_data)),
        ]

        for name, analyzer_class, args in analyzers:
            try:
                analyzer = analyzer_class(*args)
                print(f"✅ {name} 初始化成功")
            except Exception as e:
                print(f"❌ {name} 初始化失败: {e}")
        
        # 测试可视化生成器
        try:
            viz_gen = VisualizationGenerator()
            print(f"✅ 可视化生成器初始化成功")
        except Exception as e:
            print(f"❌ 可视化生成器初始化失败: {e}")
            
    except ImportError as e:
        print(f"❌ 模块导入失败: {e}")
    except Exception as e:
        print(f"❌ 分析模块测试失败: {e}")

def main():
    """主测试函数"""
    print("🚀 开始游戏数据分析系统测试")
    print("=" * 50)
    
    # 测试后端健康状态
    if not test_backend_health():
        print("❌ 后端服务器未运行，请先启动后端服务")
        return
    
    # 测试分析模块
    test_analytics_modules()
    
    # 测试聊天功能
    test_chat_functionality()
    
    print("\n" + "=" * 50)
    print("🎯 测试完成！")
    print(f"📊 前端界面: {FRONTEND_URL}")
    print(f"🔧 后端API: {BACKEND_URL}")

if __name__ == "__main__":
    main()
