"use client";

import { useEffect, useState } from "react";
import { getDashboard } from "@/lib/api/dashboardApi";

import StatCard from "@/components/dashboard/StatCard";
import HealthChart from "@/components/dashboard/HealthChart";
import RiskChart from "@/components/dashboard/RiskChart";
import TrendBadge from "@/components/dashboard/TrendBadge";
import AlertPanel from "@/components/dashboard/AlertPanel";

export default function DashboardPage() {
    const [data, setData] = useState<any>(null);
    const [loading, setLoading] = useState(true);

    const user =
        typeof window !== "undefined"
            ? JSON.parse(localStorage.getItem("user") || "null")
            : null;

    useEffect(() => {
        async function load() {
            try {
                if (!user?.id) return;

                const res = await getDashboard(user.id);
                setData(res.data);
            } catch (err) {
                console.error("Dashboard load error:", err);
            } finally {
                setLoading(false);
            }
        }

        load();
    }, [user?.id]);

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center text-white">
                Loading dashboard...
            </div>
        );
    }

    if (!data) {
        return (
            <div className="min-h-screen flex items-center justify-center text-red-400">
                Failed to load dashboard
            </div>
        );
    }

    return (
        <div className="p-6 bg-black min-h-screen text-white">
            {/* HEADER */}
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-2xl font-bold">Health Dashboard</h1>
                <TrendBadge trend={data.summary.trend} />
            </div>

            {/* KPI CARDS */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                <StatCard
                    title="Avg Health Score"
                    value={data.summary.avg_health_score}
                />

                <StatCard
                    title="Avg Risk Score"
                    value={data.summary.avg_risk_score}
                    color="text-red-400"
                />

                <StatCard
                    title="Data Points"
                    value={data.data_points}
                    subtitle="Last 30 days"
                />
            </div>

            {/* MAIN GRID */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div className="lg:col-span-2 space-y-6">
                    <HealthChart data={data.timeline} />
                    <RiskChart data={data.timeline} />
                </div>

                <div>
                    <AlertPanel />
                </div>
            </div>
        </div>
    );
}