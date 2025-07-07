"""
游戏数据分析核心功能模块
提供游戏数据生成、分析和可视化功能
"""

import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import json

class GameDataGenerator:
    """游戏数据生成器 - 用于模拟真实游戏数据"""
    
    @staticmethod
    def generate_player_data(player_count: int = 1000) -> pd.DataFrame:
        """生成玩家基础数据"""
        players = []
        for i in range(player_count):
            player = {
                'player_id': f'player_{i:06d}',
                'registration_date': datetime.now() - timedelta(days=random.randint(1, 365)),
                'level': random.randint(1, 100),
                'total_playtime': random.randint(10, 10000),  # 分钟
                'total_spent': round(random.uniform(0, 500), 2),
                'last_login': datetime.now() - timedelta(days=random.randint(0, 30)),
                'device_type': random.choice(['iOS', 'Android', 'PC', 'Console']),
                'country': random.choice(['CN', 'US', 'JP', 'KR', 'DE', 'FR', 'GB']),
                'player_type': random.choice(['casual', 'core', 'whale', 'new'])
            }
            players.append(player)
        return pd.DataFrame(players)
    
    @staticmethod
    def generate_session_data(player_count: int = 1000, days: int = 30) -> pd.DataFrame:
        """生成游戏会话数据"""
        sessions = []
        for day in range(days):
            date = datetime.now() - timedelta(days=day)
            daily_sessions = random.randint(100, 500)
            
            for _ in range(daily_sessions):
                session = {
                    'session_id': f'session_{len(sessions):08d}',
                    'player_id': f'player_{random.randint(0, player_count-1):06d}',
                    'start_time': date + timedelta(hours=random.randint(0, 23), 
                                                 minutes=random.randint(0, 59)),
                    'duration': random.randint(1, 180),  # 分钟
                    'levels_completed': random.randint(0, 10),
                    'items_purchased': random.randint(0, 5),
                    'revenue': round(random.uniform(0, 50), 2),
                    'crashes': random.randint(0, 2)
                }
                sessions.append(session)
        return pd.DataFrame(sessions)

class PlayerBehaviorAnalyzer:
    """玩家行为分析器"""
    
    def __init__(self, player_data: pd.DataFrame, session_data: pd.DataFrame):
        self.player_data = player_data
        self.session_data = session_data
    
    def analyze_player_segments(self) -> Dict[str, Any]:
        """分析玩家分群"""
        segments = self.player_data['player_type'].value_counts()
        
        analysis = {
            'total_players': len(self.player_data),
            'segments': {
                'casual': int(segments.get('casual', 0)),
                'core': int(segments.get('core', 0)),
                'whale': int(segments.get('whale', 0)),
                'new': int(segments.get('new', 0))
            },
            'avg_level': float(self.player_data['level'].mean()),
            'avg_playtime': float(self.player_data['total_playtime'].mean()),
            'avg_spent': float(self.player_data['total_spent'].mean())
        }
        return analysis
    
    def analyze_engagement(self) -> Dict[str, Any]:
        """分析玩家参与度"""
        # 计算日活跃用户
        recent_sessions = self.session_data[
            self.session_data['start_time'] >= datetime.now() - timedelta(days=7)
        ]
        daily_active = recent_sessions.groupby(
            recent_sessions['start_time'].dt.date
        )['player_id'].nunique()
        
        return {
            'daily_active_users': {
                str(date): int(count) for date, count in daily_active.items()
            },
            'avg_session_duration': float(self.session_data['duration'].mean()),
            'total_sessions': len(self.session_data),
            'avg_sessions_per_player': float(
                self.session_data.groupby('player_id').size().mean()
            )
        }

class PerformanceAnalyzer:
    """游戏性能分析器"""
    
    def __init__(self, session_data: pd.DataFrame):
        self.session_data = session_data
    
    def analyze_performance_metrics(self) -> Dict[str, Any]:
        """分析性能指标"""
        crash_rate = (self.session_data['crashes'].sum() / 
                     len(self.session_data)) * 100
        
        avg_load_time = random.uniform(2.0, 8.0)  # 模拟加载时间
        server_uptime = random.uniform(95.0, 99.9)  # 模拟服务器正常运行时间
        
        return {
            'crash_rate': round(crash_rate, 2),
            'avg_load_time': round(avg_load_time, 2),
            'server_uptime': round(server_uptime, 2),
            'total_crashes': int(self.session_data['crashes'].sum()),
            'performance_score': round(100 - crash_rate - (avg_load_time * 2), 1)
        }

class RevenueAnalyzer:
    """收入分析器"""
    
    def __init__(self, player_data: pd.DataFrame, session_data: pd.DataFrame):
        self.player_data = player_data
        self.session_data = session_data
    
    def analyze_revenue_metrics(self) -> Dict[str, Any]:
        """分析收入指标"""
        total_revenue = self.session_data['revenue'].sum()
        paying_players = len(self.player_data[self.player_data['total_spent'] > 0])
        
        # 按日期分组计算每日收入
        daily_revenue = self.session_data.groupby(
            self.session_data['start_time'].dt.date
        )['revenue'].sum()
        
        return {
            'total_revenue': round(total_revenue, 2),
            'paying_players': paying_players,
            'conversion_rate': round((paying_players / len(self.player_data)) * 100, 2),
            'arpu': round(total_revenue / len(self.player_data), 2),
            'arppu': round(total_revenue / max(paying_players, 1), 2),
            'daily_revenue': {
                str(date): round(revenue, 2) 
                for date, revenue in daily_revenue.items()
            }
        }

class RetentionAnalyzer:
    """留存分析器"""
    
    def __init__(self, player_data: pd.DataFrame, session_data: pd.DataFrame):
        self.player_data = player_data
        self.session_data = session_data
    
    def analyze_retention_metrics(self) -> Dict[str, Any]:
        """分析留存指标"""
        # 计算不同时期的留存率
        now = datetime.now()
        
        # 1日留存
        day1_players = self.player_data[
            self.player_data['registration_date'] <= now - timedelta(days=1)
        ]
        day1_retained = day1_players[
            day1_players['last_login'] >= now - timedelta(days=1)
        ]
        day1_retention = len(day1_retained) / max(len(day1_players), 1) * 100
        
        # 7日留存
        day7_players = self.player_data[
            self.player_data['registration_date'] <= now - timedelta(days=7)
        ]
        day7_retained = day7_players[
            day7_players['last_login'] >= now - timedelta(days=7)
        ]
        day7_retention = len(day7_retained) / max(len(day7_players), 1) * 100
        
        # 30日留存
        day30_players = self.player_data[
            self.player_data['registration_date'] <= now - timedelta(days=30)
        ]
        day30_retained = day30_players[
            day30_players['last_login'] >= now - timedelta(days=30)
        ]
        day30_retention = len(day30_retained) / max(len(day30_players), 1) * 100
        
        return {
            'day1_retention': round(day1_retention, 2),
            'day7_retention': round(day7_retention, 2),
            'day30_retention': round(day30_retention, 2),
            'churn_risk_players': len(self.player_data[
                self.player_data['last_login'] <= now - timedelta(days=14)
            ])
        }

class VisualizationGenerator:
    """数据可视化生成器"""
    
    @staticmethod
    def generate_chart_config(chart_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """生成图表配置"""
        if chart_type == 'player_segments':
            return {
                'type': 'pie',
                'title': '玩家分群分布',
                'data': data.get('segments', {}),
                'description': f"总玩家数: {data.get('total_players', 0)}"
            }
        elif chart_type == 'daily_revenue':
            return {
                'type': 'line',
                'title': '每日收入趋势',
                'data': data.get('daily_revenue', {}),
                'description': f"总收入: ${data.get('total_revenue', 0)}"
            }
        elif chart_type == 'retention_funnel':
            return {
                'type': 'funnel',
                'title': '用户留存漏斗',
                'data': {
                    '新用户': 100,
                    '1日留存': data.get('day1_retention', 0),
                    '7日留存': data.get('day7_retention', 0),
                    '30日留存': data.get('day30_retention', 0)
                },
                'description': '用户留存率分析'
            }
        else:
            return {
                'type': 'bar',
                'title': '数据概览',
                'data': data,
                'description': '游戏数据分析结果'
            }

# 全局数据缓存
_game_data_cache: Dict[str, Any] = {
    'player_data': None,
    'session_data': None,
    'last_update': None
}

def get_game_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """获取游戏数据（带缓存）"""
    global _game_data_cache

    # 如果缓存为空或超过1小时，重新生成数据
    if (_game_data_cache['last_update'] is None or
        datetime.now() - _game_data_cache['last_update'] > timedelta(hours=1)):

        _game_data_cache['player_data'] = GameDataGenerator.generate_player_data()
        _game_data_cache['session_data'] = GameDataGenerator.generate_session_data()
        _game_data_cache['last_update'] = datetime.now()

    return _game_data_cache['player_data'], _game_data_cache['session_data']
