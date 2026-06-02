"use client";

import {
    ResponsiveContainer,
    LineChart,
    Line,
    XAxis,
    YAxis,
    Tooltip,
    CartesianGrid,
    Legend,
} from "recharts";

interface PredictionHistoryItem {
    date: string;
    health_score: number;
    risk_score: number;
}

interface Props {
    data: PredictionHistoryItem[];
}

export default function PredictionTrendChart({
    data,
}: Props) {
    return (
        <div className="bg-zinc-900 p-4 rounded-xl">
            <h2 className="text-lg font-semibold mb-4">
                Prediction Trends
            </h2>

            <div className="h-[350px]">
                <ResponsiveContainer
                    width="100%"
                    height="100%"
                >
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
        </div>
    );
}