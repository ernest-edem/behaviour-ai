"use client";

import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    Tooltip,
    ResponsiveContainer,
} from "recharts";

export default function RiskChart({ data }: any) {
    return (
        <div className="bg-zinc-900 p-4 rounded-xl h-64">
            <h2 className="text-sm text-gray-400 mb-2">
                Risk Trend
            </h2>

            <ResponsiveContainer width="100%" height="100%">
                <LineChart data={data}>
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Line
                        type="monotone"
                        dataKey="risk_score"
                        stroke="#ef4444"
                    />
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
}