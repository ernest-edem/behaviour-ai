"use client";

import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    Tooltip,
    CartesianGrid,
    ResponsiveContainer,
    Legend,
} from "recharts";

type TrendData = {
    date: string;
    health_score: number;
    risk_score: number;
};

interface Props {
    data: TrendData[];
}

export default function HealthTrendChart({
    data,
}: Props) {
    return (
        <div className="w-full h-[400px] bg-white rounded-lg shadow p-4">
            <h2 className="text-xl font-semibold mb-4">
                Health Trends
            </h2>

            <ResponsiveContainer width="100%" height="100%">
                <LineChart data={data}>
                    <CartesianGrid strokeDasharray="3 3" />

                    <XAxis dataKey="date" />

                    <YAxis domain={[0, 100]} />

                    <Tooltip />

                    <Legend />

                    <Line
                        type="monotone"
                        dataKey="health_score"
                        stroke="#22c55e"
                        strokeWidth={3}
                        name="Health Score"
                    />

                    <Line
                        type="monotone"
                        dataKey="risk_score"
                        stroke="#ef4444"
                        strokeWidth={3}
                        name="Risk Score"
                    />
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
}