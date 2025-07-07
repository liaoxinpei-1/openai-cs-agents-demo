"use client";

import { PanelSection } from "./panel-section";
import { Card, CardContent } from "@/components/ui/card";
import { BarChart3 } from "lucide-react";
import type { GameAnalyticsContext } from "@/lib/types";

interface ConversationContextProps {
  context: GameAnalyticsContext;
}

export function ConversationContext({ context }: ConversationContextProps) {
  return (
    <PanelSection
      title="分析上下文"
      icon={<BarChart3 className="h-4 w-4 text-purple-600" />}
    >
      <Card className="bg-gradient-to-r from-white to-purple-50 border-purple-200 shadow-sm">
        <CardContent className="p-3">
          <div className="grid grid-cols-2 gap-2">
            {Object.entries(context).map(([key, value]) => {
              // Format display value based on key type
              let displayValue = value;
              if (key === 'time_range' && typeof value === 'object' && value) {
                displayValue = `${value.start || 'N/A'} - ${value.end || 'N/A'}`;
              } else if (key === 'metrics' && Array.isArray(value)) {
                displayValue = value.join(', ');
              } else if (typeof value === 'object' && value) {
                displayValue = JSON.stringify(value);
              }

              return (
                <div
                  key={key}
                  className="flex items-center gap-2 bg-white p-2 rounded-md border border-purple-200 shadow-sm transition-all"
                >
                  <div className="w-2 h-2 rounded-full bg-purple-500"></div>
                  <div className="text-xs">
                    <span className="text-zinc-500 font-light">{key}:</span>{" "}
                    <span
                      className={
                        displayValue
                          ? "text-zinc-900 font-light"
                          : "text-gray-400 italic"
                      }
                    >
                      {displayValue || "null"}
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        </CardContent>
      </Card>
    </PanelSection>
  );
}