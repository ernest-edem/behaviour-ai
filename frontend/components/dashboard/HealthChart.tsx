"use client";

import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    Tooltip,
    ResponsiveContainer,
} from "recharts";

export default function HealthChart({ data }: any) {
    return (
        <div className="bg-zinc-900 p-4 rounded-xl h-64">
            <h2 className="text-sm text-gray-400 mb-2">
                Health Trend
            </h2>

            <ResponsiveContainer width="100%" height="100%">
                <LineChart data={data}>
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Line
                        type="monotone"
                        dataKey="health_score"
                        stroke="#22c55e"
                    />
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
}