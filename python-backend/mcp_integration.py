"""
Real MCP Tools Integration Layer
真实的MCP工具集成层

提供与mcp-taskmanager和@antv/mcp-server-chart的真实连接
"""

import asyncio
import json
import logging
import subprocess
import websockets
import aiohttp
from typing import Dict, List, Any, Optional, Union
from pydantic import BaseModel
from dataclasses import dataclass
import uuid
import time
from pathlib import Path

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =========================
# MCP协议数据模型
# =========================

class MCPRequest(BaseModel):
    """MCP请求模型"""
    jsonrpc: str = "2.0"
    id: str
    method: str
    params: Dict[str, Any] = {}

class MCPResponse(BaseModel):
    """MCP响应模型"""
    jsonrpc: str = "2.0"
    id: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None

class MCPError(Exception):
    """MCP错误"""
    def __init__(self, code: int, message: str, data: Any = None):
        self.code = code
        self.message = message
        self.data = data
        super().__init__(f"MCP Error {code}: {message}")

# =========================
# MCP客户端基类
# =========================

class MCPClient:
    """MCP客户端基类"""
    
    def __init__(self, server_command: List[str], server_args: List[str] = None):
        self.server_command = server_command
        self.server_args = server_args or []
        self.process = None
        self.websocket = None
        self.is_connected = False
        self.request_id_counter = 0
        
    async def start(self) -> bool:
        """启动MCP服务器"""
        try:
            # 启动服务器进程
            full_command = self.server_command + self.server_args
            logger.info(f"启动MCP服务器: {' '.join(full_command)}")
            
            self.process = await asyncio.create_subprocess_exec(
                *full_command,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            # 等待服务器启动
            await asyncio.sleep(2)
            
            # 检查进程是否正常运行
            if self.process.returncode is not None:
                stderr = await self.process.stderr.read()
                raise Exception(f"服务器启动失败: {stderr.decode()}")
            
            self.is_connected = True
            logger.info("MCP服务器启动成功")
            return True
            
        except Exception as e:
            logger.error(f"启动MCP服务器失败: {e}")
            return False
    
    async def stop(self):
        """停止MCP服务器"""
        if self.process:
            self.process.terminate()
            await self.process.wait()
            self.is_connected = False
            logger.info("MCP服务器已停止")
    
    def _generate_request_id(self) -> str:
        """生成请求ID"""
        self.request_id_counter += 1
        return f"req_{self.request_id_counter}_{uuid.uuid4().hex[:8]}"
    
    async def _send_request(self, method: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """发送MCP请求"""
        if not self.is_connected:
            raise MCPError(-1, "MCP服务器未连接")
        
        request = MCPRequest(
            id=self._generate_request_id(),
            method=method,
            params=params or {}
        )
        
        try:
            # 通过stdin发送请求
            request_json = request.model_dump_json() + "\n"
            self.process.stdin.write(request_json.encode())
            await self.process.stdin.drain()
            
            # 读取响应
            response_line = await self.process.stdout.readline()
            if not response_line:
                raise MCPError(-2, "服务器无响应")
            
            response_data = json.loads(response_line.decode().strip())
            response = MCPResponse(**response_data)
            
            if response.error:
                raise MCPError(
                    response.error.get('code', -1),
                    response.error.get('message', 'Unknown error'),
                    response.error.get('data')
                )
            
            return response.result or {}
            
        except json.JSONDecodeError as e:
            raise MCPError(-3, f"响应解析失败: {e}")
        except Exception as e:
            raise MCPError(-4, f"请求发送失败: {e}")

# =========================
# 任务管理器MCP客户端
# =========================

class TaskManagerMCPClient(MCPClient):
    """任务管理器MCP客户端"""
    
    def __init__(self):
        # 从配置文件读取路径
        taskmanager_path = "/Users/liaoxinpei/Documents/Cline/MCP/mcp-taskmanager/dist/index.js"
        super().__init__(["node", taskmanager_path])
    
    async def create_task(self, title: str, description: str, priority: str = "medium") -> Dict[str, Any]:
        """创建任务"""
        params = {
            "title": title,
            "description": description,
            "priority": priority,
            "status": "pending"
        }
        return await self._send_request("task/create", params)
    
    async def decompose_task(self, task_id: str, query: str, context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """分解任务"""
        params = {
            "task_id": task_id,
            "query": query,
            "context": context or {},
            "decomposition_strategy": "intelligent"
        }
        result = await self._send_request("task/decompose", params)
        return result.get("subtasks", [])
    
    async def update_task_status(self, task_id: str, status: str, result: Dict[str, Any] = None) -> Dict[str, Any]:
        """更新任务状态"""
        params = {
            "task_id": task_id,
            "status": status,
            "result": result
        }
        return await self._send_request("task/update", params)
    
    async def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """获取任务状态"""
        params = {"task_id": task_id}
        return await self._send_request("task/status", params)
    
    async def list_tasks(self, filter_status: str = None) -> List[Dict[str, Any]]:
        """列出任务"""
        params = {}
        if filter_status:
            params["status"] = filter_status
        result = await self._send_request("task/list", params)
        return result.get("tasks", [])

# =========================
# 图表生成器MCP客户端
# =========================

class ChartGeneratorMCPClient(MCPClient):
    """图表生成器MCP客户端"""
    
    def __init__(self):
        super().__init__(["npx", "-y", "@antv/mcp-server-chart"])
    
    async def generate_chart(self, chart_type: str, data: Dict[str, Any], 
                           title: str = "", options: Dict[str, Any] = None) -> Dict[str, Any]:
        """生成图表"""
        params = {
            "type": chart_type,
            "data": data,
            "title": title,
            "options": options or {}
        }
        return await self._send_request("chart/generate", params)
    
    async def generate_line_chart(self, data: List[Dict[str, Any]], 
                                x_field: str, y_field: str, title: str = "") -> Dict[str, Any]:
        """生成折线图"""
        params = {
            "data": data,
            "x_field": x_field,
            "y_field": y_field,
            "title": title
        }
        return await self._send_request("chart/line", params)
    
    async def generate_bar_chart(self, data: List[Dict[str, Any]], 
                               category_field: str, value_field: str, title: str = "") -> Dict[str, Any]:
        """生成柱状图"""
        params = {
            "data": data,
            "category_field": category_field,
            "value_field": value_field,
            "title": title
        }
        return await self._send_request("chart/bar", params)
    
    async def generate_pie_chart(self, data: List[Dict[str, Any]], 
                               category_field: str, value_field: str, title: str = "") -> Dict[str, Any]:
        """生成饼图"""
        params = {
            "data": data,
            "category_field": category_field,
            "value_field": value_field,
            "title": title
        }
        return await self._send_request("chart/pie", params)
    
    async def generate_dashboard(self, charts: List[Dict[str, Any]], 
                               layout: str = "grid", title: str = "") -> Dict[str, Any]:
        """生成仪表板"""
        params = {
            "charts": charts,
            "layout": layout,
            "title": title
        }
        return await self._send_request("dashboard/create", params)

# =========================
# MCP集成管理器
# =========================

class MCPIntegrationManager:
    """MCP集成管理器"""
    
    def __init__(self):
        self.task_manager = TaskManagerMCPClient()
        self.chart_generator = ChartGeneratorMCPClient()
        self.is_initialized = False
    
    async def initialize(self) -> bool:
        """初始化所有MCP客户端"""
        try:
            logger.info("初始化MCP集成管理器...")
            
            # 启动任务管理器
            task_manager_ok = await self.task_manager.start()
            if not task_manager_ok:
                logger.error("任务管理器启动失败")
                return False
            
            # 启动图表生成器
            chart_generator_ok = await self.chart_generator.start()
            if not chart_generator_ok:
                logger.error("图表生成器启动失败")
                await self.task_manager.stop()
                return False
            
            self.is_initialized = True
            logger.info("MCP集成管理器初始化成功")
            return True
            
        except Exception as e:
            logger.error(f"MCP集成管理器初始化失败: {e}")
            return False
    
    async def shutdown(self):
        """关闭所有MCP客户端"""
        if self.task_manager.is_connected:
            await self.task_manager.stop()
        if self.chart_generator.is_connected:
            await self.chart_generator.stop()
        self.is_initialized = False
        logger.info("MCP集成管理器已关闭")
    
    async def health_check(self) -> Dict[str, bool]:
        """健康检查"""
        return {
            "task_manager": self.task_manager.is_connected,
            "chart_generator": self.chart_generator.is_connected,
            "overall": self.is_initialized
        }

# 全局MCP管理器实例
mcp_manager = MCPIntegrationManager()
