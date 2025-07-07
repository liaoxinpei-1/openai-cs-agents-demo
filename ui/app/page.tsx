"use client";

import { useEffect, useState } from "react";
import { AgentPanel } from "@/components/agent-panel";
import { Chat } from "@/components/chat";
import type { Agent, AgentEvent, GuardrailCheck, Message, GameAnalyticsContext } from "@/lib/types";
import { callChatAPI } from "@/lib/api";

// 生成唯一ID的辅助函数
const generateId = (() => {
  let counter = 0;
  return (prefix: string = "id") => `${prefix}-${Date.now()}-${++counter}`;
})();

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [events, setEvents] = useState<AgentEvent[]>([]);
  const [agents, setAgents] = useState<Agent[]>([]);
  const [currentAgent, setCurrentAgent] = useState<string>("");
  const [guardrails, setGuardrails] = useState<GuardrailCheck[]>([]);
  const [context, setContext] = useState<GameAnalyticsContext>({});
  const [conversationId, setConversationId] = useState<string | null>(null);
  // Loading state while awaiting assistant response
  const [isLoading, setIsLoading] = useState(false);
  // 防止水合错误的标志
  const [isMounted, setIsMounted] = useState(false);

  // 确保组件已挂载
  useEffect(() => {
    setIsMounted(true);
  }, []);

  // Boot the conversation
  useEffect(() => {
    (async () => {
      const data = await callChatAPI("", conversationId ?? "");
      setConversationId(data.conversation_id);
      setCurrentAgent(data.current_agent);
      setContext(data.context);
      const now = Date.now();
      const initialEvents = (data.events || []).map((e: any, index: number) => ({
        ...e,
        timestamp: e.timestamp ?? now + index,
      }));
      setEvents(initialEvents);
      setAgents(data.agents || []);
      setGuardrails(data.guardrails || []);
      if (Array.isArray(data.messages)) {
        setMessages(
          data.messages.map((m: any, index: number) => ({
            id: generateId("initial"),
            content: m.content,
            role: "assistant",
            agent: m.agent,
            timestamp: new Date(now + index),
          }))
        );
      }
    })();
  }, []);

  // Send a user message
  const handleSendMessage = async (content: string) => {
    const now = Date.now();
    const userMsg: Message = {
      id: generateId("user"),
      content,
      role: "user",
      timestamp: new Date(now),
    };

    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);

    const data = await callChatAPI(content, conversationId ?? "");

    if (!conversationId) setConversationId(data.conversation_id);
    setCurrentAgent(data.current_agent);
    setContext(data.context);
    if (data.events) {
      const responseTime = Date.now();
      const stamped = data.events.map((e: any, index: number) => ({
        ...e,
        timestamp: e.timestamp ?? responseTime + index,
      }));
      setEvents((prev) => [...prev, ...stamped]);
    }
    if (data.agents) setAgents(data.agents);
    // Update guardrails state
    if (data.guardrails) setGuardrails(data.guardrails);

    if (data.messages) {
      const responseTime = Date.now();
      const responses: Message[] = data.messages.map((m: any, index: number) => ({
        id: generateId("response"),
        content: m.content,
        role: "assistant",
        agent: m.agent,
        timestamp: new Date(responseTime + index),
      }));
      setMessages((prev) => [...prev, ...responses]);
    }

    setIsLoading(false);
  };

  // 防止水合错误，在客户端挂载前显示加载状态
  if (!isMounted) {
    return (
      <main className="flex h-screen items-center justify-center bg-gray-100">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600 mx-auto mb-4"></div>
          <p className="text-gray-600">正在加载游戏数据分析系统...</p>
        </div>
      </main>
    );
  }

  return (
    <main className="flex h-screen gap-2 bg-gray-100 p-2">
      <AgentPanel
        agents={agents}
        currentAgent={currentAgent}
        events={events}
        guardrails={guardrails}
        context={context}
      />
      <Chat
        messages={messages}
        onSendMessage={handleSendMessage}
        isLoading={isLoading}
      />
    </main>
  );
}
